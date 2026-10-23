@echo off
title Predictor Deportivo IA - Automatizacion Progol
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m src.progol.auto_pipeline %1
pause