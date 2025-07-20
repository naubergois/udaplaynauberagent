@echo off
REM Activate the existing Python virtual environment on Windows
IF NOT EXIST .venv\Scripts\activate.bat (
    echo Virtual environment not found. Run setup_windows.bat first.
    exit /b 1
)
call .venv\Scripts\activate
