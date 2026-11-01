@echo off
REM ===========================================================================
REM  Godot editor DEV build (FULL / all modules) - ASCII only, PATH-free
REM  Purpose : full-featured editor build for debugging the engine + game code.
REM            Enables every module. Only ANGLE / D3D12 / accesskit are kept off
REM            because their external dependencies are NOT installed on this box;
REM            Vulkan remains the default rendering backend.
REM            To enable them later, run the install scripts below, then remove
REM            the corresponding `=no` flag:
REM              python misc\scripts\install_accesskit.py
REM              python misc\scripts\install_d3d12_sdk_windows.py
REM              python misc\scripts\install_angle.py
REM  Requires: Python 3.9+, SCons 4.4+, Visual Studio (MSVC) + Windows SDK
REM  Output  : bin\anunreal.windows.editor.dev.x86_64.exe
REM  Note    : first build is slow (tens of minutes to ~1 hour).
REM ===========================================================================
setlocal
cd /d "%~dp0"

set "PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
set "SCONS=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\Scripts\scons.exe"
set "SCONSARGS=platform=windows target=editor dev_build=yes accesskit=no d3d12=no angle=no"

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
echo [1/2] Building full Godot editor (all modules) ...
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
