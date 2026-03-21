# Claude Code Dotfiles

Personal Claude Code configuration backup — commands, skills, settings, and global instructions.

## Contents

| Directory | Description |
|-----------|-------------|
| `CLAUDE.md` | Global instructions (Plan-Execute workflow, notification hooks) |
| `settings.json` | Hooks, enabled plugins, permissions |
| `commands/` | 3 custom slash commands (`/hello`, `/bye`, `/sc`) |

## Install on a New Machine

### Windows (PowerShell)

```powershell
git clone https://github.com/benthsu/claude-dotfiles.git
cd claude-dotfiles
powershell -ExecutionPolicy Bypass -File install.ps1
```

### macOS / Linux

```bash
git clone https://github.com/benthsu/claude-dotfiles.git
cd claude-dotfiles
bash install.sh
```

## Notes

- Marketplace plugins and MCP connectors are **not affected** — they are stored separately and will remain intact on the target machine.

## Conflict Handling

The install script uses a **backup + merge** strategy:

- Existing files with same names → backed up as `.bak`, then overwritten
- Files unique to the target machine → preserved (not deleted)
- MCP connectors and marketplace plugins → not affected

