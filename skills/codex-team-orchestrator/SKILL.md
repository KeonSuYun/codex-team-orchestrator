---
name: codex-team-orchestrator
description: "Run a lightweight Leader-led Codex team inside the app. Use when the user wants one Codex conversation to coordinate visible teammate project threads, choose or ask for roles, delegate work with verified goal-tool handshakes, store thread ids in a roster, minimize token-heavy cross-thread messages, and communicate in the user's language."
---

# Codex Team Orchestrator

## Defaults

- Treat the current conversation as Leader unless the user asks for a durable Leader thread.
- If this skill is explicitly named by the user, do orchestration first. Do not silently collapse into direct implementation.
- For any explicit orchestrator request, announce a visible team decision before implementation or file edits.
- Leader-only is allowed for simple, low-risk tasks, but only after telling the user why no teammates are being created.
- If the user explicitly asks for a team, multiple agents, members, or Boss role assignment, create or reuse teammates unless the user chooses Leader-only.
- Teammates are normal Codex project threads created with `codex_app.create_thread`.
- Do not use temporary subagents for teammates unless the user explicitly changes the design.
- Use the user's language for replies, teammate prompts, questions, and summaries.
- Store thread ids in the project by default: `<project_root>/.codex/team-rosters/`.
- Use `$CODEX_HOME/team-rosters/` or `C:\Users\<user>\.codex\team-rosters\` only when there is no project root or the user asks for a cross-project team.

## Tools

Use these when available:

- Thread tools: `create_thread`, `send_message_to_thread`, `read_thread`, `list_threads`, `set_thread_title`.
- Choice UI: `request_user_input`, including inside Goal mode when exposed.
- Goal tools in the active thread: `get_goal`, `create_goal`, `update_goal`.
- Automation: `automation_update` only for Leader monitoring or scheduled follow-up.

Do not claim a goal, pause, or automation state was changed unless the relevant tool or target thread reported it.

## Role Selection

Resolve roles in this order:

1. User-named roles.
2. One `request_user_input` role question, if useful and available.
3. Saved role catalog, only when the user asks for reusable/default roles.
4. Leader chooses the smallest useful role set.

If asking with `request_user_input`, use 2-3 choices, put the recommended one first, and write labels in the user's language. If the tool is unavailable, ask the same question in plain text.

When the user explicitly invokes this skill and roles are unclear, prefer a small team choice over Leader-only. For product or coding tasks, a useful default is:

- builder/implementer for changes
- reviewer or QA for critique and acceptance checks
- optional product/design role when requirements or UX are unclear

Leader may still implement final integration, but should not start by doing the whole task alone after an explicit orchestrator request.

## Visible Team Decision

Before implementation or file edits, Leader must send a short user-facing decision:

```text
TEAM_DECISION: Leader-only / teammate team
Reason: ...
Execution: ...
```

Use the user's language. Keep it short.

If choosing Leader-only:

- Say the task is simple or narrow enough for Leader to complete directly.
- Say no teammate threads will be created for this run.
- Continue without asking for extra confirmation unless the user requested role choice or team creation.

If choosing teammates:

- Name the roles and why they exist.
- Create or reuse teammate threads before implementation.
- Save/update the roster.

## Token Budget

- Save tokens by summarizing and referencing, not by hiding information a teammate needs to do good work.
- Send each teammate the minimum complete assignment: role, Leader id, roster ref, objective, task, necessary context, acceptance criteria, dependencies, edit scope, output format.
- Send the full roster only during first identity setup or when the roster changed. Later use `roster_ref` or the roster file path.
- Do not resend full history, role catalogs, old task plans, or long explanations unless a teammate needs them.
- Prefer task deltas: what changed, what to do next, and what to report.
- Read only active or recently messaged teammate threads. Use small reads or latest-turn options when the tool supports them.
- Do not poll completed or blocked teammates unless resuming them.
- Avoid empty keepalive messages. If no work remains, complete or block goals and stop monitoring.
- `MESSAGE_TO_LEADER` should contain only material cross-role information.
- Keep `STATUS_PACKET` compact, preferably one line:
  `role=... status=active|complete|blocked|goal_unconfirmed goal=... blocker=... needs=...`

## Team Model

Use a small team structure instead of long prompts:

- Team record: the roster is the source of truth for Leader, teammates, thread ids, workspace, session notes, and current tasks.
- Task board: Leader tracks only active work items with `id`, `owner`, `status`, `depends_on`, and `handoff_to`.
- Mailbox: teammates send cross-role updates through `MESSAGE_TO_LEADER`; Leader forwards only useful parts to the right teammate.
- Status lifecycle: `pending`, `active`, `blocked`, `complete`, `failed`, `goal_unconfirmed`.
- Shared workspace: teammates work in the same project/root unless Leader explicitly isolates scope.
- Session mode: preserve the current Codex permission/plan/goal posture when possible, but do not assume UI controls can be changed remotely.

Team quality comes from structure, not verbosity:

- Every delegated task needs an owner, objective, necessary context, acceptance criteria, scope, and handoff target when relevant.
- Distinct roles should produce distinct deliverables. Do not flatten all teammates into generic assistants.
- If work is risky or user-facing, assign review or QA before Leader finalizes.
- If roles disagree, Leader keeps the disagreement visible, decides or asks the user, and routes the decision back to teammates.

## Verified Goal Control

- Do not rely on `/goal` text alone as proof of Goal mode.
- Each teammate assignment is a task-scoped goal, not a permanent standby goal.
- Start or resume work by asking the teammate to call `get_goal`; if no active goal exists, call `create_goal`; then call `get_goal` again and report whether `status=active`.
- If goal tools are unavailable or verification fails, use `status=goal_unconfirmed` and continue only as a bounded normal task if Leader accepts that fallback.
- When done, teammate calls `update_goal(status="complete")`, reports once, and stops.
- When paused, blocked, or waiting for input, teammate calls `update_goal(status="blocked")`, reports once, and stops.
- A blocked goal cannot be directly restored to active. To continue, ask the teammate to mark the blocked goal `complete`, create a fresh goal, call `get_goal`, and verify `status=active`.
- Leader should also avoid idling with an active goal when no concrete work remains.

## Compact Teammate Assignment

Use this shape and fill only relevant fields:

```text
You are {ROLE_NAME}. Leader={LEADER_THREAD_ID}. lang={USER_LANGUAGE}. roster={ROSTER_REF}.

