@echo off
setlocal enabledelayedexpansion

REM Initialize conda for shell usage and activate the environment
call conda activate ./venv

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