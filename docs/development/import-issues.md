# Import issues

The 18 issue files in `docs/issues/` are the source of truth. The import script does not rewrite their content.

PowerShell:

```powershell
.\scripts\import-issues.ps1 -Repo OWNER/REPO
```

If `origin` points to GitHub, `-Repo` can be omitted:

```powershell
.\scripts\import-issues.ps1
```

Bash:

```bash
./scripts/import-issues.sh OWNER/REPO
```
