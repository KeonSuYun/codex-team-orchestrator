$ErrorActionPreference = "Stop"

$repoUrl = if ($env:CODEX_TEAM_ORCHESTRATOR_REPO) {
  $env:CODEX_TEAM_ORCHESTRATOR_REPO
} else {
  "https://github.com/KeonSuYun/codex-team-orchestrator.git"
}

$codexHome = if ($env:CODEX_HOME) {
  $env:CODEX_HOME
} else {
  Join-Path $HOME ".codex"
}

$dest = Join-Path $codexHome "skills\codex-team-orchestrator"
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("codex-team-orchestrator-" + [System.Guid]::NewGuid().ToString("N"))

try {
  git clone --depth 1 $repoUrl (Join-Path $tmp "repo") | Out-Null

  if (Test-Path $dest) {
    Remove-Item $dest -Recurse -Force
  }

  New-Item -ItemType Directory -Force (Split-Path -Parent $dest) | Out-Null
  Copy-Item (Join-Path $tmp "repo\skills\codex-team-orchestrator") $dest -Recurse -Force

  Write-Host "Installed codex-team-orchestrator to $dest"
  Write-Host "Restart Codex to pick up the skill."
} finally {
  if (Test-Path $tmp) {
    Remove-Item $tmp -Recurse -Force
  }
}
