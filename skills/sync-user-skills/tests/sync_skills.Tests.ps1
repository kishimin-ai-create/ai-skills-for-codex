$scriptPath = Join-Path $PSScriptRoot '..\scripts\sync_skills.ps1'

Describe 'sync_skills.ps1 bidirectional synchronization' {
    BeforeEach {
        $root = Join-Path $TestDrive ([guid]::NewGuid().ToString())
        $left = Join-Path $root 'left'
        $right = Join-Path $root 'right'
        New-Item -ItemType Directory -Path $left, $right | Out-Null
    }

    It 'copies a source-only skill to the destination' {
        New-Item -ItemType Directory -Path (Join-Path $left 'alpha') | Out-Null
        Set-Content -LiteralPath (Join-Path $left 'alpha\SKILL.md') -Value 'alpha'

        & $scriptPath -SourcePath $left -DestinationPath $right

        Get-Content -Raw -LiteralPath (Join-Path $right 'alpha\SKILL.md') | Should Be (Get-Content -Raw -LiteralPath (Join-Path $left 'alpha\SKILL.md'))
    }

    It 'copies a destination-only skill back to the source' {
        New-Item -ItemType Directory -Path (Join-Path $right 'beta') | Out-Null
        Set-Content -LiteralPath (Join-Path $right 'beta\SKILL.md') -Value 'beta'

        & $scriptPath -SourcePath $left -DestinationPath $right

        Test-Path -LiteralPath (Join-Path $left 'beta\SKILL.md') | Should Be $true
    }

    It 'uses the recursively newer skill directory' {
        New-Item -ItemType Directory -Path (Join-Path $left 'gamma'), (Join-Path $right 'gamma') | Out-Null
        Set-Content -LiteralPath (Join-Path $left 'gamma\SKILL.md') -Value 'older'
        Set-Content -LiteralPath (Join-Path $right 'gamma\SKILL.md') -Value 'newer'
        (Get-Item -LiteralPath (Join-Path $left 'gamma\SKILL.md')).LastWriteTimeUtc = [datetime]'2026-01-01T00:00:00Z'
        (Get-Item -LiteralPath (Join-Path $right 'gamma\SKILL.md')).LastWriteTimeUtc = [datetime]'2026-01-02T00:00:00Z'

        & $scriptPath -SourcePath $left -DestinationPath $right

        (Get-Content -Raw -LiteralPath (Join-Path $left 'gamma\SKILL.md')).Trim() | Should Be 'newer'
    }

    It 'stops on equal timestamps with different content' {
        New-Item -ItemType Directory -Path (Join-Path $left 'delta'), (Join-Path $right 'delta') | Out-Null
        Set-Content -LiteralPath (Join-Path $left 'delta\SKILL.md') -Value 'left'
        Set-Content -LiteralPath (Join-Path $right 'delta\SKILL.md') -Value 'right'
        $same = [datetime]'2026-01-01T00:00:00Z'
        (Get-Item -LiteralPath (Join-Path $left 'delta\SKILL.md')).LastWriteTimeUtc = $same
        (Get-Item -LiteralPath (Join-Path $right 'delta\SKILL.md')).LastWriteTimeUtc = $same

        { & $scriptPath -SourcePath $left -DestinationPath $right } | Should Throw
    }
}
