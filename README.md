# OnePlus Backup Tool

A comprehensive backup and restore solution for OnePlus devices with advanced file management and selective restore capabilities.

## 📱 Overview

The OnePlus Backup Tool is a professional Windows application designed specifically for OnePlus device owners who need reliable, granular control over their device backups. **Featuring a revolutionary dual backup approach**, this tool combines traditional SD card backup with native OnePlus backup integration for complete device coverage.

Unlike standard backup solutions that only capture user files, our **dual backup system** ensures both your personal data AND system-level backups are preserved and easily restorable with complete visibility into backup contents and precise restoration control.

## ✨ Key Features

### 🗂️ **Revolutionary Dual Backup System** ⭐

**The only tool that combines BOTH backup methods for complete coverage:**

#### 📁 **Layer 1: SD Card Backup**
- **Complete File System**: Every folder, every file from your device's storage
- **User Data Focus**: Photos, downloads, documents, custom folders
- **Direct Access**: Raw file-level backup with original structure preserved
- **Universal Compatibility**: Works with any Android file manager content

#### 🔧 **Layer 2: OnePlus Native Integration**
- **System-Level Backups**: Apps, settings, SMS, contacts, call logs
- **OnePlus Optimized**: Leverages OnePlus's proprietary backup format
- **Deep Integration**: System databases, configurations, app data
- **Native Restoration**: Seamlessly integrates with OnePlus restore mechanisms

#### 🎯 **Smart Dual Detection**
- **Automatic Discovery**: Finds existing backups from both systems
- **Unified Management**: Single interface for both backup types
- **Cross-Reference**: Links related backups for complete restore sessions
- **Intelligent Scanning**: Differentiates between backup types automatically

### 🎯 **Advanced Restore Interface**
- **Separate Restore Window**: Dedicated interface for restore operations
- **File Tree Visualization**: Browse backups with complete directory structure
- **Device Path Mapping**: See exactly where each file will be restored on your device
- **Selective Restoration**: Choose individual files, folders, or entire categories
- **Checkbox Selection**: Intuitive selection with Select All/Unselect All options

### 📊 **Comprehensive File Management**
- **File Type Recognition**: Automatic categorization with icons
  - 📱 Apps (.apk files)
  - 🗃️ Databases (.db, .db-journal)  
  - ⚙️ Configuration files (.xml, .conf)
  - 👥 Contacts (.vcf)
  - 💬 Messages (.vmsg)
  - 🖼️ Images (.jpg, .png, .gif)
  - 📄 Documents and other files
- **Size Information**: File and folder sizes displayed
- **Original Path Display**: See source and destination paths

### 🚀 **Real-Time Progress Monitoring**
- **Live Progress Bars**: Real-time transfer progress with speed indicators
- **Detailed Logging**: Complete operation logs with timestamps
- **Background Processing**: Non-blocking operations with threading
- **Error Handling**: Robust error recovery and reporting

### 🔧 **Professional User Interface**
- **Tabbed Interface**: Organized sections for different backup types
- **Modern GUI**: Clean, intuitive design built with tkinter
- **Responsive Design**: Scalable windows with proper scrolling
- **Status Updates**: Real-time status messages and progress feedback

## 🛠️ System Requirements

### **For End Users (Executable)**
- Windows 7/8/10/11 (64-bit)
- Android Debug Bridge (ADB) installed
- OnePlus device with USB debugging enabled
- USB cable for device connection

### **For Developers (Python)**
- Python 3.7+ with tkinter support
- Android SDK Platform Tools (ADB)
- Windows PowerShell or Command Prompt access

## 📦 Installation & Setup

### **Option 1: Executable (Recommended)**
1. Download `OnePlus_Backup_Tool.exe`
2. Install ADB (Android Platform Tools)
3. Enable USB debugging on your OnePlus device
4. Run the executable - no Python installation needed!

### **Option 2: Python Script**
1. Clone or download the source code
2. Install Python 3.7+ with tkinter
3. Install required dependencies (if any)
4. Run: `python oneplus_sdcard_backup_tool_final.py`

## 🎮 How to Use

### **Initial Setup**
1. **Connect Device**: USB cable to OnePlus device
2. **Enable Debugging**: Settings > Developer Options > USB Debugging
3. **Launch Tool**: Run OnePlus_Backup_Tool.exe
4. **Grant Permissions**: Accept ADB debugging prompt on device

### **Creating Dual Backups** 🔄

**The tool creates TWO types of backups simultaneously:**

#### **Phase 1: User Data Backup (SD Card)**
1. **Scan SD Content**: Click "Refresh SD Folders" to discover user files
2. **Select Personal Data**: Choose photos, downloads, documents using checkboxes
3. **Raw File Backup**: Direct file-by-file copy with structure preservation

