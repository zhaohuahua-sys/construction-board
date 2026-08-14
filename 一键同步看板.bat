@echo off
chcp 65001 >nul
title 施工看板 · 一键同步
where node >nul 2>nul
if errorlevel 1 (
  echo [错误] 未找到 Node.js，请先安装 Node.js
  pause
  exit /b 1
)
node "C:\Users\Administrator.rokin-2025VMFLM\Desktop\Workbuddy\06-施工看板\.workbuddy\publish\sync_update.js"
echo.
pause
