@echo off
setlocal
title Hostel Java Application - 25ITT32
color 0B

echo ==============================================================================
echo   HOSTEL ROOM ALLOCATION SYSTEM - JAVA PROGRAMMING SUITE
echo   Course Code: 25ITT32 - Object-Oriented Application Execution
echo ==============================================================================
echo.

cd /d "%~dp0"

if not exist "bin" mkdir "bin"

echo [STEP 1] Compiling Java Source Files with javac...
javac -encoding UTF-8 -d bin src/com/hostel/model/*.java src/com/hostel/exception/*.java src/com/hostel/service/*.java src/com/hostel/thread/*.java src/com/hostel/Main.java

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Java compilation failed! Please verify that JDK is installed.
    echo.
    pause
    cmd /k
)

echo [SUCCESS] Compilation successful! Class files generated in 'bin' directory.
echo.

echo [STEP 2] Executing Java Main Application Suite...
echo.
java -cp bin com.hostel.Main

echo.
echo ==============================================================================
echo [SUCCESS] Java Application execution complete!
echo Output saved to: %~dp0java_execution_output.txt
echo Screenshot saved to: %~dp0java_execution_screenshot.png
echo ==============================================================================
echo.
echo NOTE: This window will remain open so you can view the output.
echo Press any key to close this window, or close it manually.
echo.
pause
cmd /k
