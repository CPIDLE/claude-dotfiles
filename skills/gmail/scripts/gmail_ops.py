#!/usr/bin/env python3
"""
Standalone Gmail CLI tool using Google API with OAuth2.
All commands output JSON to stdout; errors go to stderr.
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

# Paths
SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
CLIENT_SECRET = ASSETS_DIR / "client_secret.json"
TOKEN_FILE = ASSETS_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
]


def get_credentials():
    """Get valid OAuth2 credentials, prompting for auth if needed."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            if not CLIENT_SECRET.exists():
                print(json.dumps({"error": f"Client secret not found at {CLIENT_SECRET}"}), file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())

    return creds


def get_service():
    """Build Gmail API service."""
    from googleapiclient.discovery import build
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)


def output(data):
    """Print JSON to stdout, handling Windows encoding issues."""
    text = json.dumps(data, ensure_ascii=False, indent=2)
    try:
        sys.stdout.buffer.write(text.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()
    except AttributeError:
        # Fallback if buffer not available
        print(json.dumps(data, ensure_ascii=True, indent=2))


def parse_message(msg):
    """Extract useful fields from a Gmail message resource."""
    headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}

    # Extract body
    body_text = ""
    body_html = ""
    payload = msg.get("payload", {})

    def extract_parts(part):
        nonlocal body_text, body_html
        mime = part.get("mimeType", "")
        if mime == "text/plain" and "data" in part.get("body", {}):
            body_text = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
        elif mime == "text/html" and "data" in part.get("body", {}):
            body_html = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
        for sub in part.get("parts", []):
            extract_parts(sub)

    extract_parts(payload)

    # If body is directly in payload (no parts)
    if not body_text and not body_html and "data" in payload.get("body", {}):
        data = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")
        if payload.get("mimeType") == "text/html":
            body_html = data
        else:
            body_text = data

    # Extract attachments info
    attachments = []
    def find_attachments(part):
        if part.get("filename"):
            attachments.append({
                "filename": part["filename"],
                "mimeType": part.get("mimeType", ""),
                "size": part.get("body", {}).get("size", 0),
                "attachmentId": part.get("body", {}).get("attachmentId", ""),
            })
        for sub in part.get("parts", []):
            find_attachments(sub)
    find_attachments(payload)

    return {
        "id": msg["id"],
        "threadId": msg["threadId"],
        "labelIds": msg.get("labelIds", []),
        "snippet": msg.get("snippet", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "cc": headers.get("cc", ""),
        "subject": headers.get("subject", ""),
        "date": headers.get("date", ""),
        "message_id": headers.get("message-id", ""),
        "body_text": body_text,
        "body_html": body_html,
        "attachments": attachments,
    }


# --- Commands ---

def cmd_profile(args):
    svc = get_service()
    profile = svc.users().getProfile(userId="me").execute()
    output(profile)


def cmd_labels(args):
    svc = get_service()
    results = svc.users().labels().list(userId="me").execute()
    output(results.get("labels", []))


def cmd_search(args):
    svc = get_service()
    params = {"userId": "me", "maxResults": args.max_results}
    if args.query:
        params["q"] = args.query

    results = svc.users().messages().list(**params).execute()
    messages = results.get("messages", [])

    if not messages:
        output([])
        return

    # Fetch metadata for each message
    parsed = []
    for m in messages:
        msg = svc.users().messages().get(userId="me", id=m["id"], format="metadata",
                                          metadataHeaders=["From", "To", "Subject", "Date"]).execute()
        headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
        parsed.append({
            "id": msg["id"],
            "threadId": msg["threadId"],
            "snippet": msg.get("snippet", ""),
            "labelIds": msg.get("labelIds", []),
            "from": headers.get("from", ""),
            "to": headers.get("to", ""),
            "subject": headers.get("subject", ""),
            "date": headers.get("date", ""),
        })

    output(parsed)


def cmd_read(args):
    svc = get_service()
    msg = svc.users().messages().get(userId="me", id=args.message_id, format="full").execute()
    output(parse_message(msg))


def cmd_thread(args):
    svc = get_service()
    thread = svc.users().threads().get(userId="me", id=args.thread_id, format="full").execute()
    messages = [parse_message(m) for m in thread.get("messages", [])]
    output({"threadId": thread["id"], "messages": messages})


def cmd_send(args):
    svc = get_service()

    if args.html:
        msg = MIMEText(args.body, "html")
    else:
        msg = MIMEText(args.body, "plain")

    msg["to"] = args.to
    msg["subject"] = args.subject
    if args.cc:
        msg["cc"] = args.cc
    if args.bcc:
        msg["bcc"] = args.bcc

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = svc.users().messages().send(userId="me", body={"raw": raw}).execute()
    output({"status": "sent", "id": result["id"], "threadId": result["threadId"]})


def cmd_send_attach(args):
    svc = get_service()

    message = MIMEMultipart()
    message["to"] = args.to
    message["subject"] = args.subject
    if args.cc:
        message["cc"] = args.cc
    if args.bcc:
        message["bcc"] = args.bcc

    if args.html:
        message.attach(MIMEText(args.body, "html"))
    else:
        message.attach(MIMEText(args.body, "plain"))

    for filepath in args.attachments:
        path = Path(filepath)
        if not path.exists():
            print(json.dumps({"error": f"File not found: {filepath}"}), file=sys.stderr)
            sys.exit(1)

        content_type, _ = mimetypes.guess_type(str(path))
        if content_type is None:
            content_type = "application/octet-stream"
        main_type, sub_type = content_type.split("/", 1)

        with open(path, "rb") as f:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=path.name)
        message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    result = svc.users().messages().send(userId="me", body={"raw": raw}).execute()
    output({"status": "sent", "id": result["id"], "threadId": result["threadId"]})


