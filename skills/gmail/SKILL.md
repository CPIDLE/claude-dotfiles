---
name: gmail
description: "Standalone Python-based Gmail skill for reading, searching, sending, and managing emails via Google API with OAuth2 authentication. Use this skill whenever the user wants to interact with Gmail — checking inbox, searching emails, reading messages, sending or drafting emails, managing labels, or any email-related task. Also trigger when the user mentions 'email', 'inbox', 'unread messages', 'send a message to', 'draft an email', 'check my mail', or references Gmail in any way. This skill uses direct Google API access with stored OAuth credentials, independent of any MCP connector."
---

# Gmail Skill

A self-contained Gmail integration using Google's Python API client with OAuth2 authentication. Provides full Gmail access: search, read, send, draft, label management, and more.

## Setup

The skill requires two Python packages:

```bash
pip install google-auth-oauthlib google-api-python-client
```

### Credential paths

- **Client secret**: `C:\Users\benth\.claude\skills\gmail\assets\client_secret.json`
- **Token cache**: `C:\Users\benth\.claude\skills\gmail\assets\token.json` (auto-generated after first auth)

If `token.json` doesn't exist or is expired, the auth script will open a browser for the user to log in. After that, the token refreshes automatically.

## How to use

All Gmail operations go through a single Python script. Run it via Bash:

```bash
PYTHONIOENCODING=utf-8 python "C:/Users/benth/.claude/skills/gmail/scripts/gmail_ops.py" <command> [options]
```

**Important**: Always set `PYTHONIOENCODING=utf-8` to handle CJK and Unicode characters in email content on Windows.

### Available commands

| Command | Description | Key options |
|---------|-------------|-------------|
| `search` | Search messages | `--query`, `--max-results` |
| `read` | Read a full message | `--message-id` |
| `thread` | Read entire thread | `--thread-id` |
| `send` | Send an email | `--to`, `--subject`, `--body`, `--cc`, `--bcc`, `--html` |
| `draft` | Create a draft | `--to`, `--subject`, `--body`, `--thread-id` |
| `send-draft` | Send an existing draft | `--draft-id` |
| `reply` | Reply to a message | `--message-id`, `--body`, `--html` |
| `labels` | List all labels | (no options) |
| `modify` | Add/remove labels | `--thread-id`, `--add-labels`, `--remove-labels` |
| `profile` | Show account info | (no options) |
| `auth` | Force re-authentication | (no options) |
| `attachments` | Download attachments | `--message-id`, `--output-dir` |
| `send-attach` | Send with attachments | `--to`, `--subject`, `--body`, `--attachments` |

### Examples

```bash
# Search unread emails
python gmail_ops.py search --query "is:unread" --max-results 10

# Read a specific message
python gmail_ops.py read --message-id "18e3a4b5c6d7e8f9"

# Send an email
python gmail_ops.py send --to "someone@example.com" --subject "Hello" --body "Message body here"

# Send HTML email
python gmail_ops.py send --to "someone@example.com" --subject "Report" --body "<h1>Title</h1><p>Content</p>" --html

# Create a draft reply
python gmail_ops.py draft --to "someone@example.com" --subject "Re: Topic" --body "Draft reply" --thread-id "18e3a4b5c6d7e8f9"

# Reply to a message
python gmail_ops.py reply --message-id "18e3a4b5c6d7e8f9" --body "Thanks for the update!"

# Download attachments
python gmail_ops.py attachments --message-id "18e3a4b5c6d7e8f9" --output-dir ./downloads

# Send with attachments
python gmail_ops.py send-attach --to "someone@example.com" --subject "Files" --body "See attached" --attachments file1.pdf file2.png

# Modify labels on a thread
python gmail_ops.py modify --thread-id "18e3a4b5c6d7e8f9" --add-labels "STARRED" --remove-labels "UNREAD"
```

### Output format

All commands output JSON to stdout for easy parsing. Error messages go to stderr. A non-zero exit code means failure — check stderr for details.

### Authentication flow

On first run (or when token expires and can't refresh), the script opens a browser window for Google OAuth consent. The user must approve access. After that, `token.json` is saved and reused automatically. If running in a headless environment, the script prints a URL for the user to visit manually.

## Important notes

- Always use `--query` with Gmail search syntax (same as the Gmail search bar): `from:`, `to:`, `subject:`, `is:unread`, `has:attachment`, `after:2024/1/1`, etc.
- Message and thread IDs come from the `search` command output.
- The `--body` flag accepts plain text by default. Add `--html` to send HTML-formatted email.
- When replying, the script automatically handles `In-Reply-To` and `References` headers.
- Label IDs can be found via the `labels` command. Common system labels: `INBOX`, `UNREAD`, `STARRED`, `SPAM`, `TRASH`.
