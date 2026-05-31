---
name: codex-team-orchestrator
description: "Run a Leader-led Codex team inside the app. The current conversation acts as Leader by default, can ask the user to choose roles through Codex Plan-mode choices, creates visible project-thread teammates with `/goal`, stores teammate thread ids in a roster, routes member messages through Leader, and uses the user's language."
---

# Codex Team Orchestrator

## Purpose

Use this skill when the user wants a Leader/Boss to split a task across visible Codex project-thread agents.

Default behavior:

- The current conversation is the Leader.
- Start with no teammates.
- Create teammates only when roles, parallel work, review, or long-lived context are useful.
- Teammates must be normal Codex project threads created with `codex_app.create_thread`.
- Every created Leader or teammate thread should start with `/goal`.
- Store thread ids in a roster so the user does not copy ids manually.

## User Experience

Everything happens inside Codex. Do not tell the user to run scripts, edit JSON, copy thread ids, or manually create conversations.

The user can:

- Tell Leader to choose roles.
- Name roles in natural language.
- Ask Leader to show a Codex Plan-mode role choice.
- Define a reusable role catalog in plain language.

Examples:

```text
使用 codex-team-orchestrator 做这个任务，角色你来决定。
使用 codex-team-orchestrator，用产品经理、前端开发、后端开发、严苛用户。
使用 codex-team-orchestrator，先问我这次要什么团队角色。
以后这个项目默认角色池是：产品经理、前端开发、后端开发、严苛用户。策略是 locked。
```

## Language

Use the user's language for all user-facing text, teammate prompts, role-selection questions, status reports, and summaries.

Keep exact identifiers unchanged when needed: file paths, commands, JSON keys, role slugs, thread ids, API names, and code symbols.

## Role Selection

Resolve roles in this order:

1. Roles named by the user in natural language.
2. Codex Plan-mode role choice using `request_user_input`, if available.
3. Saved role catalog, only if the user asks for reusable/preset roles.
4. Leader chooses the smallest useful role set.

If roles are unclear and teammates would help, ask one role-selection question before creating teammates.

When `request_user_input` is available:

- Use one question.
- Put the recommended option first.
- Use 2-3 mutually exclusive options.
- Do not add an `Other` option; Codex adds free-form Other automatically.
- Write labels and descriptions in the user's language.

Suggested choices:

- Leader 自动选择（Recommended）
- 软件小队
- 审查小队

## Required Tools

Use thread tools when available:

- `codex_app.create_thread`
- `codex_app.read_thread`
- `codex_app.send_message_to_thread`
- `codex_app.list_threads`
- `codex_app.set_thread_title`
- `request_user_input` when available in Plan mode
- current Leader goal tools: `get_goal`, `create_goal`, `update_goal`

Do not use `multi_agent_v1.spawn_agent` for teammates unless the user explicitly changes the design.

## Goal Mode

- Current Leader: use `create_goal` if available and no active goal exists.
- New Leader or teammate project threads: initial prompt must begin with `/goal`.
- Existing teammate threads: send a `/goal` follow-up only if they are not already operating under a goal.
- After creating or messaging a `/goal` thread, inspect with `read_thread` when practical.
- If Goal mode cannot be confirmed, continue with the persistent role prompt and tell the user if it matters.

Goal prompt shape:

```text
/goal You are {ROLE_NAME} in a Leader-led Codex team.

Objective: {ROLE_OBJECTIVE}

Leader identity: {LEADER_ID_OR_CURRENT_THREAD}
Your role slug: {ROLE_SLUG}
User language: {USER_LANGUAGE}

{ROLE_PROMPT}
```

## Roster

Store rosters under:

```text
$CODEX_HOME/team-rosters/
```

Fallback:

```text
C:\Users\<user>\.codex\team-rosters\
```

Roster shape:

```json
{
  "team_name": "snake-default",
  "scope": "project",
  "project_root": "E:\\Project",
  "leader_thread_id": "current-thread-or-id",
  "leader_mode": "current_thread_or_durable_thread",
  "role_catalog": {
    "name": "software-core",
    "policy": "suggested",
    "source": "inline-or-path"
  },
  "teammates": {
    "role_slug": {
      "role": "Role Display Name",
      "thread_id": "...",
      "purpose": "Why this role exists",
      "allowed_to_edit": false
    }
  }
}
```

## Workflow

1. Choose operating mode:
   - Direct task: current conversation is Leader.
   - Existing team: reuse or update roster.
   - Durable Leader: create a separate Leader only if the user asks.
2. Resolve project scope. Prefer current project with `target.type = "project"` and `environment.type = "local"`.
3. Resolve roles.
4. Create or update current Leader goal if available.
5. Decide whether teammates are needed.
6. Create only useful teammates with `/goal` project-thread prompts.
7. Rename teammate threads as `<Role Name> - <team_name>`.
8. Save roster.
9. Send each teammate an identity update with its own thread id, Leader id, roster, role rules, and user language.
10. Send narrow tasks to teammates.
11. Monitor teammates with `read_thread`.
12. Integrate results and report concise status to the user.

## Communication

Leader is the router. Teammates do not talk directly to each other.

Every teammate response should include:

```text
MESSAGE_TO_LEADER:
STATUS_PACKET:
```

Leader responses should include useful parts of:

```text
DECISION:
TASKS_TO_SEND:
TEAM_STATUS:
RISKS:
NEXT_STEP:
```

Monitoring rule:

- After sending tasks, check each active teammate with `read_thread`.
- For longer tasks, check again after meaningful progress or when the user asks for status.
- If a teammate needs another teammate to know something, Leader forwards the message.

## Role Catalogs

Role catalogs are optional. Use them only when the user asks for reusable roles or project defaults.

Catalog paths:

- Project: `.codex/team-role-catalog.json`
- User default: `$CODEX_HOME/team-role-catalogs/default.json`
- Team-specific: `$CODEX_HOME/team-role-catalogs/{team_name}.json`

Policies:

- `suggested`: prefer catalog roles, but Leader may add roles when needed.
- `locked`: use only catalog roles unless the user authorizes additions.

See `references/user-role-catalog.md` for schema and examples.

## Prompt Templates

Read `references/role-prompts.md` when creating Leader or teammate prompts.

Use examples there as examples only; roles are not fixed.

## Safety

- Do not let multiple teammates edit the same files concurrently.
- Prefer critique, reviewer, user-simulator, strategy, and product roles as read-only unless Leader explicitly assigns edit scope.
- Protect user changes.
- Keep persistent teammate threads open unless the user asks to archive them.
