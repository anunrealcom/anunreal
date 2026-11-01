@echo off
REM ===========================================================================
REM  Godot compilation database generator (Windows) - ASCII only, PATH-free
REM  Purpose : generate compile_commands.json for Qt Creator / CLion / clangd
REM  Requires: Python 3.9+, SCons 4.4+, Visual Studio (MSVC) + Windows SDK
REM  Usage   : double-click this file
REM  Note    : accesskit=no d3d12=no skips two optional deps needing downloads.
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

echo == Python ==
"%PY%" --version
echo == SCons ==
if exist "%SCONS%" ( "%SCONS%" --version ) else ( "%PY%" -m SCons --version )

echo.
echo [1/2] Generating compile_commands.json ...
if exist "%SCONS%" (
    "%SCONS%" %SCONSARGS% compiledb=yes compiledb_gen_only=yes
) else (
    "%PY%" -m SCons %SCONSARGS% compiledb=yes compiledb_gen_only=yes
)

echo.
if exist compile_commands.json (
    echo [OK] Generated: %CD%\compile_commands.json
) else (
    echo [FAIL] Not generated. Check the scons output above.
)
pause
