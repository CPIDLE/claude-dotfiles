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

## Post-Install Checklist

After running the install script:

1. **Gmail OAuth credentials** — manually copy `token.json` and `client_secret.json` into `~/.claude/skills/gmail/assets/` (not stored in repo for security)
2. **Marketplace plugins** — reinstall with `claude plugins install`
3. **MCP Connectors** — reconnect via OAuth (Gmail, Google Calendar, Slack, Google Drive) — these are cloud-based and cannot be transferred via files

## Conflict Handling

The install script uses a **backup + merge** strategy:

- Existing files with same names → backed up as `.bak`, then overwritten
- Files unique to the target machine → preserved (not deleted)
- MCP connectors and marketplace plugins → not affected

