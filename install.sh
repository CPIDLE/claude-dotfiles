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

# 5. opencode Commands + Config (if opencode is installed)
echo ""
echo "--- opencode ---"
if command -v opencode &>/dev/null; then
    OPENCODE_BASE="$HOME/.config/opencode"
    OPENCODE_CMD_DIR="$OPENCODE_BASE/commands"
    mkdir -p "$OPENCODE_CMD_DIR"

    # 5a. Commands
    if [ -d "$SCRIPT_DIR/commands-opencode" ]; then
        for f in "$SCRIPT_DIR/commands-opencode/"*.md; do
            [ -e "$f" ] || continue
            backup_and_copy "$f" "$OPENCODE_CMD_DIR/$(basename "$f")"
        done
    fi

    # 5b. Config files (opencode.json, tui.json, AGENTS.md)
    if [ -d "$SCRIPT_DIR/opencode-config" ]; then
        for f in opencode.json tui.json AGENTS.md; do
            if [ -e "$SCRIPT_DIR/opencode-config/$f" ]; then
                backup_and_copy "$SCRIPT_DIR/opencode-config/$f" "$OPENCODE_BASE/$f"
            fi
        done
        # switch-to-opencode.ps1 (Windows/MSYS only)
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            if [ -e "$SCRIPT_DIR/opencode-config/switch-to-opencode.ps1" ]; then
                backup_and_copy "$SCRIPT_DIR/opencode-config/switch-to-opencode.ps1" "$OPENCODE_BASE/switch-to-opencode.ps1"
            fi
        fi
    fi
else
    echo "  [SKIP] opencode not installed"
fi

# 6. MCP Config
echo ""
echo "--- MCP Config ---"
if [ -e "$SCRIPT_DIR/mcp.json" ]; then
    backup_and_copy "$SCRIPT_DIR/mcp.json" "$CLAUDE_DIR/.mcp.json"
fi

# 7. Claude Switcher (Windows/MSYS only)
echo ""
echo "--- Claude Switcher ---"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    if [ -e "$SCRIPT_DIR/claude-switcher.ps1" ]; then
        backup_and_copy "$SCRIPT_DIR/claude-switcher.ps1" "$CLAUDE_DIR/claude-switcher.ps1"
    fi
else
    echo "  [SKIP] Windows-only utility"
fi

# 8. Skills
echo ""
echo "--- Skills ---"
if [ -d "$SCRIPT_DIR/skills" ]; then
    mkdir -p "$CLAUDE_DIR/skills"
    # Copy skill directories
    for skill_dir in "$SCRIPT_DIR/skills/"*/; do
        [ -d "$skill_dir" ] || continue
        skill_name=$(basename "$skill_dir")
        mkdir -p "$CLAUDE_DIR/skills/$skill_name"
        cp -r "$skill_dir"* "$CLAUDE_DIR/skills/$skill_name/" 2>/dev/null
        echo "  [OK]  ~/.claude/skills/$skill_name/"
    done
    # Copy standalone skill files
    for f in "$SCRIPT_DIR/skills/"*.md; do
        [ -e "$f" ] || continue
        backup_and_copy "$f" "$CLAUDE_DIR/skills/$(basename "$f")"
    done
fi

# 8.5. Hooks
echo ""
echo "--- Hooks ---"
if [ -d "$SCRIPT_DIR/hooks" ]; then
    mkdir -p "$CLAUDE_DIR/hooks"
    for f in "$SCRIPT_DIR/hooks/"*; do
        [ -f "$f" ] || continue
        backup_and_copy "$f" "$CLAUDE_DIR/hooks/$(basename "$f")"
    done
fi

# 9. Docs
echo ""
echo "--- Docs ---"
if [ -d "$SCRIPT_DIR/docs" ]; then
    mkdir -p "$CLAUDE_DIR/docs"
    for f in "$SCRIPT_DIR/docs/"*.md; do
        [ -e "$f" ] || continue
        backup_and_copy "$f" "$CLAUDE_DIR/docs/$(basename "$f")"
    done
fi

# 10. .env reminder
echo ""
if [ ! -e "$CLAUDE_DIR/.env" ]; then
    echo "[INFO] No .env found at $CLAUDE_DIR/.env"
    echo "       Copy .env.example and fill in your secrets:"
    echo "       cp $SCRIPT_DIR/.env.example $CLAUDE_DIR/.env"
fi

# 11. Plugin summary
echo ""
echo "--- Plugins ---"
echo "  Configured in settings.json (auto-install on first launch):"
echo "    skill-creator, code-simplifier, context7, coderabbit,"
echo "    claude-md-management, playwright"
echo "  Optional plugins: see docs/plugins.md"

echo ""
echo "=== Done! ==="
