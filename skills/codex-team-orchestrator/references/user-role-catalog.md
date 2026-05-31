# User Role Catalogs

Use this reference when the user wants reusable team roles or asks the Leader to choose from roles they configured.

All user-facing explanations about role catalogs should use the user's language. Keep JSON keys, role slugs, paths, and exact identifiers unchanged.

## Purpose

A role catalog is a pool of possible teammates. It is not an instruction to create every role. The Leader still starts Leader-only, decides whether teammates are useful, then selects the smallest useful subset.

Use `policy: "suggested"` for flexible teams. Use `policy: "locked"` when the user wants the Leader to stay inside a fixed set of roles.

## File Locations

Project-local catalog:

```text
<project-root>\.codex\team-role-catalog.json
```

User-level catalogs:

```text
$CODEX_HOME\team-role-catalogs\default.json
$CODEX_HOME\team-role-catalogs\{team_name}.json
```

Fallback when `CODEX_HOME` is unavailable:

```text
C:\Users\<user>\.codex\team-role-catalogs\
```

## Internal Helper Script

Codex may use the bundled script internally for standard catalogs and validation. Do not tell the user to run this script as part of normal use; the user should stay inside Codex and describe the roles in chat or choose through Plan-mode UI.

Available presets:

- `software-core`: Product Manager, Frontend Developer, Backend Developer, Strict User.
- `strategy-core`: Researcher, Skeptic, Operator.

Use `--policy locked` when the Leader must not invent roles outside the catalog. Use `--overwrite` only after confirming the user wants to replace an existing catalog.

User-facing prompts should look like:

```text
我会把这个项目的默认角色池设为：产品经理、前端开发、后端开发、严苛用户；策略为 locked。以后 Leader 会先按这个角色池选择，不需要你手动改文件。
```

## Schema

```json
{
  "name": "software-core",
  "policy": "suggested",
  "roles": {
    "role_slug": {
      "name": "Role Display Name",
      "purpose": "Why this role exists.",
      "default_edit": false,
      "when_to_use": "When Leader should choose this role.",
      "prompt": "Role-specific behavior instructions."
    }
  }
}
```

Required fields:

- `name`
- `policy`
- `roles`
- each role's `name` and `purpose`

Optional fields:

- `default_edit`
- `when_to_use`
- `prompt`
- `model`
- `thread_title`

## Example: Software Team

```json
{
  "name": "software-core",
  "policy": "suggested",
  "roles": {
    "product_manager": {
      "name": "Product Manager",
      "purpose": "Clarify requirements, scope, acceptance criteria, and tradeoffs.",
      "default_edit": false,
      "when_to_use": "Use for unclear product behavior, UX decisions, and acceptance criteria.",
      "prompt": "Turn vague goals into concrete requirements. Prefer concise acceptance criteria and call out missing product decisions."
    },
    "frontend_developer": {
      "name": "Frontend Developer",
      "purpose": "Implement UI, interactions, responsive behavior, and visual QA.",
      "default_edit": true,
      "when_to_use": "Use for browser-visible features, layout, styling, and frontend bugs.",
      "prompt": "Follow existing design patterns, verify with screenshots when UI changes, and keep edits scoped."
    },
    "backend_developer": {
      "name": "Backend Developer",
      "purpose": "Implement APIs, storage, permissions, and server runtime behavior.",
      "default_edit": true,
      "when_to_use": "Use for API contracts, data flow, persistence, auth, and backend bugs.",
      "prompt": "Preserve API compatibility, document contract changes, and add focused tests for risky behavior."
    },
    "strict_user": {
      "name": "Strict User",
      "purpose": "Review the result as a demanding real user and flag confusing or broken behavior.",
      "default_edit": false,
      "when_to_use": "Use before shipping user-facing workflows or when quality expectations are high.",
      "prompt": "Be blunt about friction, missing states, unclear copy, and incomplete workflows. Produce actionable findings."
    }
  }
}
```

## Example: General Strategy Team

```json
{
  "name": "strategy-core",
  "policy": "suggested",
  "roles": {
    "researcher": {
      "name": "Researcher",
      "purpose": "Gather evidence and identify relevant options.",
      "default_edit": false,
      "when_to_use": "Use when facts may have changed, sources matter, or the task needs external evidence.",
      "prompt": "Prefer primary sources, cite evidence, and separate facts from inference."
    },
    "skeptic": {
      "name": "Skeptic",
      "purpose": "Challenge assumptions, weak plans, and hidden risks.",
      "default_edit": false,
      "when_to_use": "Use when the decision is high-impact, ambiguous, or easy to overfit.",
      "prompt": "Look for missing constraints, failure modes, and claims that need stronger evidence."
    },
    "operator": {
      "name": "Operator",
      "purpose": "Turn plans into concrete steps, owners, and checks.",
      "default_edit": false,
      "when_to_use": "Use when the user needs execution planning rather than open-ended analysis.",
      "prompt": "Produce practical next actions, dependencies, and verification checks."
    }
  }
}
```

## Leader Selection Rules

When a catalog is active:

1. List the relevant catalog roles in `TEAM_PLAN`.
2. Select only roles that clearly help the current task.
3. Do not create every role by default.
4. In `suggested` policy, invent non-catalog roles only when the catalog lacks an important capability.
5. In `locked` policy, ask the user before using any non-catalog role.
6. If the user explicitly names roles for the task, that instruction overrides automatic selection.
