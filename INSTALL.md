# Install

## Codex Skill Installer

In Codex, ask:

```text
Install this skill:
https://github.com/KeonSuYun/codex-team-orchestrator/tree/main/skills/codex-team-orchestrator
```

Restart Codex after install.

## Shell Installer

macOS / Linux / WSL:

```bash
curl -fsSL https://raw.githubusercontent.com/KeonSuYun/codex-team-orchestrator/main/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/KeonSuYun/codex-team-orchestrator/main/install.ps1 | iex
```

## Manual Install

Copy:

```text
skills/codex-team-orchestrator
```

to:

```text
$CODEX_HOME/skills/codex-team-orchestrator
```

If `CODEX_HOME` is not set, use:

```text
~/.codex/skills/codex-team-orchestrator
```

Restart Codex.