Goal check:
1. Call get_goal.
2. If no active goal exists, create_goal("{OBJECTIVE}").
3. Call get_goal again and report goal_status.

Task id: {TASK_ID}
Task: {TASK}
Context: {NECESSARY_CONTEXT}
Acceptance: {ACCEPTANCE_CRITERIA}
Dependencies: {DEPENDENCIES_OR_NONE}
Handoff: {WHO_NEEDS_THIS_NEXT_OR_NONE}
Scope: {EDIT_SCOPE_OR_READ_ONLY}
Constraints: {CONSTRAINTS}

Rules: work only in role; protect user changes; route cross-role info through Leader.

Output:
RESULT: ...
MESSAGE_TO_LEADER: ... (only if needed)
STATUS_PACKET: task=... role=... status=active|complete|blocked|failed|goal_unconfirmed goal=... blocker=... needs=...

Done: update_goal complete and stop. Waiting/paused: update_goal blocked and stop.
```

## Workflow

1. Understand the task and user language.
2. If the user says to set it as a goal, or goal tools are available for concrete work, create or confirm a Leader goal before implementation.
3. Decide whether this is an explicit orchestrator request.
4. Announce the visible team decision.
5. Resolve roles and keep the team minimal.
6. For teammate mode, create/reuse teammates before editing unless the user chose Leader-only.
7. Create new teammate threads only when needed; rename them `<Role Name> - <team_name>`.
8. Send identity once, then send compact task assignments.
9. Save or update the roster after thread creation or role changes.
10. Monitor active teammates, integrate results, route cross-role messages, and resolve conflicts.
11. Review high-risk or user-facing outputs before finalizing.
12. Complete or block idle goals and stop polling when no active delegated work remains.

## Roster

Default roster path:

```text
<project_root>/.codex/team-rosters/{team_name}.json
```

Fallback only when no project root exists or the user wants a cross-project team:

```text
$CODEX_HOME/team-rosters/{team_name}.json
```

Keep rosters small. Suggested shape:

```json
{
  "team_name": "default",
  "project_root": "E:\\Project",
  "leader_thread_id": "current-or-thread-id",
  "monitoring_automation_id": null,
  "role_catalog": {"name": null, "policy": "suggested"},
  "tasks": [
    {"id": "T1", "owner": "role_slug", "status": "active", "depends_on": [], "handoff_to": []}
  ],
  "teammates": {
    "role_slug": {
      "role": "Role Name",
      "thread_id": "...",
      "allowed_to_edit": false,
      "goal_status": "unknown",
      "last_checked_at": null
    }
  }
}
```

## Automation

- Use automation only to wake Leader for monitoring, not to pause or resume teammate goals.
- `automation_update.status` only has `ACTIVE` and `PAUSED`; it controls scheduled runs.
- Default to low-frequency checks, usually 10-30 minutes, for long delegated work.
- Pause or stop the monitoring automation when no teammate has active work.
- Team pause: send block prompts to active teammates, then pause monitoring automation.
- Team resume: reactivate monitoring if needed, then send fresh-goal resume prompts.

## References

- Read `references/role-prompts.md` only when prompt templates are needed.
- Read `references/user-role-catalog.md` only when the user asks for reusable roles or catalogs.

## Safety

- Do not let multiple teammates edit the same files concurrently.
- Keep reviewer, product, strategy, and user-simulator roles read-only unless Leader assigns an edit scope.
- Protect user changes and edits made by other agents.
- Keep teammate threads open unless the user asks to archive them.
