@echo off
echo Building OnePlus Backup Tool Executable...
echo.

REM Clean previous build
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build the executable
C:/ProgramData/miniconda3/Scripts/conda.exe run -p C:\ProgramData\miniconda3 --no-capture-output python -m PyInstaller oneplus_backup_tool.spec --clean

echo.
if exist "dist\OnePlus_Backup_Tool.exe" (
    echo ✅ Build completed successfully!
    echo 📁 Executable location: dist\OnePlus_Backup_Tool.exe
    echo.
    echo 📋 File size:
    dir "dist\OnePlus_Backup_Tool.exe" | findstr OnePlus_Backup_Tool.exe
    echo.
    echo 🚀 You can now distribute the OnePlus_Backup_Tool.exe file!
) else (
    echo ❌ Build failed! Check the output above for errors.
)

echo.
pause