def cmd_draft(args):
    svc = get_service()

    if args.html:
        msg = MIMEText(args.body, "html")
    else:
        msg = MIMEText(args.body, "plain")

    msg["to"] = args.to
    msg["subject"] = args.subject

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    body = {"message": {"raw": raw}}
    if args.thread_id:
        body["message"]["threadId"] = args.thread_id

    result = svc.users().drafts().create(userId="me", body=body).execute()
    output({"status": "drafted", "draftId": result["id"], "messageId": result["message"]["id"]})


def cmd_send_draft(args):
    svc = get_service()
    result = svc.users().drafts().send(userId="me", body={"id": args.draft_id}).execute()
    output({"status": "sent", "id": result["id"], "threadId": result.get("threadId", "")})


def cmd_reply(args):
    svc = get_service()

    # Get original message for headers
    orig = svc.users().messages().get(userId="me", id=args.message_id, format="metadata",
                                       metadataHeaders=["From", "To", "Cc", "Subject", "Message-ID"]).execute()
    headers = {h["name"].lower(): h["value"] for h in orig.get("payload", {}).get("headers", [])}

    if args.html:
        msg = MIMEText(args.body, "html")
    else:
        msg = MIMEText(args.body, "plain")

    msg["to"] = headers.get("from", "")
    subject = headers.get("subject", "")
    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"
    msg["subject"] = subject

    message_id = headers.get("message-id", "")
    if message_id:
        msg["In-Reply-To"] = message_id
        msg["References"] = message_id

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = svc.users().messages().send(
        userId="me",
        body={"raw": raw, "threadId": orig["threadId"]}
    ).execute()
    output({"status": "sent", "id": result["id"], "threadId": result["threadId"]})


def cmd_modify(args):
    svc = get_service()
    body = {}
    if args.add_labels:
        body["addLabelIds"] = args.add_labels
    if args.remove_labels:
        body["removeLabelIds"] = args.remove_labels

    result = svc.users().threads().modify(userId="me", id=args.thread_id, body=body).execute()
    output({"status": "modified", "threadId": result["id"], "labels": result.get("messages", [{}])[0].get("labelIds", [])})


def cmd_attachments(args):
    svc = get_service()
    msg = svc.users().messages().get(userId="me", id=args.message_id, format="full").execute()

    out_dir = Path(args.output_dir) if args.output_dir else Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    def download_parts(part):
        if part.get("filename") and part.get("body", {}).get("attachmentId"):
            att = svc.users().messages().attachments().get(
                userId="me", messageId=args.message_id, id=part["body"]["attachmentId"]
            ).execute()
            data = base64.urlsafe_b64decode(att["data"])
            filepath = out_dir / part["filename"]
            filepath.write_bytes(data)
            saved.append({"filename": part["filename"], "path": str(filepath), "size": len(data)})
        for sub in part.get("parts", []):
            download_parts(sub)

    download_parts(msg.get("payload", {}))
    output({"status": "downloaded", "attachments": saved})


