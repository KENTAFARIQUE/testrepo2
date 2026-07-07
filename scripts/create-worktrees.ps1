<#
Create git worktrees for parallel agent development.

Usage:
  .\scripts\create-worktrees.ps1
  .\scripts\create-worktrees.ps1 -BaseBranch main
  .\scripts\create-worktrees.ps1 -ParentDir ..\workspaces

By default, worktrees are created next to the current repository folder:
  ../tubedigest-backend
  ../tubedigest-frontend
  ...
#>

param(
    [string]$ConfigPath = "worktrees.json",
    [string]$BaseBranch = "main",
    [string]$ParentDir = ""
)

$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSNativeCommandUseErrorActionPreference = $false
}

function Ok([string]$Text) { Write-Host "    [OK] $Text" -ForegroundColor Green }
function Warn([string]$Text) { Write-Host "    [WARN] $Text" -ForegroundColor Yellow }
function Fail([string]$Text) { Write-Host "    [FAIL] $Text" -ForegroundColor Red; exit 1 }
function Step([string]$Text) { Write-Host "`n==> $Text" -ForegroundColor Cyan }

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        Fail "Required command not found: $Name"
    }
}

function Load-WorktreeConfig {
    param([string]$Path)

    if (-not (Test-Path $Path)) { Fail "Worktree config not found: $Path" }
    $json = Get-Content $Path -Raw | ConvertFrom-Json
    if ($null -ne $json.worktrees) { return @($json.worktrees) }
    return @($json)
}

Step "Checking prerequisites"
Require-Command git
if (-not (Test-Path ".git")) { Fail "Run this script from the main repository checkout." }
Ok "git repository detected"

$root = (Get-Location).Path
if (-not $ParentDir -or $ParentDir.Trim().Length -eq 0) {
    $ParentDir = Split-Path $root -Parent
} else {
    $ParentDir = (Resolve-Path $ParentDir).Path
}

$items = Load-WorktreeConfig -Path $ConfigPath
if ($items.Count -eq 0) { Fail "No worktrees configured in $ConfigPath" }

Step "Creating worktrees"
Write-Host "    Parent: $ParentDir" -ForegroundColor Gray
Write-Host "    Base:   $BaseBranch" -ForegroundColor Gray

# Make sure base branch exists locally.
git rev-parse --verify $BaseBranch 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Fail "Base branch not found locally: $BaseBranch"
}

foreach ($item in $items) {
    $suffix = $item.path_suffix
    if (-not $suffix) { $suffix = $item.key }
    $branch = $item.branch

    if (-not $suffix -or -not $branch) {
        Warn "Invalid item in $ConfigPath. Expected path_suffix/key and branch."
        continue
    }

    $path = Join-Path $ParentDir "tubedigest-$suffix"

    if (Test-Path $path) {
        Warn "Path already exists, skipping: $path"
        continue
    }

    $branchExists = git branch --list $branch
    if ($branchExists) {
        git worktree add $path $branch | Out-Null
    } else {
        git worktree add -b $branch $path $BaseBranch | Out-Null
    }

    Ok "Created $path -> $branch"
}

Step "Summary"
Write-Host "Open these folders in separate VS Code windows:" -ForegroundColor Cyan
foreach ($item in $items) {
    $suffix = $item.path_suffix
    if (-not $suffix) { $suffix = $item.key }
    if ($suffix) {
        Write-Host "  $(Join-Path $ParentDir "tubedigest-$suffix")"
    }
}
Write-Host ""
Write-Host "Control/main folder:" -ForegroundColor Cyan
Write-Host "  $root"
Write-Host ""
Write-Host "Check:" -ForegroundColor Cyan
Write-Host "  git worktree list"
