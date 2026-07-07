<#
TubeDigest bootstrap (safe version)

This script does only the repository bootstrap:
  1. verifies git/gh auth;
  2. initializes git if needed;
  3. creates/updates initial commit;
  4. creates or connects GitHub repo;
  5. pushes main;
  6. syncs labels from .github/labels.yml.

It does NOT create issues and does NOT create worktrees.
Use separately:
  .\scripts\import-issues.ps1
  .\scripts\create-worktrees.ps1
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$RepoName,

    [string]$OrgName = "",

    [ValidateSet("public", "private", "internal")]
    [string]$Visibility = "private",

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSNativeCommandUseErrorActionPreference = $false
}

function Step([string]$Text) { Write-Host "`n==> $Text" -ForegroundColor Cyan }
function Ok([string]$Text) { Write-Host "    [OK] $Text" -ForegroundColor Green }
function Warn([string]$Text) { Write-Host "    [WARN] $Text" -ForegroundColor Yellow }
function Fail([string]$Text) { Write-Host "    [FAIL] $Text" -ForegroundColor Red; exit 1 }

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        Fail "Required command not found: $Name"
    }
}

function Resolve-RepoSlug {
    if ($OrgName -and $OrgName.Trim().Length -gt 0) {
        return "$OrgName/$RepoName"
    }
    $user = gh api user --jq ".login" 2>$null
    if (-not $user) { Fail "Could not resolve GitHub user. Run gh auth login." }
    return "$user/$RepoName"
}

function Ensure-MainBranch {
    if (-not (Test-Path ".git")) {
        git init -b main | Out-Null
        Ok "Initialized git repository on main"
        return
    }

    $current = git branch --show-current 2>$null
    if (-not $current) {
        git checkout -b main | Out-Null
        Ok "Created main branch"
        return
    }

    if ($current -ne "main") {
        Warn "Current branch is '$current'. Switching to main."
        git switch main | Out-Null
    }
    Ok "Git repository ready on main"
}

function Ensure-Commit {
    git add .
    $status = git status --porcelain
    if (-not $status) {
        Ok "No local changes to commit"
        return
    }

    git commit -m "chore: bootstrap tubedigest template" | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Ok "Committed current template state"
    } else {
        Fail "git commit failed. Check git status."
    }
}

function Ensure-GitHubRepoAndPush {
    param([string]$RepoSlug, [string]$Visibility)

    $repoExists = $false
    gh repo view $RepoSlug 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $repoExists = $true }

    if (-not $repoExists) {
        if ($DryRun) {
            Warn "DRY RUN: would create $RepoSlug"
        } else {
            gh repo create $RepoSlug "--$Visibility" | Out-Null
            if ($LASTEXITCODE -ne 0) { Fail "Could not create GitHub repository: $RepoSlug" }
            Ok "Created GitHub repository: $RepoSlug"
        }
    } else {
        Ok "GitHub repository already exists: $RepoSlug"
    }

    $targetRemote = "https://github.com/$RepoSlug.git"
    $origin = git remote get-url origin 2>$null

    if (-not $origin) {
        git remote add origin $targetRemote
        Ok "Added origin remote: $targetRemote"
    } elseif ($origin -ne $targetRemote) {
        Warn "Origin pointed to another repo: $origin"
        git remote set-url origin $targetRemote
        Ok "Updated origin remote: $targetRemote"
    } else {
        Ok "Origin remote already correct"
    }

    if ($DryRun) {
        Warn "DRY RUN: would push main to origin"
        return
    }

    git push -u origin main
    if ($LASTEXITCODE -ne 0) { Fail "git push failed" }
    Ok "Pushed main branch"
}

function Sync-Labels {
    param([string]$RepoSlug)

    if (-not (Test-Path ".github/labels.yml")) {
        Warn ".github/labels.yml not found; skipping labels"
        return
    }

    $content = Get-Content ".github/labels.yml" -Raw
    $matches = [regex]::Matches(
        $content,
        "(?ms)-\s*name:\s*['\"]?(?<name>[^`r`n'\"]+)['\"]?\s*`r?`n\s*color:\s*['\"]?(?<color>[^`r`n'\"]+)['\"]?(?:\s*`r?`n\s*description:\s*['\"]?(?<desc>[^`r`n'\"]*)['\"]?)?"
    )

    if ($matches.Count -eq 0) {
        Warn "No labels parsed from .github/labels.yml"
        return
    }

    foreach ($m in $matches) {
        $name = $m.Groups["name"].Value.Trim()
        $color = $m.Groups["color"].Value.Trim().TrimStart("#")
        $desc = $m.Groups["desc"].Value.Trim()

        if ($DryRun) {
            Write-Host "    [DRY] label $name" -ForegroundColor Gray
            continue
        }

        gh label create $name --repo $RepoSlug --color $color --description $desc --force 2>$null | Out-Null
    }

    Ok "Labels synced: $($matches.Count)"
}

Step "[1/5] Checking prerequisites"
Require-Command git
Require-Command gh
gh auth status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { Fail "GitHub CLI is not authenticated. Run: gh auth login" }
if (-not (Test-Path "AGENTS.md")) { Fail "Run bootstrap from the project root." }
Ok "Prerequisites verified"

$RepoSlug = Resolve-RepoSlug
Step "[2/5] Repository configuration"
Write-Host "    Repository: $RepoSlug"
Write-Host "    Visibility:  $Visibility"

Step "[3/5] Preparing local git"
Ensure-MainBranch
Ensure-Commit

Step "[4/5] Creating/updating GitHub repo"
Ensure-GitHubRepoAndPush -RepoSlug $RepoSlug -Visibility $Visibility

Step "[5/5] Syncing labels"
Sync-Labels -RepoSlug $RepoSlug

Write-Host ""
Write-Host "Bootstrap complete." -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  .\scripts\import-issues.ps1 -Repo $RepoSlug"
Write-Host "  .\scripts\create-worktrees.ps1"
Write-Host ""
