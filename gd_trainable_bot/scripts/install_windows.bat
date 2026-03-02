@echo off
setlocal
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .
echo Instalacion completa. Ejecuta scripts\run_menu.bat
