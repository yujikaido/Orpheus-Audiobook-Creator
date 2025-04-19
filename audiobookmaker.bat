@echo off
cd /d "%~dp0"
call conda activate orpheus-audiobook
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
