@echo off
REM ============================================================
REM  Build PC Autopilot into a Windows .exe with PyInstaller.
REM  Run this on a real Windows machine with Python 3.10-3.12.
REM ============================================================
setlocal enabledelayedexpansion

echo.
echo === PC Autopilot Windows build ===
echo.

REM --- 1. Create / reuse a virtual environment -------------------------
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 goto :error
)
call .venv\Scripts\activate.bat

REM --- 2. Install dependencies (full Windows set) ---------------------
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements-win.txt
python -m pip install pyinstaller pytest
if errorlevel 1 goto :error

REM --- 3. Run the automated tests before packaging -------------------
echo.
echo Running tests...
python -m pytest -q
if errorlevel 1 (
    echo Tests failed -- aborting build.
    goto :error
)

REM --- 4. Clean previous build artifacts -----------------------------
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM --- 5. Package with PyInstaller -----------------------------------
echo.
echo Packaging with PyInstaller...
pyinstaller --clean --noconfirm PCAutopilot.spec
if errorlevel 1 goto :error

echo.
echo === Build complete ===
echo Output: dist\PCAutopilot\PCAutopilot.exe
echo.

REM --- 6. Smoke-test the packaged exe (launch + auto-close) ----------
echo Smoke-testing the packaged executable...
set PCAUTOPILOT_SELFTEST=1
dist\PCAutopilot\PCAutopilot.exe
if errorlevel 1 (
    echo WARNING: packaged exe self-test returned an error code.
) else (
    echo Packaged exe self-test passed.
)
set PCAUTOPILOT_SELFTEST=

goto :eof

:error
echo.
echo BUILD FAILED.
exit /b 1
