@echo off
setlocal enabledelayedexpansion

REM Check for venv directory
if exist "venv" (
    call conda activate ./venv
) else (
    echo No venv directory found. Exiting.
    pause
    exit /b 1
)

set "urls="

:input_loop
set "url="
set /p url=Enter Threads profile URL (press Enter to finish): 
if "%url%"=="" goto run
set "urls=!urls! %url%"
goto input_loop

:run
threads-downloader --profile %urls%

echo Download completed. Press Enter to exit.
pause >nul