# Codex Team Orchestrator

Leader-led Codex project-thread teams.

Use one Codex conversation as the Leader. The Leader can ask which roles you want, create visible project-thread teammates, verify task-scoped goals, keep their thread ids in a roster, and route member updates back through the Leader.

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
- When explicitly invoked, Leader announces the team decision before implementation.
- Leader-only is allowed for simple tasks, but Leader must say why no teammate threads are being created.
- If you explicitly ask for a team, multiple agents, members, or Boss role assignment, Leader creates or reuses teammates unless you choose Leader-only.
- Teammates are visible Codex project threads.
- Each teammate assignment uses an explicit `create_goal` / `get_goal` handshake; teammates complete or block goals after reporting results so idle threads do not keep consuming tokens.
- Token-saving keeps briefs compact, but does not remove necessary context, acceptance criteria, dependencies, handoffs, critique, or review.
- Leader keeps the team working like a real team: clear ownership, distinct roles, explicit handoffs, surfaced disagreement, and review before risky integration.
- Role choice can happen through Codex Plan-mode options, including while Goal mode is active.
- User can name roles directly in natural language.
- Roster stores teammate thread ids.
- Teammates report through `MESSAGE_TO_LEADER` and `STATUS_PACKET`.
- Leader monitors teammates with `read_thread`.
- Leader keeps a lightweight task board, uses teammate messages as a mailbox, and tracks statuses such as active, blocked, complete, failed, and goal_unconfirmed.
- Replies use the user's language.

## Goal Control

- Start work by asking the teammate to call `get_goal`, then `create_goal` if needed, then `get_goal` again.
- Treat `get_goal.status=active` as the success signal.
- Pause or wait by asking the teammate to mark its goal `blocked`.
- Resume by asking the teammate to mark the old blocked goal `complete`, then create a new goal.
- Use automations only to wake the Leader for periodic monitoring; automation `ACTIVE/PAUSED` does not pause teammate goals.

## Role Choice

Priority:

1. Roles named by the user.
2. Codex Plan-mode role choice, when available, including inside Goal mode.
3. Saved role catalog, when requested.
4. Leader chooses the smallest useful team.

Example roles are not fixed. Use whatever fits the task.

## 🙏 特别感谢

| 社区 | 说明 |
| --- | --- |
| [LINUX DO](https://linux.do) | [LINUX DO](https://linux.do) - 新的理想型社区。 |

## Roster

Rosters are stored in the project by default:

```text
<project_root>/.codex/team-rosters/
```

Fallback only when there is no project root or the user wants a cross-project team:

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
