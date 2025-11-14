@echo off
echo 🚀 Creating OnePlus Backup Tool Release Package...
echo.

set VERSION=1.0.0
set RELEASE_DIR=OnePlus_Backup_Tool_v%VERSION%

REM Create release directory
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

REM Copy executable
if exist "dist\OnePlus_Backup_Tool.exe" (
    copy "dist\OnePlus_Backup_Tool.exe" "%RELEASE_DIR%\"
    echo ✅ Executable copied
) else (
    echo ❌ Executable not found! Run build_exe.bat first.
    pause
    exit /b 1
)

REM Create necessary folders
mkdir "%RELEASE_DIR%\backups"

REM Copy documentation
if exist "README_EXECUTABLE.md" (
    copy "README_EXECUTABLE.md" "%RELEASE_DIR%\README.md"
    echo ✅ Documentation copied
)

REM Create ADB installation guide
echo # ADB Setup Guide > "%RELEASE_DIR%\ADB_Setup.md"
echo. >> "%RELEASE_DIR%\ADB_Setup.md"
echo ## Quick ADB Installation >> "%RELEASE_DIR%\ADB_Setup.md"
echo. >> "%RELEASE_DIR%\ADB_Setup.md"
echo 1. **Download Android Platform Tools**: >> "%RELEASE_DIR%\ADB_Setup.md"
echo    - Go to: https://developer.android.com/studio/releases/platform-tools >> "%RELEASE_DIR%\ADB_Setup.md"
echo    - Download "SDK Platform-Tools for Windows" >> "%RELEASE_DIR%\ADB_Setup.md"
echo. >> "%RELEASE_DIR%\ADB_Setup.md"
echo 2. **Extract and Setup**: >> "%RELEASE_DIR%\ADB_Setup.md"
echo    - Extract the zip file >> "%RELEASE_DIR%\ADB_Setup.md"
echo    - Copy `adb.exe` to the same folder as OnePlus_Backup_Tool.exe >> "%RELEASE_DIR%\ADB_Setup.md"
echo    - OR add the platform-tools folder to your system PATH >> "%RELEASE_DIR%\ADB_Setup.md"
echo. >> "%RELEASE_DIR%\ADB_Setup.md"
echo 3. **Enable USB Debugging on your OnePlus device**: >> "%RELEASE_DIR%\ADB_Setup.md"
echo    - Settings ^> Developer Options ^> USB Debugging >> "%RELEASE_DIR%\ADB_Setup.md"
echo    - If Developer Options is hidden: Settings ^> About Phone ^> Tap Build Number 7 times >> "%RELEASE_DIR%\ADB_Setup.md"

REM Create simple usage instructions
echo # OnePlus Backup Tool - Quick Start > "%RELEASE_DIR%\QUICK_START.md"
echo. >> "%RELEASE_DIR%\QUICK_START.md"
echo ## 🚀 How to Use >> "%RELEASE_DIR%\QUICK_START.md"
echo. >> "%RELEASE_DIR%\QUICK_START.md"
echo 1. **Setup ADB** (see ADB_Setup.md) >> "%RELEASE_DIR%\QUICK_START.md"
echo 2. **Connect OnePlus device** via USB >> "%RELEASE_DIR%\QUICK_START.md"
echo 3. **Enable USB Debugging** on device >> "%RELEASE_DIR%\QUICK_START.md"
echo 4. **Run OnePlus_Backup_Tool.exe** >> "%RELEASE_DIR%\QUICK_START.md"
echo 5. **Click "Refresh"** buttons to scan device >> "%RELEASE_DIR%\QUICK_START.md"
echo 6. **Select items** to backup/restore >> "%RELEASE_DIR%\QUICK_START.md"
echo 7. **Click "Backup Selected"** or **"Restore Selected"** >> "%RELEASE_DIR%\QUICK_START.md"
echo. >> "%RELEASE_DIR%\QUICK_START.md"
echo ## 📁 Backups >> "%RELEASE_DIR%\QUICK_START.md"
echo - Saved in `backups` folder >> "%RELEASE_DIR%\QUICK_START.md"
echo - Organized by date and time >> "%RELEASE_DIR%\QUICK_START.md"
echo - Can be moved to external storage >> "%RELEASE_DIR%\QUICK_START.md"

echo.
echo ✅ Release package created: %RELEASE_DIR%\
echo.
echo 📦 Package contents:
dir "%RELEASE_DIR%" /b
echo.
echo 📊 Package size:
for /f "tokens=3" %%a in ('dir "%RELEASE_DIR%" /s ^| find "File(s)"') do echo Files: %%a bytes
echo.
echo 🎯 Ready for distribution!
echo.
pause