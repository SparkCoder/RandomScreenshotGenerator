@echo off

rem Check for virtual environment
if not exist venv\ (
    echo Virtual environment missing! [Run setup.bat]
    echo.
    echo Press any key to exit ...
    pause >nul
    goto end
)

rem Enter virtual environment
call .\venv\Scripts\activate.bat

rem Run program
python -m app

rem Deactivate virtual environment
call deactivate

:end
@echo on