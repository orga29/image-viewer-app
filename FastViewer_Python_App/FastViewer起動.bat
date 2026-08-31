@echo off
cd /d "%~dp0"
start "" "d:\NextCloud\AI-workroom\.venv\Scripts\pythonw.exe" "%~dp0main.py" "%~1"
