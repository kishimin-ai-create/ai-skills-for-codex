[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [string]$SourcePath,

    [Parameter(Mandatory)]
    [string]$DestinationPath,

    [switch]$PruneStale
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$source = (Resolve-Path -LiteralPath $SourcePath).Path
$performedAction = $false
if (-not (Test-Path -LiteralPath $DestinationPath)) {
    if ($PSCmdlet.ShouldProcess($DestinationPath, 'Create destination skills directory')) {
        New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
        $performedAction = $true
    }
}

$skillDirectories = @(Get-ChildItem -LiteralPath $source -Directory)
$destinationDirectories = if (Test-Path -LiteralPath $DestinationPath) {
    @(Get-ChildItem -LiteralPath $DestinationPath -Directory)
} else {
    @()
}

foreach ($skillDirectory in $skillDirectories) {
    $target = Join-Path $DestinationPath $skillDirectory.Name
    if ($PSCmdlet.ShouldProcess($target, "Copy skill '$($skillDirectory.Name)'")) {
        New-Item -ItemType Directory -Path $target -Force | Out-Null
        Get-ChildItem -LiteralPath $skillDirectory.FullName -Force | Copy-Item -Destination $target -Recurse -Force
        $performedAction = $true
    }
    Write-Output "SYNC $($skillDirectory.Name)"
}

if ($PruneStale) {
    $sourceNames = @($skillDirectories.Name)
    foreach ($destinationDirectory in $destinationDirectories) {
        if ($destinationDirectory.Name -notin $sourceNames) {
            if ($PSCmdlet.ShouldProcess($destinationDirectory.FullName, "Remove stale skill '$($destinationDirectory.Name)'")) {
                Remove-Item -LiteralPath $destinationDirectory.FullName -Recurse -Force
                $performedAction = $true
            }
            Write-Output "PRUNE $($destinationDirectory.Name)"
        }
    }
}

$sourceFiles = @(Get-ChildItem -LiteralPath $source -File -Recurse | ForEach-Object {
    $_.FullName.Substring($source.Length).TrimStart('\')
})
$destinationFiles = if (Test-Path -LiteralPath $DestinationPath) {
    @(Get-ChildItem -LiteralPath $DestinationPath -File -Recurse | ForEach-Object {
        $_.FullName.Substring($DestinationPath.Length).TrimStart('\')
    })
} else {
    @()
}

$missing = @($sourceFiles | Where-Object { $_ -notin $destinationFiles })
$extra = @()
if ($PruneStale) {
    $extra = @($destinationFiles | Where-Object { $_ -notin $sourceFiles })
}

if ($performedAction -and ($missing.Count -gt 0 -or $extra.Count -gt 0)) {
    throw "Verification failed. Missing: $($missing -join ', '); Extra: $($extra -join ', ')"
}

if ($performedAction) {
    foreach ($relativePath in $sourceFiles) {
        $sourceFile = Join-Path $source $relativePath
        $destinationFile = Join-Path $DestinationPath $relativePath
        $sourceHash = (Get-FileHash -LiteralPath $sourceFile).Hash
        $destinationHash = (Get-FileHash -LiteralPath $destinationFile).Hash
        if ($sourceHash -ne $destinationHash) {
            throw "Verification failed for '$relativePath'."
        }
    }
}

if (-not $performedAction) {
    Write-Output 'PREVIEW OK'
} else {
    Write-Output 'VERIFY OK'
}
