[CmdletBinding()]
param(
    [string]$RepositoryPath = ".",
    [string[]]$ProtectedBranches = @("main")
)

$repositoryRoot = git -C $RepositoryPath rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0) {
    throw "RepositoryPath is not a Git repository: $RepositoryPath"
}

$gitDirectory = git -C $repositoryRoot rev-parse --git-dir
if ($LASTEXITCODE -ne 0) {
    throw "Unable to resolve the Git directory: $repositoryRoot"
}

if (![System.IO.Path]::IsPathRooted($gitDirectory)) {
    $gitDirectory = Join-Path $repositoryRoot $gitDirectory
}

$hooksDirectory = Join-Path $gitDirectory "hooks"
$hookPath = Join-Path $hooksDirectory "pre-push"
$managedMarker = "# Managed by protect-shared-branches"

if (Test-Path -LiteralPath $hookPath) {
    $existingHook = Get-Content -Raw -LiteralPath $hookPath
    if (!$existingHook.Contains($managedMarker)) {
        throw "A pre-push hook already exists and is not managed by this skill: $hookPath"
    }
}

$patterns = $ProtectedBranches |
    Sort-Object -Unique |
    ForEach-Object { "refs/heads/$($_)" }

$hook = @"
#!/bin/sh
$managedMarker

while read local_ref local_oid remote_ref remote_oid
do
    case "`$remote_ref" in
        $($patterns -join "|") )
            echo "Push rejected: direct updates to a shared branch must go through a pull request." >&2
            exit 1
            ;;
    esac
done

exit 0
"@

New-Item -ItemType Directory -Path $hooksDirectory -Force | Out-Null
[System.IO.File]::WriteAllText(
    $hookPath,
    $hook.Replace("`r`n", "`n"),
    [System.Text.UTF8Encoding]::new($false))

Write-Output $hookPath
