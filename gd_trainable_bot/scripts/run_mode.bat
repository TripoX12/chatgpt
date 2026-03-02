@echo off
setlocal
if "%1"=="" (
  echo Uso: scripts\run_mode.bat [calibration^|collect^|training^|play^|stats]
  exit /b 1
)
call .venv\Scripts\activate
gd-bot --mode %1
