@echo off

rem Check for virtual environment
if not exist venv\ (
    echo Virtual environment missing! [Run setup.bat]
    goto exit
)

rem Enter virtual environment
call .\venv\Scripts\activate.bat

rem Run program
python -m app

rem Deactivate virtual environment
deactivate

:exit
@echo on