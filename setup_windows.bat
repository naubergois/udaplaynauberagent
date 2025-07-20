@echo off
REM Setup Python virtual environment for UdaPlay project on Windows
python -m venv .venv
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment.
    exit /b 1
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies.
    exit /b 1
)
echo.
echo Setup complete. Activate the environment with:
echo   call .venv\Scripts\activate
