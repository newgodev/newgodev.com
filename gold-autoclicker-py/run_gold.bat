@echo off
cd /d "%~dp0"
pythonw "%~dp0gold_autoclicker.py"
if errorlevel 1 python "%~dp0gold_autoclicker.py"
