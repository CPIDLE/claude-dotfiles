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

# 1. Global CLAUDE.md (global-claude.md -> ~/.claude/CLAUDE.md)
echo ""
echo "--- CLAUDE.md (global) ---"
backup_and_copy "$SCRIPT_DIR/global-claude.md" "$CLAUDE_DIR/CLAUDE.md"

# 2. settings.json
echo ""
echo "--- settings.json ---"
backup_and_copy "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"

# 2.5. settings.local.json (permissions whitelist)
echo ""
echo "--- settings.local.json ---"
if [ -e "$SCRIPT_DIR/settings.local.json" ]; then
    backup_and_copy "$SCRIPT_DIR/settings.local.json" "$CLAUDE_DIR/settings.local.json"
fi

# 3. Status Line
echo ""
echo "--- Status Line ---"
backup_and_copy "$SCRIPT_DIR/statusline.sh" "$CLAUDE_DIR/statusline.sh"
backup_and_copy "$SCRIPT_DIR/statusline.js" "$CLAUDE_DIR/statusline.js"
backup_and_copy "$SCRIPT_DIR/pm-update.sh" "$CLAUDE_DIR/pm-update.sh"

# 4. Commands
echo ""
echo "--- Commands ---"
mkdir -p "$CLAUDE_DIR/commands"
for f in "$SCRIPT_DIR/commands/"*.md; do
    [ -e "$f" ] || continue
    backup_and_copy "$f" "$CLAUDE_DIR/commands/$(basename "$f")"
done

# 5. opencode Commands (if opencode is installed)
echo ""
echo "--- opencode Commands ---"
if command -v opencode &>/dev/null; then
    OPENCODE_DIR="$HOME/.config/opencode/commands"
    mkdir -p "$OPENCODE_DIR"
    if [ -d "$SCRIPT_DIR/commands-opencode" ]; then
        for f in "$SCRIPT_DIR/commands-opencode/"*.md; do
            [ -e "$f" ] || continue
            backup_and_copy "$f" "$OPENCODE_DIR/$(basename "$f")"
        done
    else
        echo "  [SKIP] commands-opencode/ not found"
    fi
else
    echo "  [SKIP] opencode not installed"
fi

echo ""
echo "=== Done! ==="