#### **Phase 2: System Backup (OnePlus Native)**
1. **Scan System Backups**: Click "Refresh Device Backups" to find OnePlus backups
2. **Select System Data**: Choose apps, settings, SMS, contacts from native backups
3. **Native Format Backup**: Preserves OnePlus backup integrity and format

#### **Unified Process**
4. **Choose Location**: Select destination folder for BOTH backup types
5. **Dual Backup Execution**: Tool processes both backup layers simultaneously
6. **Progress Monitoring**: Real-time progress for each backup phase
7. **Completion**: Both backup types saved with timestamp organization

**Result**: Complete device backup covering both user files AND system data!

### **Dual Layer Restoration** 🔄

**Restore from EITHER or BOTH backup layers with complete control:**

#### **🎯 Smart Restore Interface**
1. **Open Restore Window**: Click "Restore Selected" for dedicated interface
2. **Dual Layer Detection**: Tool automatically identifies both backup types
3. **Layer Visualization**: Separate tabs for SD Card and OnePlus backups

#### **📱 Layer 1: User Data Restore (SD Card)**
4. **Browse Files**: Tree view of all SD card contents with original paths
5. **Selective Restoration**: Choose individual files, folders, or categories
6. **Path Mapping**: See exactly where files will be restored on device
7. **Direct File Restore**: Raw file placement maintaining directory structure

#### **🔧 Layer 2: System Restore (OnePlus Native)**
8. **System Data Selection**: Choose apps, contacts, SMS, settings from native backups
9. **Native Format Restore**: Preserves OnePlus backup format and integrity
10. **Deep System Integration**: Restores system databases and configurations

#### **🚀 Unified Restore Process**
11. **Cross-Layer Selection**: Mix and match from both backup layers
12. **Conflict Resolution**: Smart handling when data exists in both layers
13. **Progress Monitoring**: Real-time progress for each restoration phase
14. **Validation**: Post-restore verification for both layers
15. **Reboot Recommended**: Device restart for complete system integration

**Result**: Precise restoration combining user files AND system data!

## 📁 Dual Backup Structure

**Our revolutionary dual backup system creates TWO parallel backup layers:**

```
backups/
└── 2025-11-14_15-30-45/               # 🕐 Timestamped backup session
    │
    ├── 📱 LAYER 1: SD CARD BACKUP      # 👤 User Data Layer
    │   └── sdcard/                      
    │       ├── DCIM/                    # 📸 Camera photos & videos
    │       ├── Download/                # ⬇️ Downloaded files  
    │       ├── Documents/               # 📄 User documents
    │       ├── Music/                   # 🎵 Audio files
    │       ├── Pictures/                # 🖼️ Additional images
    │       ├── Android/data/            # 📱 App external data
    │       └── [custom folders]/        # 📂 User-created folders
    │
    ├── 🔧 LAYER 2: ONEPLUS NATIVE      # ⚙️ System Data Layer
    │   └── oneplus_backups/             
    │       └── Backup/                  # 🏠 Complete system backup
    │           ├── AppBackup/           # 📱 Application data & settings
    │           ├── ContactBackup/       # 👥 Contacts database
    │           ├── SmsBackup/           # 💬 SMS messages
    │           ├── CalllogBackup/       # ☎️ Call history
    │           ├── SystemSettings/      # ⚙️ System configurations
    │           ├── WifiBackup/          # 📶 WiFi passwords & settings
    │           └── [system databases]/  # 🗃️ Core system data
    │
    └── 📦 LEGACY SUPPORT               # 🔄 Additional backups
        └── device_backups/              
            ├── contacts.vcf             # 📇 Exported contacts
            ├── messages.vmsg           # 📨 SMS backup
            └── [other formats]/         # 🔧 Various backup formats
```

### **🎯 Dual Layer Benefits:**
- **📱 Layer 1**: Direct file access, universal compatibility, easy browsing
- **🔧 Layer 2**: System integrity, OnePlus optimization, complete app data
- **🔄 Combined**: Total device coverage with redundancy and flexibility

## 🔍 Technical Features

### **Dual Backup Capabilities** 🚀

#### **🔄 Unified Dual-Layer Processing**
- **Simultaneous Operation**: Both backup layers processed in parallel
- **Cross-Layer Validation**: Ensures consistency between backup types
- **Intelligent Deduplication**: Prevents redundant backup of same data
- **Layer Prioritization**: Smart handling when data exists in both layers

#### **📱 SD Card Layer (User Data)**
- **Complete Filesystem**: Full directory tree with structure preservation
- **Raw File Access**: Direct file-level backup for maximum compatibility
- **Selective Granularity**: Individual folder and file selection
- **Universal Format**: Standard file system backup readable anywhere

