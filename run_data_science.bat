@echo off
setlocal
title Hostel Data Science Analytics - 25ITC31
color 0E

echo ==============================================================================
echo   HOSTEL STUDENT ACCOMMODATION ANALYSIS - FOUNDATIONS OF DATA SCIENCE
echo   Course Code: 25ITC31 - Python EDA, Statistics and Visualization Suite
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

echo [INFO] Launching Python Data Science Analytics...
echo.
"%PYTHON_EXE%" hostel_data_analysis.py

echo.
echo ==============================================================================
echo [SUCCESS] Data Science Analytics Execution Complete!
echo Charts saved to: %~dp0visualizations
echo Output log saved to: %~dp0data_science_execution_output.txt
echo Screenshot saved to: %~dp0data_science_execution_screenshot.png
echo ==============================================================================
echo.
echo NOTE: This window will remain open so you can view the output.
echo Press any key to close this window, or close it manually.
echo.
pause
cmd /k
