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

# 3. Commands
echo ""
echo "--- Commands ---"
mkdir -p "$CLAUDE_DIR/commands"
for f in "$SCRIPT_DIR/commands/"*.md; do
    [ -e "$f" ] || continue
    backup_and_copy "$f" "$CLAUDE_DIR/commands/$(basename "$f")"
done

# 4. Skills
echo ""
echo "--- Skills ---"
mkdir -p "$CLAUDE_DIR/skills"

# Copy skill files at root level
for f in "$SCRIPT_DIR/skills/"*.md; do
    [ -e "$f" ] || continue
    backup_and_copy "$f" "$CLAUDE_DIR/skills/$(basename "$f")"
done

# Copy skill directories
for d in "$SCRIPT_DIR/skills/"/*/; do
    [ -d "$d" ] || continue
    skill_name="$(basename "$d")"
    dest_skill="$CLAUDE_DIR/skills/$skill_name"
    if [ -d "$dest_skill" ]; then
        rm -rf "$dest_skill.bak"
        mv "$dest_skill" "$dest_skill.bak"
        echo "  [BAK] $dest_skill -> $dest_skill.bak"
    fi
    cp -r "$d" "$dest_skill"
    echo "  [OK]  $dest_skill"
done

echo ""
echo "=== Done! ==="
echo ""
echo "Next steps:"
echo "  1. Copy gmail OAuth files manually:"
echo "     token.json + client_secret.json -> $CLAUDE_DIR/skills/gmail/assets/"
echo "  2. Reinstall marketplace plugins: claude plugins install"
echo "  3. Reconnect MCP connectors (Gmail, GCal, Slack) - requires OAuth"
echo "  4. Check gyro-kb skill paths match your new machine"
