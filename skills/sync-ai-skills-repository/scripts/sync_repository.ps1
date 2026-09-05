[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$RepositoryPath,
    [switch]$InspectOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repository = (Resolve-Path -LiteralPath $RepositoryPath).Path
if (-not (Test-Path -LiteralPath (Join-Path $repository '.git'))) {
    throw "Not a Git worktree: '$repository'."
}

$dirty = @(git -C $repository status --porcelain)
if ($LASTEXITCODE -ne 0) { throw "Could not inspect '$repository'." }
if ($dirty.Count -gt 0) {
    throw 'The worktree is dirty. Commit, stash, or discard changes before synchronization.'
}

$upstream = (git -C $repository rev-parse --abbrev-ref '@{upstream}').Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($upstream)) {
    throw 'The current branch has no upstream branch.'
}

git -C $repository fetch --prune | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Could not fetch '$upstream'." }

$counts = ((git -C $repository rev-list --left-right --count "HEAD...$upstream") -split '\s+')
if ($LASTEXITCODE -ne 0 -or $counts.Count -ne 2) {
    throw "Could not compare HEAD with '$upstream'."
}
$ahead = [int]$counts[0]
$behind = [int]$counts[1]

if ($ahead -eq 0 -and $behind -eq 0) {
    Write-Output 'IN_SYNC ahead=0 behind=0'
    return
}
if ($ahead -gt 0 -and $behind -gt 0) {
    throw "Both sides advanced (ahead=$ahead behind=$behind). Resolve the divergence explicitly."
}
if ($ahead -gt 0) {
    Write-Output "LOCAL_AHEAD ahead=$ahead behind=0"
    return
}
if ($InspectOnly) {
    Write-Output "REMOTE_AHEAD ahead=0 behind=$behind"
    return
}

git -C $repository merge --ff-only $upstream | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Could not fast-forward to '$upstream'." }
Write-Output "REMOTE_APPLIED ahead=0 behind=$behind"
