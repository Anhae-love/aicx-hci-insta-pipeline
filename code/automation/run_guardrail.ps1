<#
    사람 부재 가드레일 러너 — 매일 저녁(기본 21:00) 작업 스케줄러가 호출한다.

      .\run_guardrail.ps1                   마감 21:00 기준으로 만료 처리
      .\run_guardrail.ps1 -Deadline 21:00
      .\run_guardrail.ps1 -DryRun           바꾸지 않고 대상만 로그에 남김

    오늘까지의 콘텐츠 중 21시까지 사람이 승인/반려하지 않은 것을
    expired_no_review 로 보류 처리하고(기획실 측정 루프에 기록), 대시보드에 반영한다.
#>
[CmdletBinding()]
param(
    [string] $Deadline = '21:00',
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path   # …/code/automation
$CodeRoot = Split-Path -Parent $Here
if ((Split-Path -Leaf $CodeRoot) -eq 'code') {
    $Root = Split-Path -Parent $CodeRoot
} else {
    $Root = $CodeRoot
}
$DataRoot = Join-Path $Root 'data'
if (-not (Test-Path $DataRoot) -and (Test-Path (Join-Path $Root 'output'))) { $DataRoot = $Root }
$LogDir = Join-Path $DataRoot 'logs'
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Force -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir ((Get-Date -Format 'yyyy-MM-dd') + '.log')

function Write-Log { param([string]$m,[string]$lv='INFO')
    $line = '[{0}] {1,-5} {2}' -f (Get-Date -Format 'HH:mm:ss'), $lv, $m
    Add-Content -Path $Log -Value $line -Encoding utf8; Write-Host $line
}

$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $py) { Write-Log 'python 을 찾을 수 없다' 'ERROR'; exit 1 }

Write-Log "가드레일 시작 (마감 $Deadline, DryRun=$DryRun)"
$args = @((Join-Path $Here 'guardrail.py'), '--deadline', $Deadline)
if ($DryRun) { $args += '--dry-run' }

& $py @args 2>&1 | ForEach-Object { Write-Log "  $_" }
$code = $LASTEXITCODE
Write-Log "가드레일 종료 exit=$code"

# exit 2 = 만료 처리한 항목이 있다 → manifest 갱신 + push
if ($code -eq 2 -and -not $DryRun) {
    try {
        if (Test-Path (Join-Path $Root '.git')) {
            & $py (Join-Path $Here 'build_manifest.py') $Root (Join-Path $Root 'docs') 2>&1 |
                ForEach-Object { Write-Log "  $_" }
            Push-Location $Root
            try {
                git add docs data 2>&1 | Out-Null
                if ((git status --porcelain docs data) -join '') {
                    git commit -m ("auto: " + (Get-Date -Format 'yyyy-MM-dd') + " 가드레일 보류") 2>&1 |
                        ForEach-Object { Write-Log "  git: $_" }
                    git push 2>&1 | ForEach-Object { Write-Log "  git: $_" }
                    Write-Log '가드레일 결과 push 완료'
                }
            } finally { Pop-Location }
        }
    } catch {
        Write-Log "가드레일 push 실패: $($_.Exception.Message)" 'WARN'
    }
}
exit 0
