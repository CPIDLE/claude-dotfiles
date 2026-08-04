"""
呼叫 Gemini API（預設 gemini-3-pro-image，即 Nano Banana Pro）依 prompt 生成圖片。

用法：
    python gemini_image_gen.py --prompt-file prompt.md --out out.png
    python gemini_image_gen.py --prompt "一段文字" --out out.png
    python gemini_image_gen.py --prompt-file p.md --out v2.png --ref ref.png   # 圖生圖/以圖修圖
    python gemini_image_gen.py --prompt-file p.md --out v2.png --size 4K       # 拉高解析度

Key 來源優先序：環境變數 GEMINI_API_KEY > ~/.claude/.env 裡的 GEMINI_API_KEY。
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error

DEFAULT_MODEL = "gemini-3-pro-image"  # Nano Banana Pro，中文密集文字渲染明顯優於 gemini-2.5-flash-image
DOTENV_FALLBACK = os.path.join(os.path.expanduser("~"), ".claude", ".env")


def load_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    if os.path.exists(DOTENV_FALLBACK):
        with open(DOTENV_FALLBACK, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(f"找不到 GEMINI_API_KEY，請設環境變數或確認 {DOTENV_FALLBACK} 存在該欄位")


def build_parts(prompt_text, ref_image_path):
    parts = []
    if ref_image_path:
        mime, _ = mimetypes.guess_type(ref_image_path)
        with open(ref_image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        parts.append({"inlineData": {"mimeType": mime or "image/png", "data": data}})
    parts.append({"text": prompt_text})
    return parts


def generate(prompt_text, out_path, ref_image_path=None, api_key=None, model=DEFAULT_MODEL,
             image_size=None, aspect_ratio=None):
    api_key = api_key or load_api_key()
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {"contents": [{"parts": build_parts(prompt_text, ref_image_path)}]}
    image_config = {}
    if image_size:
        image_config["imageSize"] = image_size
    if aspect_ratio:
        image_config["aspectRatio"] = aspect_ratio
    if image_config:
        body["generationConfig"] = {"imageConfig": image_config}
    req = urllib.request.Request(
        f"{api_url}?key={api_key}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"API 錯誤 {e.code}: {e.read().decode('utf-8', 'replace')}")

    candidates = payload.get("candidates", [])
    if not candidates:
        sys.exit(f"沒有回傳 candidates，完整回應：{json.dumps(payload, ensure_ascii=False)[:2000]}")

    saved = False
    text_notes = []
    for part in candidates[0]["content"]["parts"]:
        if "inlineData" in part:
            img_bytes = base64.b64decode(part["inlineData"]["data"])
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            print(f"已存檔：{out_path}（{len(img_bytes)} bytes）")
            saved = True
        elif "text" in part:
            text_notes.append(part["text"])

    if text_notes:
        print("模型附帶文字回應：", " ".join(text_notes)[:500])
    if not saved:
        sys.exit("回應中沒有圖片資料（inlineData），可能被安全過濾擋下或 prompt 需調整")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--prompt", help="直接傳入 prompt 文字")
    src.add_argument("--prompt-file", help="從檔案讀 prompt（.md/.txt 皆可，整檔當文字）")
    ap.add_argument("--out", required=True, help="輸出圖片路徑（.png）")
    ap.add_argument("--ref", help="參考圖片路徑，做圖生圖／以圖修圖時帶入")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"模型名稱（預設 {DEFAULT_MODEL}）")
    ap.add_argument("--size", choices=["1K", "2K", "4K"], help="輸出解析度（gemini-3-pro-image 系列支援）")
    ap.add_argument("--aspect-ratio", default="16:9", help="長寬比（預設 16:9）")
    args = ap.parse_args()

    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as f:
            prompt_text = f.read()
    else:
        prompt_text = args.prompt

    generate(prompt_text, args.out, ref_image_path=args.ref, model=args.model,
              image_size=args.size, aspect_ratio=args.aspect_ratio)


if __name__ == "__main__":
    main()
