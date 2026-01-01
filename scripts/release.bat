@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Threads Downloader - Release Script
echo ========================================
echo.

:: Get latest tag
for /f "tokens=*" %%i in ('git describe --tags --abbrev^=0 2^>nul') do set LATEST_TAG=%%i

if "%LATEST_TAG%"=="" (
    set LATEST_TAG=v0.0.0
    echo No existing tags found. Starting from v0.0.0
) else (
    echo Current version: %LATEST_TAG%
)

:: Parse version numbers
set VERSION=%LATEST_TAG:v=%
for /f "tokens=1,2,3 delims=." %%a in ("%VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)

:: Calculate new versions
set /a NEW_MAJOR=%MAJOR%+1
set /a NEW_MINOR=%MINOR%+1
set /a NEW_PATCH=%PATCH%+1

echo.
echo Select action:
echo   [1] Patch  %MAJOR%.%MINOR%.%NEW_PATCH%  (bug fixes)
echo   [2] Minor  %MAJOR%.%NEW_MINOR%.0  (new features)
echo   [3] Major  %NEW_MAJOR%.0.0  (breaking changes)
echo   [4] Custom version
echo   [5] Replace existing tag
echo   [6] Cancel
echo.

set /p CHOICE="Enter choice (1-6): "

if "%CHOICE%"=="1" (
    set NEW_VERSION=%MAJOR%.%MINOR%.%NEW_PATCH%
) else if "%CHOICE%"=="2" (
    set NEW_VERSION=%MAJOR%.%NEW_MINOR%.0
) else if "%CHOICE%"=="3" (
    set NEW_VERSION=%NEW_MAJOR%.0.0
) else if "%CHOICE%"=="4" (
    set /p NEW_VERSION="Enter custom version (e.g., 1.2.3): "
) else if "%CHOICE%"=="5" (
    goto :replace_tag
) else (
    echo Cancelled.
    exit /b 0
)

goto :create_release

:replace_tag
echo.
echo Recent tags (up to 10):
echo.

set TAG_COUNT=0
for /f "tokens=*" %%t in ('git tag --sort^=-creatordate 2^>nul') do (
    if !TAG_COUNT! lss 10 (
        set /a TAG_COUNT+=1
        set "TAG_!TAG_COUNT!=%%t"
        echo   [!TAG_COUNT!] %%t
    )
)

if %TAG_COUNT%==0 (
    echo No tags found.
    exit /b 0
)

echo   [0] Cancel
echo.

set /p TAG_CHOICE="Select tag to replace (0-%TAG_COUNT%): "

if "%TAG_CHOICE%"=="0" (
    echo Cancelled.
    exit /b 0
)

set "SELECTED_TAG=!TAG_%TAG_CHOICE%!"
if "%SELECTED_TAG%"=="" (
    echo Invalid selection.
    exit /b 1
)

set NEW_VERSION=%SELECTED_TAG:v=%

echo.
echo Replacing tag: %SELECTED_TAG%
echo.

set /p CONFIRM="Confirm replace %SELECTED_TAG%? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Cancelled.
    exit /b 0
)

:: Delete local and remote tag
echo Deleting existing tag...
git tag -d %SELECTED_TAG% 2>nul
git push origin --delete %SELECTED_TAG% 2>nul

goto :do_release

:create_release
echo.
echo New version: v%NEW_VERSION%
echo.

set /p CONFIRM="Confirm release v%NEW_VERSION%? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Cancelled.
    exit /b 0
)

:: Update version in pyproject.toml
echo Updating pyproject.toml...
powershell -Command "(Get-Content pyproject.toml) -replace 'version = \"[^\"]+\"', 'version = \"%NEW_VERSION%\"' | Set-Content pyproject.toml"

:: Git operations
echo.
echo Committing changes...
git add -A
git commit -m "chore: bump version to v%NEW_VERSION%"

:do_release
echo Creating tag v%NEW_VERSION%...
git tag -a v%NEW_VERSION% -m "Release v%NEW_VERSION%"

echo Pushing to remote...
git push origin main
git push origin v%NEW_VERSION%

echo.
echo ========================================
echo   Release v%NEW_VERSION% pushed!
echo   GitHub Actions will build binaries.
echo ========================================
pause
