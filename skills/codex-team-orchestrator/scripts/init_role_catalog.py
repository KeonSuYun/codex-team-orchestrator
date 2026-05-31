#!/usr/bin/env python3
"""Create or validate Codex Team Orchestrator role catalogs."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


PRESETS: dict[str, dict[str, Any]] = {
    "software-core": {
        "name": "software-core",
        "policy": "suggested",
        "roles": {
            "product_manager": {
                "name": "Product Manager",
                "purpose": "Clarify requirements, scope, acceptance criteria, and tradeoffs.",
                "default_edit": False,
                "when_to_use": "Use for unclear product behavior, UX decisions, and acceptance criteria.",
                "prompt": "Turn vague goals into concrete requirements. Prefer concise acceptance criteria and call out missing product decisions.",
            },
            "frontend_developer": {
                "name": "Frontend Developer",
                "purpose": "Implement UI, interactions, responsive behavior, and visual QA.",
                "default_edit": True,
                "when_to_use": "Use for browser-visible features, layout, styling, and frontend bugs.",
                "prompt": "Follow existing design patterns, verify with screenshots when UI changes, and keep edits scoped.",
            },
            "backend_developer": {
                "name": "Backend Developer",
                "purpose": "Implement APIs, storage, permissions, and server runtime behavior.",
                "default_edit": True,
                "when_to_use": "Use for API contracts, data flow, persistence, auth, and backend bugs.",
                "prompt": "Preserve API compatibility, document contract changes, and add focused tests for risky behavior.",
            },
            "strict_user": {
                "name": "Strict User",
                "purpose": "Review the result as a demanding real user and flag confusing or broken behavior.",
                "default_edit": False,
                "when_to_use": "Use before shipping user-facing workflows or when quality expectations are high.",
                "prompt": "Be blunt about friction, missing states, unclear copy, and incomplete workflows. Produce actionable findings.",
            },
        },
    },
    "strategy-core": {
        "name": "strategy-core",
        "policy": "suggested",
        "roles": {
            "researcher": {
                "name": "Researcher",
                "purpose": "Gather evidence and identify relevant options.",
                "default_edit": False,
                "when_to_use": "Use when facts may have changed, sources matter, or the task needs external evidence.",
                "prompt": "Prefer primary sources, cite evidence, and separate facts from inference.",
            },
            "skeptic": {
                "name": "Skeptic",
                "purpose": "Challenge assumptions, weak plans, and hidden risks.",
                "default_edit": False,
                "when_to_use": "Use when the decision is high-impact, ambiguous, or easy to overfit.",
                "prompt": "Look for missing constraints, failure modes, and claims that need stronger evidence.",
            },
            "operator": {
                "name": "Operator",
                "purpose": "Turn plans into concrete steps, owners, and checks.",
                "default_edit": False,
                "when_to_use": "Use when the user needs execution planning rather than open-ended analysis.",
                "prompt": "Produce practical next actions, dependencies, and verification checks.",
            },
        },
    },
}


def default_codex_home() -> Path:
    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return Path(env_home)
    return Path.home() / ".codex"


def target_path(scope: str, name: str, project_root: str | None, output: str | None) -> Path:
    if output:
        return Path(output)
    if scope == "project":
        root = Path(project_root) if project_root else Path.cwd()
        return root / ".codex" / "team-role-catalog.json"
    return default_codex_home() / "team-role-catalogs" / f"{name}.json"


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(catalog.get("name"), str) or not catalog["name"].strip():
        errors.append("catalog.name must be a non-empty string")
    if catalog.get("policy") not in {"suggested", "locked"}:
        errors.append("catalog.policy must be suggested or locked")
    roles = catalog.get("roles")
    if not isinstance(roles, dict) or not roles:
        errors.append("catalog.roles must be a non-empty object")
        return errors
    for slug, role in roles.items():
        if not isinstance(slug, str) or not slug.strip():
            errors.append("role slugs must be non-empty strings")
        if not isinstance(role, dict):
            errors.append(f"role {slug!r} must be an object")
            continue
        if not isinstance(role.get("name"), str) or not role["name"].strip():
            errors.append(f"role {slug!r}.name must be a non-empty string")
        if not isinstance(role.get("purpose"), str) or not role["purpose"].strip():
            errors.append(f"role {slug!r}.purpose must be a non-empty string")
    return errors


def write_catalog(path: Path, catalog: dict[str, Any], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    errors = validate_catalog(catalog)
    if errors:
        raise SystemExit("Invalid catalog:\n- " + "\n- ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=sorted(PRESETS), default="software-core")
    parser.add_argument("--name", help="Catalog name. Defaults to preset name.")
    parser.add_argument("--policy", choices=["suggested", "locked"], help="Override catalog policy.")
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project-root", help="Project root for --scope project. Defaults to cwd.")
    parser.add_argument("--output", help="Explicit output path.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--validate", help="Validate an existing catalog JSON instead of creating one.")
    args = parser.parse_args()

    if args.validate:
        path = Path(args.validate)
        catalog = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_catalog(catalog)
        if errors:
            raise SystemExit("Invalid catalog:\n- " + "\n- ".join(errors))
        print(f"Catalog is valid: {path}")
        return 0

    catalog = json.loads(json.dumps(PRESETS[args.preset]))
    catalog["name"] = args.name or catalog["name"]
    if args.policy:
        catalog["policy"] = args.policy

    path = target_path(args.scope, catalog["name"], args.project_root, args.output)
    write_catalog(path, catalog, args.overwrite)
    print(f"Wrote role catalog: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
