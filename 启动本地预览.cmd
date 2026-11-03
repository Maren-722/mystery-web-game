@echo off
setlocal
cd /d "%~dp0"
set "nq_node=node"
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" set "nq_node=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
if not exist "node_modules\vite\bin\vite.js" (
  echo Run npm ci in this folder first.
  pause
  exit /b 1
)
if not exist "dist\index.html" (
  echo Run npm run build in this folder first.
  pause
  exit /b 1
)
"%nq_node%" "node_modules\vite\bin\vite.js" preview --host 127.0.0.1 --port 5174 --open
