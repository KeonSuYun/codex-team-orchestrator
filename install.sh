#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${CODEX_TEAM_ORCHESTRATOR_REPO:-https://github.com/KeonSuYun/codex-team-orchestrator.git}"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
DEST="$CODEX_HOME_DIR/skills/codex-team-orchestrator"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

git clone --depth 1 "$REPO_URL" "$TMP_DIR/repo" >/dev/null

rm -rf "$DEST"
mkdir -p "$(dirname "$DEST")"
cp -R "$TMP_DIR/repo/skills/codex-team-orchestrator" "$DEST"

echo "Installed codex-team-orchestrator to $DEST"
echo "Restart Codex to pick up the skill."