def cmd_auth(args):
    """Force re-authentication by deleting token and re-running auth flow."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
    get_credentials()
    output({"status": "authenticated"})


def main():
    parser = argparse.ArgumentParser(description="Gmail CLI tool")
    sub = parser.add_subparsers(dest="command", required=True)

    # profile
    sub.add_parser("profile", help="Show account info")

    # labels
    sub.add_parser("labels", help="List all labels")

    # search
    p = sub.add_parser("search", help="Search messages")
    p.add_argument("--query", "-q", default="", help="Gmail search query")
    p.add_argument("--max-results", "-n", type=int, default=10, help="Max results")

    # read
    p = sub.add_parser("read", help="Read a message")
    p.add_argument("--message-id", "-m", required=True, help="Message ID")

    # thread
    p = sub.add_parser("thread", help="Read entire thread")
    p.add_argument("--thread-id", "-t", required=True, help="Thread ID")

    # send
    p = sub.add_parser("send", help="Send an email")
    p.add_argument("--to", required=True, help="Recipient(s)")
    p.add_argument("--subject", "-s", required=True, help="Subject")
    p.add_argument("--body", "-b", required=True, help="Body text")
    p.add_argument("--cc", default=None, help="CC recipients")
    p.add_argument("--bcc", default=None, help="BCC recipients")
    p.add_argument("--html", action="store_true", help="Send as HTML")

    # send-attach
    p = sub.add_parser("send-attach", help="Send with attachments")
    p.add_argument("--to", required=True, help="Recipient(s)")
    p.add_argument("--subject", "-s", required=True, help="Subject")
    p.add_argument("--body", "-b", required=True, help="Body text")
    p.add_argument("--cc", default=None, help="CC recipients")
    p.add_argument("--bcc", default=None, help="BCC recipients")
    p.add_argument("--html", action="store_true", help="Send as HTML")
    p.add_argument("--attachments", nargs="+", required=True, help="File paths")

    # draft
    p = sub.add_parser("draft", help="Create a draft")
    p.add_argument("--to", required=True, help="Recipient(s)")
    p.add_argument("--subject", "-s", required=True, help="Subject")
    p.add_argument("--body", "-b", required=True, help="Body text")
    p.add_argument("--html", action="store_true", help="HTML body")
    p.add_argument("--thread-id", default=None, help="Thread ID for reply draft")

    # send-draft
    p = sub.add_parser("send-draft", help="Send an existing draft")
    p.add_argument("--draft-id", required=True, help="Draft ID")

    # reply
    p = sub.add_parser("reply", help="Reply to a message")
    p.add_argument("--message-id", "-m", required=True, help="Message ID to reply to")
    p.add_argument("--body", "-b", required=True, help="Reply body")
    p.add_argument("--html", action="store_true", help="Send as HTML")

    # modify
    p = sub.add_parser("modify", help="Add/remove labels on a thread")
    p.add_argument("--thread-id", "-t", required=True, help="Thread ID")
    p.add_argument("--add-labels", nargs="*", default=[], help="Labels to add")
    p.add_argument("--remove-labels", nargs="*", default=[], help="Labels to remove")

    # attachments
    p = sub.add_parser("attachments", help="Download attachments")
    p.add_argument("--message-id", "-m", required=True, help="Message ID")
    p.add_argument("--output-dir", "-o", default=None, help="Output directory")

    # auth
    sub.add_parser("auth", help="Force re-authentication")

    args = parser.parse_args()

    commands = {
        "profile": cmd_profile,
        "labels": cmd_labels,
        "search": cmd_search,
        "read": cmd_read,
        "thread": cmd_thread,
        "send": cmd_send,
        "send-attach": cmd_send_attach,
        "draft": cmd_draft,
        "send-draft": cmd_send_draft,
        "reply": cmd_reply,
        "modify": cmd_modify,
        "attachments": cmd_attachments,
        "auth": cmd_auth,
    }

    try:
        commands[args.command](args)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
