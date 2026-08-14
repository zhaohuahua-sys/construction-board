@echo off
chcp 65001 >nul
title Construction Board Sync
echo ================================================
echo  Construction Board - One Click Sync
echo ================================================
echo.

REM --- Find latest source Excel ---
set "SRC=C:\Users\Administrator.rokin-2025VMFLM\Desktop\Opencode\甘特图-v2"
if not exist "%SRC%" (
  echo [ERROR] Source folder not found: %SRC%
  pause
  exit /b 1
)

set "LATEST="
for /f "delims=" %%f in ('dir /b /o-d "%SRC%\Phase II*.xlsx" 2^>nul') do (
  if not defined LATEST set "LATEST=%%f"
)
if not defined LATEST (
  echo [ERROR] No Phase II *.xlsx found in source folder.
  pause
  exit /b 1
)
echo [1/3] Found latest file: %LATEST%

REM --- Copy to repo data folder ---
set "REPO=C:\Users\Administrator.rokin-2025VMFLM\Desktop\Workbuddy\06-施工看板\.workbuddy\publish"
copy /y "%SRC%\%LATEST%" "%REPO%\data\Phase II 施工总览.xlsx" >nul
if errorlevel 1 (
  echo [ERROR] Copy failed.
  pause
  exit /b 1
)
echo [2/3] Copied to data\Phase II 施工总览.xlsx

REM --- Git push ---
cd /d "%REPO%"
git add -A
git commit -m "sync: %LATEST%"
git push origin main
if errorlevel 1 (
  echo [ERROR] Git push failed. Check network or GitHub login.
  pause
  exit /b 1
)
echo.
echo [3/3] DONE! Web will auto-update within ~1 minute.
echo       URL: https://zhaohuahua-sys.github.io/construction-board/
echo ================================================
pause
