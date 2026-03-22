#!/bin/bash
# Claude Code Dotfiles Installer (macOS / Linux)
# Usage: bash install.sh

set -e

CLAUDE_DIR="$HOME/.claude"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Claude Code Dotfiles Installer ==="
echo ""

# Ensure ~/.claude/ exists
mkdir -p "$CLAUDE_DIR"

backup_and_copy() {
    local src="$1" dest="$2"
    if [ -e "$dest" ]; then
        cp "$dest" "$dest.bak"
        echo "  [BAK] $dest -> $dest.bak"
    fi
    cp "$src" "$dest"
    echo "  [OK]  $dest"
}

# 1. CLAUDE.md
echo ""
echo "--- CLAUDE.md ---"
backup_and_copy "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"

# 2. settings.json
echo ""
echo "--- settings.json ---"
backup_and_copy "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"

# 3. Status Line
echo ""
echo "--- Status Line ---"
backup_and_copy "$SCRIPT_DIR/statusline.sh" "$CLAUDE_DIR/statusline.sh"
backup_and_copy "$SCRIPT_DIR/statusline.js" "$CLAUDE_DIR/statusline.js"

# 4. Commands
echo ""
echo "--- Commands ---"
mkdir -p "$CLAUDE_DIR/commands"
for f in "$SCRIPT_DIR/commands/"*.md; do
    [ -e "$f" ] || continue
    backup_and_copy "$f" "$CLAUDE_DIR/commands/$(basename "$f")"
done

echo ""
echo "=== Done! ==="
