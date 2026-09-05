$scriptPath = Join-Path $PSScriptRoot '..\scripts\sync_repository.ps1'

Describe 'sync_repository.ps1' {
    BeforeEach {
        $root = Join-Path $TestDrive ([guid]::NewGuid().ToString())
        $remote = Join-Path $root 'remote.git'
        $seed = Join-Path $root 'seed'
        $local = Join-Path $root 'local'

        New-Item -ItemType Directory -Path $root | Out-Null
        git init --bare $remote | Out-Null
        git init -b main $seed | Out-Null
        git -C $seed config user.name 'Test User'
        git -C $seed config user.email 'test@example.com'
        Set-Content -LiteralPath (Join-Path $seed 'SKILL.md') -Value 'initial'
        git -C $seed add SKILL.md
        git -C $seed commit -m 'initial' | Out-Null
        git -C $seed remote add origin $remote
        git -C $seed push -u origin main | Out-Null
        git clone -b main $remote $local | Out-Null
        git -C $local config user.name 'Test User'
        git -C $local config user.email 'test@example.com'
    }

    It 'reports in-sync when both tips match' {
        $result = & $scriptPath -RepositoryPath $local -InspectOnly
        $result | Should Be 'IN_SYNC ahead=0 behind=0'
    }

    It 'reports local-ahead without publishing' {
        Set-Content -LiteralPath (Join-Path $local 'SKILL.md') -Value 'local'
        git -C $local commit -am 'local' | Out-Null

        $result = & $scriptPath -RepositoryPath $local -InspectOnly

        $result | Should Be 'LOCAL_AHEAD ahead=1 behind=0'
        (git -C $remote rev-parse main) | Should Not Be (git -C $local rev-parse HEAD)
    }

    It 'fast-forwards when the remote is ahead' {
        Set-Content -LiteralPath (Join-Path $seed 'SKILL.md') -Value 'remote'
        git -C $seed commit -am 'remote' | Out-Null
        git -C $seed push | Out-Null

        $result = & $scriptPath -RepositoryPath $local

        $result | Should Be 'REMOTE_APPLIED ahead=0 behind=1'
        (git -C $local rev-parse HEAD) | Should Be (git -C $seed rev-parse HEAD)
    }

    It 'stops when both sides advanced' {
        Set-Content -LiteralPath (Join-Path $local 'local.md') -Value 'local'
        git -C $local add local.md
        git -C $local commit -m 'local' | Out-Null
        Set-Content -LiteralPath (Join-Path $seed 'remote.md') -Value 'remote'
        git -C $seed add remote.md
        git -C $seed commit -m 'remote' | Out-Null
        git -C $seed push | Out-Null

        $threw = $false
        try { & $scriptPath -RepositoryPath $local } catch { $threw = $true }
        $threw | Should Be $true
    }

    It 'stops when the worktree is dirty' {
        Set-Content -LiteralPath (Join-Path $local 'SKILL.md') -Value 'dirty'

        $threw = $false
        try { & $scriptPath -RepositoryPath $local } catch { $threw = $true }
        $threw | Should Be $true
    }
}
