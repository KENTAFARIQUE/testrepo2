<#
Import TubeDigest issues from docs/issues/*.md.

This script intentionally does only one thing: create GitHub Issues from the
existing issue markdown files. It does not create repositories, push code,
create worktrees, or edit issue contents.

Usage:
  .\scripts\import-issues.ps1 -Repo KENTAFARIQUE/testrepo
  .\scripts\import-issues.ps1

When -Repo is omitted, the script uses the current repository's GitHub remote.
#>

param(
    [string]$Repo = "",
    [switch]$DryRun
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

function Resolve-RepoSlug {
    param([string]$Repo)

    if ($Repo -and $Repo.Trim().Length -gt 0) {
        return $Repo.Trim()
    }

    $origin = git remote get-url origin 2>$null
    if (-not $origin) {
        Fail "Could not resolve repo. Pass -Repo owner/name or configure origin."
    }

    if ($origin -match "github.com[:/](?<owner>[^/]+)/(?<name>[^/.]+)(\.git)?$") {
        return "$($Matches.owner)/$($Matches.name)"
    }

    Fail "Origin remote is not a GitHub repository: $origin"
}

function Get-IssueTitle {
    param([string]$Content, [string]$Fallback)

    foreach ($line in ($Content -split "`r?`n")) {
        $trimmed = $line.Trim()
        if ($trimmed -match "^#{1,2}\s+(.+)$") {
            return $Matches[1].Trim()
        }
    }

    return $Fallback
}

function Get-IssueLabels {
    param([string]$Content)

    $labels = @()
    $match = [regex]::Match($Content, "(?ms)^## Labels\s*`r?`n(.+?)(?=`r?`n##\s|\z)")
    if ($match.Success) {
        $labelText = $match.Groups[1].Value -replace "`r", "" -replace "`n", " "
        $labels = $labelText -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    }
    return @($labels)
}

function Issue-Exists {
    param([string]$RepoSlug, [string]$Title)

    $issues = gh issue list --repo $RepoSlug --state all --limit 300 --json title 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $issues) { return $false }

    $parsed = $issues | ConvertFrom-Json
    foreach ($issue in $parsed) {
        if ($issue.title -eq $Title) { return $true }
    }
    return $false
}

Step "Checking prerequisites"
Require-Command git
Require-Command gh
if (-not (Test-Path "docs/issues")) { Fail "docs/issues not found. Run from project root." }
Ok "Prerequisites verified"

$RepoSlug = Resolve-RepoSlug -Repo $Repo
Step "Importing issues into $RepoSlug"

$issueFiles = Get-ChildItem "docs/issues" -Filter "*.md" |
    Where-Object { $_.Name -match "^\d{2}-" } |
    Sort-Object Name

if ($issueFiles.Count -eq 0) { Fail "No numbered issue files found in docs/issues." }

$created = 0
$skipped = 0

foreach ($file in $issueFiles) {
    $content = Get-Content $file.FullName -Raw
    $title = Get-IssueTitle -Content $content -Fallback ([System.IO.Path]::GetFileNameWithoutExtension($file.Name))
    $labels = Get-IssueLabels -Content $content

    if (Issue-Exists -RepoSlug $RepoSlug -Title $title) {
        Warn "Issue already exists: $title"
        $skipped++
        continue
    }

    if ($DryRun) {
        Write-Host "    [DRY] $title" -ForegroundColor Gray
        if ($labels.Count -gt 0) { Write-Host "          labels: $($labels -join ', ')" -ForegroundColor Gray }
        continue
    }

    $args = @("issue", "create", "--repo", $RepoSlug, "--title", $title, "--body-file", $file.FullName)
    foreach ($label in $labels) {
        $args += @("--label", $label)
    }

    $output = & gh @args 2>&1
    if ($LASTEXITCODE -eq 0) {
        Ok "Created issue: $title"
        $created++
    } else {
        Warn "Failed to create issue '$title': $output"
    }
}

Step "Summary"
Ok "Created: $created"
Ok "Skipped: $skipped"
Write-Host ""
Write-Host "Check:" -ForegroundColor Cyan
Write-Host "  gh issue list --repo $RepoSlug"
