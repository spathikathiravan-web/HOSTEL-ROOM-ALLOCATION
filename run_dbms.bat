@echo off
setlocal
title Hostel DBMS Execution - 25ITT31
color 0A

echo ==============================================================================
echo   HOSTEL ROOM ALLOCATION SYSTEM - DATABASE MANAGEMENT SYSTEM (DBMS)
echo   Course Code: 25ITT31 - Execution and Verification Suite
echo ==============================================================================
echo.

cd /d "%~dp0"

set "PYTHON_EXE=D:\python_env\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=py -3.12"
    ) else (
        where python >nul 2>nul
        if %errorlevel% equ 0 (
            set "PYTHON_EXE=python"
        ) else (
            set "PYTHON_EXE=C:\Users\oviya\AppData\Local\Programs\Python\Python312\python.exe"
        )
    )
)

echo [INFO] Running DBMS SQL Query Suite...
echo.
"%PYTHON_EXE%" run_dbms.py

echo.
echo ==============================================================================
echo [SUCCESS] DBMS Script execution complete!
echo Output saved to: %~dp0dbms_execution_output.txt
echo Screenshot saved to: %~dp0dbms_execution_screenshot.png
echo ==============================================================================
echo.
echo NOTE: This window will remain open so you can view the output.
echo Press any key to close this window, or close it manually.
echo.
pause
cmd /k
