[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)][string]$SourcePath,
    [Parameter(Mandatory)][string]$DestinationPath,
    [switch]$PruneStale
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($PruneStale) {
    throw '-PruneStale is incompatible with bidirectional synchronization. Remove a skill explicitly after reviewing both sides.'
}

function Get-DirectorySnapshot {
    param([Parameter(Mandatory)][string]$Path)
    $files = @(Get-ChildItem -LiteralPath $Path -File -Recurse | Sort-Object FullName)
    $entries = @($files | ForEach-Object {
        $relative = $_.FullName.Substring($Path.Length).TrimStart('\', '/')
        "$relative=$((Get-FileHash -LiteralPath $_.FullName).Hash)"
    })
    $latest = if ($files.Count -gt 0) {
        ($files | Measure-Object -Property LastWriteTimeUtc -Maximum).Maximum
    } else {
        (Get-Item -LiteralPath $Path).LastWriteTimeUtc
    }
    [pscustomobject]@{ Digest = $entries -join "`n"; Latest = [datetime]$latest }
}

function Copy-SkillDirectory {
    param(
        [Parameter(Mandatory)][string]$From,
        [Parameter(Mandatory)][string]$To,
        [Parameter(Mandatory)][string]$Direction
    )
    if (-not $PSCmdlet.ShouldProcess($To, "$Direction '$([IO.Path]::GetFileName($From))'")) { return }
    if (Test-Path -LiteralPath $To) { Remove-Item -LiteralPath $To -Recurse -Force }
    New-Item -ItemType Directory -Path $To -Force | Out-Null
    Get-ChildItem -LiteralPath $From -Force | Copy-Item -Destination $To -Recurse -Force
}

$source = (Resolve-Path -LiteralPath $SourcePath).Path
if (-not (Test-Path -LiteralPath $DestinationPath)) {
    if ($PSCmdlet.ShouldProcess($DestinationPath, 'Create synchronization directory')) {
        New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
    }
}
$destination = if (Test-Path -LiteralPath $DestinationPath) {
    (Resolve-Path -LiteralPath $DestinationPath).Path
} else {
    [IO.Path]::GetFullPath($DestinationPath)
}

$sourceDirectories = @(Get-ChildItem -LiteralPath $source -Directory)
$destinationDirectories = if (Test-Path -LiteralPath $destination) { @(Get-ChildItem -LiteralPath $destination -Directory) } else { @() }
$sourceNames = @($sourceDirectories | ForEach-Object { $_.Name })
$destinationNames = @($destinationDirectories | ForEach-Object { $_.Name })
$names = @(($sourceNames + $destinationNames) | Sort-Object -Unique)

foreach ($name in $names) {
    $sourceSkill = Join-Path $source $name
    $destinationSkill = Join-Path $destination $name
    $sourceExists = Test-Path -LiteralPath $sourceSkill
    $destinationExists = Test-Path -LiteralPath $destinationSkill

    if ($sourceExists -and -not $destinationExists) {
        Copy-SkillDirectory -From $sourceSkill -To $destinationSkill -Direction 'COPY SOURCE_TO_DESTINATION'
        Write-Output "SOURCE_TO_DESTINATION $name"
        continue
    }
    if ($destinationExists -and -not $sourceExists) {
        Copy-SkillDirectory -From $destinationSkill -To $sourceSkill -Direction 'COPY DESTINATION_TO_SOURCE'
        Write-Output "DESTINATION_TO_SOURCE $name"
        continue
    }

    $sourceSnapshot = Get-DirectorySnapshot -Path $sourceSkill
    $destinationSnapshot = Get-DirectorySnapshot -Path $destinationSkill
    if ($sourceSnapshot.Digest -eq $destinationSnapshot.Digest) {
        Write-Output "IN_SYNC $name"
    } elseif ($sourceSnapshot.Latest -gt $destinationSnapshot.Latest) {
        Copy-SkillDirectory -From $sourceSkill -To $destinationSkill -Direction 'COPY SOURCE_TO_DESTINATION'
        Write-Output "SOURCE_TO_DESTINATION $name"
    } elseif ($destinationSnapshot.Latest -gt $sourceSnapshot.Latest) {
        Copy-SkillDirectory -From $destinationSkill -To $sourceSkill -Direction 'COPY DESTINATION_TO_SOURCE'
        Write-Output "DESTINATION_TO_SOURCE $name"
    } else {
        throw "Conflict in '$name': content differs but the newest timestamps are equal."
    }
}

if ($WhatIfPreference) { Write-Output 'PREVIEW OK'; return }

foreach ($name in $names) {
    $sourceSnapshot = Get-DirectorySnapshot -Path (Join-Path $source $name)
    $destinationSnapshot = Get-DirectorySnapshot -Path (Join-Path $destination $name)
    if ($sourceSnapshot.Digest -ne $destinationSnapshot.Digest) {
        throw "Verification failed for '$name'."
    }
}
Write-Output 'VERIFY OK'
