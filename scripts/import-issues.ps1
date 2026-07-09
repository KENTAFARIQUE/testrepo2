param(
    [string]$Repo = "",
    [string]$IssuesDir = "docs/issues"
)

$ErrorActionPreference = "Stop"

function Ok($Text) {
    Write-Host "    [OK] $Text" -ForegroundColor Green
}

function Warn($Text) {
    Write-Host "    [WARN] $Text" -ForegroundColor Yellow
}

function Fail($Text) {
    Write-Host "    [FAIL] $Text" -ForegroundColor Red
    exit 1
}

function Step($Text) {
    Write-Host ""
    Write-Host "==> $Text" -ForegroundColor Cyan
}

function Require-Command($Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        Fail "Command not found: $Name"
    }
}

function Resolve-Repo {
    if ($Repo -and $Repo.Trim().Length -gt 0) {
        return $Repo
    }

    $resolved = gh repo view --json nameWithOwner --jq ".nameWithOwner" 2>$null
    if (-not $resolved) {
        Fail "Could not resolve GitHub repo. Pass -Repo owner/name."
    }

    return $resolved
}

function Get-IssueTitle {
    param([string]$Content, [string]$FileName)

    foreach ($line in ($Content -split "`r?`n")) {
        if ($line -match "^#\s+(.+)$") {
            return $Matches[1].Trim()
        }
    }

    return [System.IO.Path]::GetFileNameWithoutExtension($FileName)
}

function Get-IssueLabels {
    param([string]$Content)

    $labels = @()

    # Format 1:
    # Labels: a, b, c
    foreach ($line in ($Content -split "`r?`n")) {
        if ($line -match "^\s*Labels:\s*(.+)$") {
            $labels += ($Matches[1] -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        }
    }

    # Format 2:
    # ## Labels
    # a, b, c
    $match = [regex]::Match($Content, "(?ms)^##\s+Labels\s*`r?`n(?<labels>.*?)(?=`r?`n##\s+|\z)")
    if ($match.Success) {
        $text = $match.Groups["labels"].Value.Trim()
        $labels += ($text -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    }

    return @($labels | Select-Object -Unique)
}

function Ensure-Label {
    param(
        [string]$RepoName,
        [string]$Label
    )

    if (-not $Label) {
        return
    }

    $labelsJson = gh label list --repo $RepoName --limit 500 --json name 2>$null
    $labels = $labelsJson | ConvertFrom-Json

    foreach ($item in $labels) {
        if ($item.name -eq $Label) {
            return
        }
    }

    $color = "ededed"

    if ($Label -like "agent:*") { $color = "5319e7" }
    elseif ($Label -like "area:*") { $color = "1d76db" }
    elseif ($Label -like "type:*") { $color = "0e8a16" }
    elseif ($Label -like "phase:*") { $color = "fbca04" }
    elseif ($Label -like "priority:*") { $color = "d93f0b" }
    elseif ($Label -eq "ready-for-agent") { $color = "00c853" }
    elseif ($Label -eq "needs-review") { $color = "b60205" }
    elseif ($Label -eq "ci") { $color = "5319e7" }
    elseif ($Label -eq "testing") { $color = "c5def5" }

    gh label create $Label --repo $RepoName --color $color --description "Auto-created by import-issues.ps1" 2>$null | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Ok "Created missing label: $Label"
    } else {
        Warn "Could not create label: $Label"
    }
}

function Issue-Exists {
    param(
        [string]$RepoName,
        [string]$Title
    )

    $all = gh issue list --repo $RepoName --state all --limit 500 --json title | ConvertFrom-Json
    foreach ($issue in $all) {
        if ($issue.title -eq $Title) {
            return $true
        }
    }

    return $false
}

Step "Checking prerequisites"
Require-Command gh

gh auth status 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Fail "gh is not authenticated. Run: gh auth login"
}

if (-not (Test-Path $IssuesDir)) {
    Fail "Issues directory not found: $IssuesDir"
}

$ResolvedRepo = Resolve-Repo
Ok "Prerequisites verified"

Step "Importing issues into $ResolvedRepo"

$files = Get-ChildItem $IssuesDir -Filter "*.md" |
    Where-Object { $_.Name -match "^\d{2}-" } |
    Sort-Object Name

if ($files.Count -eq 0) {
    Fail "No numbered issue files found in $IssuesDir"
}

$created = 0
$skipped = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $title = Get-IssueTitle -Content $content -FileName $file.Name
    $labels = Get-IssueLabels -Content $content

    foreach ($label in $labels) {
        Ensure-Label -RepoName $ResolvedRepo -Label $label
    }

    if (Issue-Exists -RepoName $ResolvedRepo -Title $title) {
        Warn "Issue already exists, skipping: $title"
        $skipped++
        continue
    }

    $args = @(
        "issue", "create",
        "--repo", $ResolvedRepo,
        "--title", $title,
        "--body-file", $file.FullName
    )

    foreach ($label in $labels) {
        $args += @("--label", $label)
    }

    $output = & gh @args 2>&1

    if ($LASTEXITCODE -eq 0) {
        Ok "Created issue: $title"
        $created++
    } else {
        Warn "Failed to create issue: $title"
        Write-Host $output
    }
}

Step "Done"
Write-Host "Created: $created"
Write-Host "Skipped: $skipped"