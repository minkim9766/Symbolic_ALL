$installPath = "$HOME\symbolic-tools"

if (!(Test-Path -Path $installPath)) {
    New-Item -ItemType Directory -Path $installPath | Out-Null
}

Copy-Item -Path ".\symbolic-all.ps1" -Destination "$installPath\symbolic-all.ps1" -Force
Copy-Item -Path ".\symbolic-all-core.psm1" -Destination "$installPath\symbolic-all-core.psm1" -Force

$envPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not ($envPath -split ";" | Where-Object { $_ -eq $installPath })) {
    [Environment]::SetEnvironmentVariable("Path", "$envPath;$installPath", "User")
    Write-Host "▶️ 환경변수 PATH에 추가됨: $installPath"
} else {
    Write-Host "ℹ️ 환경변수 PATH에 이미 등록되어 있습니다."
}

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "`n✅ 설치 완료! 이제 'symbolic-all' 명령을 사용할 수 있습니다."