#### **🔧 OnePlus Native Layer (System Data)**
- **Native Format Preservation**: Maintains OnePlus backup integrity
- **System Database Backup**: Complete app data, settings, configurations
- **Proprietary Integration**: Leverages OnePlus's built-in backup mechanisms
- **Deep System Access**: Captures data inaccessible through standard methods

#### **⚡ Advanced Processing**
- **Incremental Detection**: Identifies changes in both backup layers
- **Smart Updates**: Updates only modified data in each layer
- **Compression**: Layer-appropriate compression for optimal storage
- **Integrity Validation**: Verifies both backup layers independently

### **Restore Capabilities**
- **Granular Control**: Individual file/folder restoration
- **Path Validation**: Ensures correct device path mapping  
- **Overwrite Protection**: Smart handling of existing files
- **Batch Operations**: Multiple file restoration with progress tracking

### **Safety Features**
- **Root Access**: Automatic ADB root escalation when needed
- **Error Recovery**: Robust error handling and retry mechanisms
- **Validation**: Pre-restore checks for device compatibility
- **Logging**: Comprehensive operation logs for troubleshooting

## 🎯 Dual Backup Use Cases

### **🏠 For Regular Users**
**Complete Protection Scenarios:**
- **Pre-Update Safety**: Dual backup before OnePlus system updates (user files + system state)
- **Factory Reset Recovery**: Full device restoration with both personal files AND app settings
- **Device Migration**: Transfer complete device state to new OnePlus device
- **Accident Protection**: Recover from data loss with both file-level and system-level restoration

### **⚡ Smart Restoration Scenarios:**
- **Selective App Restore**: Restore specific apps with data from OnePlus layer only
- **File Recovery**: Restore accidentally deleted photos from SD card layer only
- **Settings Migration**: Transfer system settings while keeping current files
- **Hybrid Restore**: Combine old files with new system configuration

### **For Power Users**
- Advanced backup scheduling and management
- Detailed backup analysis and verification
- Custom backup configurations
- Development and testing data management

### **For Technicians**
- Professional device servicing
- Data recovery operations  
- Device migration services
- Bulk device management

## 📋 Supported Data Types

| Category | File Types | Description |
|----------|------------|-------------|
| **Applications** | .apk | Installed applications |
| **Contacts** | .vcf, .db | Contact databases and exports |
| **Messages** | .vmsg, .db | SMS/MMS message backups |
| **Media** | .jpg, .png, .mp4, .mp3 | Photos, videos, music |
| **Documents** | .pdf, .doc, .txt | User documents |
| **System Config** | .xml, .conf, .prop | System configuration files |
| **Databases** | .db, .db-journal | Application and system databases |
| **Archives** | .zip, .tar, .7z | Compressed backup files |

## ⚠️ Important Notes

### **Prerequisites**
- **ADB Required**: Android Debug Bridge must be properly installed
- **USB Debugging**: Must be enabled on OnePlus device  
- **Device Trust**: Accept computer fingerprint on device
- **Root Access**: Tool automatically handles root requirements

### **Limitations**
- **OnePlus Devices**: Optimized specifically for OnePlus devices
- **Windows Only**: Currently supports Windows operating systems
- **USB Connection**: Requires physical USB cable connection
- **Storage Space**: Ensure adequate space for backup storage

### **Dual Backup Safety Considerations**
- **Complete Coverage**: Dual backup ensures both user and system data protection
- **Layer Verification**: Validate both backup layers before major operations
- **Smart Restoration**: Choose appropriate layer(s) for your restoration needs
- **Device Reboot**: Essential after dual-layer restoration for system integration
- **Cross-Layer Validation**: Verify data consistency between backup layers
- **Antivirus**: Some antivirus may flag PyInstaller executables
- **Restore Strategy**: Plan whether you need file-only, system-only, or complete dual restoration

## 🔧 Troubleshooting

### **Common Issues**
- **ADB Not Found**: Install Android Platform Tools
- **Device Not Detected**: Check USB debugging and cable
- **Permission Denied**: Ensure ADB debugging is authorized
- **Restore Fails**: Verify device paths and storage space

### **Getting Help**
- Check device compatibility and ADB installation
- Review operation logs for error details
- Ensure proper USB debugging configuration
- Verify adequate storage space on both device and computer

## 📄 License

This tool is provided for personal and educational use. Please ensure compliance with your device warranty terms and local regulations regarding device modification and data backup.

---

**OnePlus Backup Tool** - Professional backup and restore solution for OnePlus devices with advanced file management capabilities.