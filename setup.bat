@echo off

rem Clear existing virtual environment if any
if exist venv\ (
    echo Clearing existing virtual environemnt!
    rd /s /q venv\
    ping localhost -n 2 >nul
)

rem Generate and activate virtual environment
echo Generating virtual environment!
virtualenv venv >nul
call .\venv\Scripts\activate.bat

rem Install packages
echo Installing required packages!
pip install -r requirements.txt -U >nul

rem Deactivate virtual environment
deactivate

@echo on