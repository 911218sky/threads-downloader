@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Threads Downloader - Setup Script
echo ========================================
echo.

:: Check if conda is installed
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Conda is not installed.
    echo.
    set /p INSTALL_CONDA="Would you like to install Miniconda? (y/n): "
    if /i "!INSTALL_CONDA!"=="y" (
        echo.
        echo Downloading Miniconda installer...
        
        :: Download Miniconda
        powershell -Command "Invoke-WebRequest -Uri 'https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe' -OutFile 'miniconda_installer.exe'"
        
        if exist "miniconda_installer.exe" (
            echo Installing Miniconda...
            start /wait "" miniconda_installer.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
            del miniconda_installer.exe
            
            :: Add conda to PATH for this session
            set "PATH=%UserProfile%\Miniconda3;%UserProfile%\Miniconda3\Scripts;%UserProfile%\Miniconda3\Library\bin;%PATH%"
            
            echo.
            echo [OK] Miniconda installed successfully!
            echo [!] Please restart your terminal and run this script again.
            pause
            exit /b 0
        ) else (
            echo [ERROR] Failed to download Miniconda installer.
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Setup cancelled. Please install Conda manually:
        echo   https://docs.conda.io/en/latest/miniconda.html
        pause
        exit /b 1
    )
)

echo [OK] Conda found: 
conda --version
echo.

:: Check if venv exists
if exist "venv" (
    echo [OK] Virtual environment found.
    set /p RECREATE="Recreate virtual environment? (y/n): "
    if /i "!RECREATE!"=="y" (
        echo Removing existing venv...
        rmdir /s /q venv
    ) else (
        goto :activate
    )
)

:: Create virtual environment
echo.
echo Creating virtual environment with Python 3.12...
call conda create -p venv python=3.12 -y
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

:activate
echo.
echo Activating virtual environment...
call conda activate ./venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: Install package in editable mode
echo.
echo Installing package in editable mode...
pip install -e .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install package.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Setup completed successfully!
echo ========================================
echo.
echo To start using Threads Downloader:
echo   1. Run: conda activate ./venv
echo   2. Run: threads-downloader --help
echo.
echo Or simply run: start.bat
echo.
pause
