@echo off
SETLOCAL EnableDelayedExpansion

rem Check if python, pip and virtualenv are installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not installed!
    goto end
)
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo pip not installed!
    goto end
)
where virtualenv >nul 2>nul
if %errorlevel% neq 0 (
    echo virtualenv not installed!
    goto end
)

rem Clear existing virtual environment if any
if exist venv\ (
    call choice /C YN /N /M "Clear existing virtual environemnt? [Y/N]: "
    if !errorlevel! neq 1 (goto end)
    rd /s /q venv\
    ping localhost -n 2 >nul
)

rem Generate and activate virtual environment
echo Generating virtual environment!
python -m virtualenv venv >nul
call .\venv\Scripts\activate.bat

rem Install packages
echo Installing required packages!
pip install -r requirements.txt -U >nul

rem Deactivate virtual environment
call deactivate

:end
If /I Not "%CMDCMDLINE:"=%" == "%COMSPEC%" (
    echo.
    echo Press any key to exit ...
    pause >nul
)
@echo on