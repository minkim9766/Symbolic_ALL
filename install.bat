@echo off
setlocal

:: 다운로드 받을 URL
set "url=https://github.com/minkim9766/Symbolic_ALL/releases/download/Release/exe.win-amd64-3.13.zip"

:: 저장할 파일 이름
set "filename=symbolic-all.zip"

:: 압축을 풀 디렉토리
set "extractDir=C:\Program Files\Symbolic_ALL"

echo [1/2] Downloading files...
powershell -command "Invoke-WebRequest -Uri '%url%' -OutFile '%filename%'"

if exist "%filename%" (
    echo Download complete! %filename%
) else (
    echo Error downloading!
    exit /b 1
)

echo [2/2] Extracting packages...
if not exist "%extractDir%" mkdir "%extractDir%"
powershell -command "Expand-Archive -Path '%filename%' -DestinationPath '%extractDir%' -Force"

echo Installation complete!

setx PATH "%PATH%;%extractDir%"

endlocal
pause