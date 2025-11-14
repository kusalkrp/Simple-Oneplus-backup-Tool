# OnePlus Backup Tool - Executable Build

## 📦 Creating Executable

Your OnePlus Backup Tool has been successfully converted to a standalone executable!

### ✅ What's Been Done

1. **PyInstaller Installed**: Used to convert Python script to executable
2. **Spec File Created**: `oneplus_backup_tool.spec` for build configuration
3. **Executable Built**: `dist/OnePlus_Backup_Tool.exe` - Ready to use!
4. **Build Script**: `build_exe.bat` for easy rebuilding

### 🚀 Using the Executable

#### **Option 1: Direct Use**
- Navigate to: `C:\Users\ganee\Desktop\Backup tool\dist\`
- Double-click: `OnePlus_Backup_Tool.exe`
- The tool will run without needing Python installed!

#### **Option 2: Distribute**
- Copy `OnePlus_Backup_Tool.exe` to any Windows computer
- No Python installation required on target machine
- All dependencies are bundled inside the executable

### 🔧 Prerequisites for Target Machine

- **Windows OS**: Windows 7/8/10/11
- **ADB Access**: Android Debug Bridge must be available
  - Either install Android SDK Platform Tools
  - Or place `adb.exe` in the same folder as the executable
- **Android Device**: 
  - USB Debugging enabled
  - Device connected via USB

### 📁 File Structure After Build

```
Backup tool/
├── oneplus_sdcard_backup_tool_final.py  # Original Python script
├── oneplus_backup_tool.spec             # PyInstaller configuration
├── build_exe.bat                        # Quick build script
├── build/                               # Build cache (can delete)
├── dist/
│   └── OnePlus_Backup_Tool.exe         # 🎯 Your standalone executable!
└── backups/                             # Backup storage folder
```

### 🔄 Rebuilding the Executable

If you make changes to the Python script:

1. **Method 1**: Run `build_exe.bat`
2. **Method 2**: Manual command:
   ```cmd
   C:/ProgramData/miniconda3/Scripts/conda.exe run -p C:\ProgramData\miniconda3 --no-capture-output python -m PyInstaller oneplus_backup_tool.spec --clean
   ```

### 📊 Executable Details

- **Size**: ~15-25 MB (includes Python interpreter + libraries)
- **Type**: Windows PE executable
- **Mode**: Windowed (no console window)
- **Dependencies**: All bundled (tkinter, subprocess, etc.)

### 🎯 Distribution Tips

1. **Single File**: Just distribute `OnePlus_Backup_Tool.exe`
2. **ADB Requirement**: Remind users to have ADB available
3. **Antivirus**: Some antivirus may flag PyInstaller executables - this is normal
4. **Testing**: Test on a clean Windows machine without Python

### 🛠️ Advanced Customization

#### Add Icon (Optional)
1. Get a `.ico` file
2. Edit `oneplus_backup_tool.spec`:
   ```python
   icon='path/to/your/icon.ico'
   ```
3. Rebuild using `build_exe.bat`

#### Console Mode (For Debugging)
- Edit spec file: `console=True`
- Rebuild to show console output

#### Smaller Size
- Edit spec file: `upx=False` (if UPX causes issues)
- Use `--onefile` flag for single file (slower startup)

### ✅ Success!

Your OnePlus backup tool is now a professional standalone executable that can be distributed to anyone with a Windows computer! 🎉