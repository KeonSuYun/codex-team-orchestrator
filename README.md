# Codex Team Orchestrator

Leader-led Codex project-thread teams.

Use one Codex conversation as the Leader. The Leader can ask which roles you want, create visible project-thread teammates, start them with `/goal`, keep their thread ids in a roster, and route member updates back through the Leader.

## Install

### From Codex

Ask Codex:

```text
Install this skill:
https://github.com/KeonSuYun/codex-team-orchestrator/tree/main/skills/codex-team-orchestrator
```

Restart Codex after install.

### One-line install

macOS / Linux / WSL:

```bash
curl -fsSL https://raw.githubusercontent.com/KeonSuYun/codex-team-orchestrator/main/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/KeonSuYun/codex-team-orchestrator/main/install.ps1 | iex
```

## Use

```text
Use codex-team-orchestrator for this task. Choose roles yourself.
```

```text
Use codex-team-orchestrator with Product Manager, Frontend Developer, Backend Developer, and Strict User.
```

```text
Use codex-team-orchestrator and ask me which roles to use first.
```

Chinese works too:

```text
使用 codex-team-orchestrator 做这个任务，先问我这次要什么团队角色。
```

## What You Get

- Current conversation acts as Leader by default.
- Leader creates teammates only when useful.
- Teammates are visible Codex project threads.
- New teammates start with `/goal`.
- Role choice can happen through Codex Plan-mode options.
- User can name roles directly in natural language.
- Roster stores teammate thread ids.
- Teammates report through `MESSAGE_TO_LEADER` and `STATUS_PACKET`.
- Leader monitors teammates with `read_thread`.
- Replies use the user's language.

## Role Choice

Priority:

1. Roles named by the user.
2. Codex Plan-mode role choice, when available.
3. Saved role catalog, when requested.
4. Leader chooses the smallest useful team.

Example roles are not fixed. Use whatever fits the task.

## Roster

Rosters are stored under:

```text
$CODEX_HOME/team-rosters/
```

Fallback:

```text
~/.codex/team-rosters/
```

The user does not need to copy thread ids manually.

## Repository Layout

```text
skills/codex-team-orchestrator/              # canonical skill
.codex/skills/codex-team-orchestrator/       # Codex-friendly mirror
plugins/codex-team-orchestrator/             # plugin-style package layout
install.sh
install.ps1
INSTALL.md
LICENSE
```

## Develop

Validate the skill:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/codex-team-orchestrator
```

## License

MIT
