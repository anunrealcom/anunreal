@echo off
REM ===========================================================================
REM  Godot editor build script (Windows) - ASCII only, PATH-free
REM  Purpose : build the Godot editor exe for Qt Creator / debugging
REM  Requires: Python 3.9+, SCons 4.4+, Visual Studio (MSVC) + Windows SDK
REM  Output  : bin\anunreal.windows.editor.dev.x86_64.exe
REM  Note    : first build is slow (tens of minutes to ~1 hour).
REM            accesskit=no d3d12=no skips two optional deps needing downloads.
REM            To enable them later, run:
REM              python misc\scripts\install_accesskit.py
REM              python misc\scripts\install_d3d12_sdk_windows.py
REM ===========================================================================
setlocal
cd /d "%~dp0"

set "PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
set "SCONS=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\Scripts\scons.exe"
set "SCONSARGS=platform=windows target=editor dev_build=yes accesskit=no d3d12=no"

if not exist "%PY%" (
    echo [ERROR] Python not found: %PY%
    echo         Edit the PY variable in this script to your python.exe path.
    pause
    exit /b 1
)

set JOBS=%NUMBER_OF_PROCESSORS%
if "%JOBS%"=="" set JOBS=4
echo Using -j%JOBS% parallel jobs.

echo.
echo [1/2] Building Godot editor (dev_build, platform=windows) ...
if exist "%SCONS%" (
    "%SCONS%" %SCONSARGS% -j%JOBS%
) else (
    "%PY%" -m SCons %SCONSARGS% -j%JOBS%
)

echo.
if exist bin\anunreal.windows.editor.dev.x86_64.exe (
    echo [OK] Build finished: %CD%\bin\anunreal.windows.editor.dev.x86_64.exe
) else (
    echo [FAIL] exe not generated. Check the scons output above.
)
pause
