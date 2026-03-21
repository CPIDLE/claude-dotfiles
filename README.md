# Claude Code Dotfiles

Personal Claude Code configuration backup — commands, skills, settings, and global instructions.

## Contents

| Directory | Description |
|-----------|-------------|
| `CLAUDE.md` | Global instructions (Plan-Execute workflow, notification hooks) |
| `settings.json` | Hooks, enabled plugins, permissions |
| `commands/` | 8 custom slash commands (`/hello`, `/bye`, `/smart-commit`, `/clip`, `/gyro-report`, `/gyro-kb`, `/sc`, `/win-gui`) |
| `skills/` | 8 custom skills (gyro-report, gyro-kb, agent-browser, dogfood, electron, gmail, slack, vercel-sandbox) |

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
2. **Marketplace plugins** — reinstall with `claude plugins install` (frontend-design, skill-creator, code-simplifier, context7, coderabbit, claude-md-management, playwright, code-review, playground, qodo-skills)
3. **MCP Connectors** — reconnect via OAuth (Gmail, Google Calendar, Slack, Google Drive) — these are cloud-based and cannot be transferred via files
4. **gyro-kb paths** — update `E:/github/personal-rag_v2/` references in `skills/gyro-kb.md` if your knowledge base is in a different location

## Conflict Handling

The install script uses a **backup + merge** strategy:

- Existing files with same names → backed up as `.bak`, then overwritten
- Files unique to the target machine → preserved (not deleted)
- MCP connectors and marketplace plugins → not affected

## Sensitive Files

The following files are excluded via `.gitignore`:

- `**/token.json` — OAuth tokens
- `**/client_secret.json` — OAuth client secrets
