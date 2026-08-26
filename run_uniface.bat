@echo off
chcp 65001 >nul
echo ===================================================
echo     ▶️ STARTING UNI-FACE
echo ===================================================
echo.
echo Launching Server...
echo.

cd /d "%~dp0"
call conda activate uniface 2>nul || echo [Warning] Conda env 'uniface' not found. Using default python.
python uni-face.py serve

pause
