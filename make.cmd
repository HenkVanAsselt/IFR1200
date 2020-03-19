@echo off

rem -----------------------------------------------------------------------
rem Check command line parameters
rem -----------------------------------------------------------------------
if "%1"==""   goto usage
if "%1"=="?"  goto usage
if "%1"=="-?" goto usage
if "%1"=="-h" goto usage
if "%1"=="--help" goto usage
goto %1
goto _eof

:clean
rmdir /s /q target
rmdir /s /q scripts
rmdir /s /q Lib
rmdir /s /q Include
rmdir /s /q .pytest_cache
rmdir /s /q __pycache__
rmdir /s /q .idea
del pyvenv.cfg
rmdir /s /q src/.pytest_cache
rmdir /s /q src/__pycache__
rmdir /s /q src/lib
goto _end

:init
python -m pip install --upgrade pip
python -m venv .\venv
call .\venv\Scripts\activate.bat
pip install -r requirements.txt
python -m pip install --upgrade pip
goto _end

:ui2py
REM --- Convert QT Designer UI file to python code.
pyuic5 -x IFR1200_gui.ui -o IFR1200_gui.py
goto _end

:fbs_init
rem --- See https://build-system.fman.io/pyqt-exe-creation/
cd src
fbs startproject
copy *.py .\main\python\
goto _end

:fbs_run
fbs run
goto _end

:fbs_freeze
goto _end

:_end