@echo off

rem Check for virtual environment
if not exist venv\ (
    echo Virtual environment missing! [Run setup.bat]
    goto end
)

rem Enter virtual environment
call .\venv\Scripts\activate.bat

rem Run program
python -m app

rem Deactivate virtual environment
deactivate

:end
@echo on