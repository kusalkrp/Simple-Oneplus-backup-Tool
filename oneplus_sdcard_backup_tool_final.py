import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import threading
import queue
import time

# ---------- Helper Functions ----------
def run_cmd(cmd):
    """Run shell command and return output."""
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode(errors='ignore').strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode(errors='ignore').strip()

def adb(args):
    return run_cmd(["adb"] + args)

def device_connected():
    out = adb(["devices"])
    for line in out.splitlines():
        if line.strip().endswith("\tdevice"):
            return True
    return False

def adb_root():
    adb(["root"])
    adb(["wait-for-device"])

# ---------- GUI App ----------
class OnePlusBackupTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OnePlus Full Backup Tool")
        self.geometry("800x800")
        self.backup_dir = os.path.abspath("./backups")
        os.makedirs(self.backup_dir, exist_ok=True)

        # Queues for thread-safe UI updates
        self.progress_queue = queue.Queue()
        self.log_queue = queue.Queue()

        # ---------- Top Buttons ----------
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=5)
        ttk.Button(top_frame, text="Refresh SD Folders", command=self.refresh_sd_folders).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Refresh Device Backups", command=self.refresh_device_backups).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Select Backup Folder", command=self.choose_backup_dir).pack(side="right", padx=5)

        self.backup_dir_label = ttk.Label(self, text=f"Backup folder: {self.backup_dir}")
        self.backup_dir_label.pack()

        # ---------- Notebook for Tabs ----------
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------- SD Card Tab ----------
        sd_tab = ttk.Frame(notebook)
        notebook.add(sd_tab, text="SD Card Folders")
        self.sd_frame = self.create_scrollable_frame_in(sd_tab, "SD Card Folders")
        self.sd_folder_vars = {}
        sd_button_frame = ttk.Frame(self.sd_frame["frame"])
        sd_button_frame.pack(side="bottom", fill="x", padx=5, pady=2)
        ttk.Button(sd_button_frame, text="Select All SD", command=self.select_all_sd).pack(side="left", padx=2)
        ttk.Button(sd_button_frame, text="Unselect All SD", command=self.unselect_all_sd).pack(side="left", padx=2)

        # ---------- Device Backups Tab ----------
        device_backup_tab = ttk.Frame(notebook)
        notebook.add(device_backup_tab, text="Device Backups")
        self.device_backup_frame = self.create_scrollable_frame_in(device_backup_tab, "OnePlus Local Backups")
        self.device_backup_vars = {}
        device_backup_button_frame = ttk.Frame(self.device_backup_frame["frame"])
        device_backup_button_frame.pack(side="bottom", fill="x", padx=5, pady=2)
        ttk.Button(device_backup_button_frame, text="Select All Backups", command=self.select_all_device_backups).pack(side="left", padx=2)
        ttk.Button(device_backup_button_frame, text="Unselect All Backups", command=self.unselect_all_device_backups).pack(side="left", padx=2)
        
        # Instructions label
        instruction_label = ttk.Label(device_backup_tab, text="First create backups using OnePlus device settings, then refresh to find them", 
                                    foreground="blue", font=("Arial", 10))
        instruction_label.pack(pady=5)

        # ---------- Backup & Restore Tab ----------
        backup_tab = ttk.Frame(notebook)
        notebook.add(backup_tab, text="Backup & Restore")

        # Progress Bar
        self.progress = ttk.Progressbar(backup_tab, orient="horizontal", length=780, mode="determinate")
        self.progress.pack(pady=5)
        self.progress_label = ttk.Label(backup_tab, text="Progress: Ready")
        self.progress_label.pack()

        # Log
        log_frame = ttk.LabelFrame(backup_tab, text="Log")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_text = tk.Text(log_frame, height=10, state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True)

        # Action Buttons
        action_frame = ttk.Frame(backup_tab)
        action_frame.pack(fill="x", pady=10)
        ttk.Button(action_frame, text="Backup Selected", command=self.backup_selected).pack(side="left", padx=10, pady=5)
        ttk.Button(action_frame, text="Restore Selected", command=self.restore_selected).pack(side="left", padx=10, pady=5)

        # Set default tab to Backup & Restore
        notebook.select(2)

        # Initialize lists
        self.refresh_sd_folders()
        self.refresh_device_backups()
        self.update_progress()
        self.update_log()

    def update_progress(self):
        updated = False
        try:
            while True:
                section, percent, item_label = self.progress_queue.get_nowait()
                self._update_progress(section, percent, item_label)
                updated = True
        except queue.Empty:
            pass
        
        # Force UI update if progress changed
        if updated:
            self.update_idletasks()
        
        # Check more frequently during operations
        self.after(50, self.update_progress)

    def update_log(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.log_text.configure(state="normal")
                self.log_text.insert("end", f"[{timestamp}] {msg}\n")
                self.log_text.see("end")
                self.log_text.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self.update_log)

    # ---------- Utility Functions ----------
    def log(self, msg):
        self.log_queue.put(msg)

    def create_scrollable_frame(self, title, height):
        frame = ttk.LabelFrame(self, text=title)
        frame.pack(fill="both", expand=False, padx=5, pady=5)
        # frame.config(height=height)  # Removed fixed height to allow buttons to be visible
        canvas = tk.Canvas(frame)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        inner = ttk.Frame(canvas)
        canvas.create_window((0,0), window=inner, anchor='nw')
        return {"frame": frame, "canvas": canvas, "inner": inner}

    def create_scrollable_frame_in(self, parent, title):
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        canvas = tk.Canvas(frame)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        inner = ttk.Frame(canvas)
        canvas.create_window((0,0), window=inner, anchor='nw')
        return {"frame": frame, "canvas": canvas, "inner": inner}

    def _update_progress(self, section, percent, item_label):
        bounded = max(0, min(100, percent))
        self.progress['value'] = bounded
        detail = f" ({item_label})" if item_label else ""
        self.progress_label.config(text=f"{section}: {bounded}%{detail}")

    def _enqueue_progress(self, section, percent, item_label):
        self.progress_queue.put((section, percent, item_label))

    def _parse_adb_progress_line(self, line):
        text = line.strip()
        if not text:
            return None, ""
        
        # Look for various ADB progress patterns
        patterns = [
            r"\]\s*(.*?):\s*(\d+)%",  # Original pattern
            r"pull:\s*(.*?):\s*(\d+)%",  # Pull pattern
            r"push:\s*(.*?):\s*(\d+)%",  # Push pattern
            r"(.*?):\s*(\d+)%",  # Generic file: X% pattern
            r"\[(\d+)%\]\s*(.*)",  # [X%] file pattern
            r"(\d+)%\s*\|\s*(.*)",  # X% | file pattern
            r"(\d+)%\s+(.+)",  # X% filename
            r"(.+)\s+(\d+)%",  # filename X%
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    if len(match.groups()) >= 2:
                        # Check if first group is percentage or filename
                        if match.group(1).isdigit():
                            return int(match.group(1)), match.group(2).strip()
                        else:
                            return int(match.group(2)), match.group(1).strip()
                except (ValueError, IndexError):
                    continue
        
        # Fallback: look for any percentage
        generic = re.search(r"(\d+)%", text)
        if generic:
            return int(generic.group(1)), text.split()[0] if text.split() else ""
        
        return None, ""
    
    def _parse_file_transfer_info(self, line):
        """Parse file transfer information from ADB output"""
        # Look for patterns like: "filename: 1234/5678 (20%)"
        # or "Transferring file.txt (1234 bytes of 5678)"
        patterns = [
            r"(\S+):\s*(\d+)/(\d+)\s*\((\d+)%\)",
            r"Transferring\s+(\S+)\s*\((\d+)\s*bytes\s*of\s*(\d+)\)",
            r"(\d+)\s*KB/s\s*\((\d+)\s*bytes\)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) >= 3:
                        if len(groups) == 4:  # filename: current/total (percent%)
                            return int(groups[1]), int(groups[2]), groups[0]
                        elif len(groups) == 3:  # Transferring filename (current bytes of total)
                            return int(groups[1]), int(groups[2]), groups[0]
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _print_terminal_progress(self, section, percent, item):
        """Print progress to terminal/console"""
        # Create a progress bar
        bar_length = 40
        filled_length = int(bar_length * percent / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Calculate elapsed time
        elapsed = time.time() - self.operation_start_time if self.operation_start_time else 0
        
        # Calculate ETA
        if percent > 0 and elapsed > 1:
            eta = (elapsed * (100 - percent)) / percent
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: --"
        
        # Print progress (this will show in console if running from terminal)
        progress_line = f"\r{section}: [{bar}] {percent:3d}% | {item[:30]:<30} | {elapsed:.1f}s | {eta_str}"
        print(progress_line, end='', flush=True)
        
        if percent >= 100:
            print()  # New line when complete

    def _run_command_with_progress(self, cmd, section, context_label):
        self._enqueue_progress(section, 0, context_label)
        self.log(f"{section}: {context_label} - started")
        self.log(f"Running command: {' '.join(cmd)}")
        
        # Terminal progress setup
        self.current_operation = f"{section}: {context_label}"
        self.operation_start_time = time.time()
        
        try:
            # Start the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            
            # Start a separate thread to monitor progress
            progress_thread = threading.Thread(
                target=self._monitor_progress_thread,
                args=(section, context_label, process),
                daemon=True
            )
            progress_thread.start()
            
            # Read output for logging
            stdout, stderr = process.communicate()
            
            # Wait for progress thread to finish
            progress_thread.join(timeout=1)
            
            # Log all output
            if stdout:
                for line in stdout.splitlines():
                    if line.strip():
                        self.log(line.strip())
            
            if stderr:
                for line in stderr.splitlines():
                    if line.strip():
                        self.log(f"Error: {line.strip()}")
            
            returncode = process.returncode
            
        except Exception as exc:
            self.log(f"{section}: {context_label} - error: {exc}")
            self._enqueue_progress(section, 0, f"Error: {exc}")
            self._print_terminal_progress(section, 0, f"Error: {exc}")
            return False
            
        if returncode != 0:
            self.log(f"{section}: {context_label} failed (exit {returncode})")
            self._enqueue_progress(section, 0, f"Failed (exit {returncode})")
            self._print_terminal_progress(section, 0, f"Failed (exit {returncode})")
            return False
            
        # Always ensure we show 100% completion
        self._enqueue_progress(section, 100, "Completed")
        self._print_terminal_progress(section, 100, "Completed")
        self.log(f"{section}: {context_label} - done")
        return True
    
    def _monitor_progress_thread(self, section, context_label, process):
        """Monitor progress in a separate thread with real-time updates"""
        start_time = time.time()
        
        while process.poll() is None:  # While process is running
            elapsed = time.time() - start_time
            
            # Estimate progress based on elapsed time
            # Most file transfers take 10-60 seconds depending on size
            if elapsed < 5:
                percent = int(elapsed * 10)  # 0-50% in first 5 seconds
            elif elapsed < 15:
                percent = 50 + int((elapsed - 5) * 3)  # 50-80% in next 10 seconds  
            elif elapsed < 30:
                percent = 80 + int((elapsed - 15) * 1)  # 80-95% in next 15 seconds
            else:
                percent = min(95, 95 + int((elapsed - 30) * 0.1))  # Slowly approach 95%
            
            percent = min(percent, 95)  # Never exceed 95% until complete
            
            # Update progress
            self._enqueue_progress(section, percent, context_label)
            self._print_terminal_progress(section, percent, context_label)
            
            # Update every 0.5 seconds for smooth progress
            time.sleep(0.5)
        
        # Final update when process completes
        self._enqueue_progress(section, 100, "Completed")
        self._print_terminal_progress(section, 100, "Completed")

    def choose_backup_dir(self):
        chosen = filedialog.askdirectory(initialdir=self.backup_dir, title="Choose backup folder")
        if chosen:
            self.backup_dir = chosen
            self.backup_dir_label.config(text=f"Backup folder: {self.backup_dir}")

    # ---------- SD Card Folders ----------
    def refresh_sd_folders(self):
        for widget in self.sd_frame["inner"].winfo_children():
            widget.destroy()
        self.sd_folder_vars.clear()
        if not device_connected():
            self.log("Device not detected. Connect and enable USB debugging.")
            return
        adb_root()
        out = adb(["shell", "ls", "-1", "-A", "/sdcard/"])
        folders = [f.strip() for f in out.splitlines() if f.strip()]
        for idx, folder in enumerate(folders):
            var = tk.IntVar(value=1)
            cb = ttk.Checkbutton(self.sd_frame["inner"], text=folder, variable=var)
            cb.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            self.sd_folder_vars[folder] = var
        self.log(f"Found {len(folders)} folders on /sdcard/.")

    # ---------- Device Backups ----------
    def refresh_device_backups(self):
        for widget in self.device_backup_frame["inner"].winfo_children():
            widget.destroy()
        self.device_backup_vars.clear()
        if not device_connected():
            self.log("Device not detected. Connect and enable USB debugging.")
            return
        adb_root()
        
        # Check OnePlus backup locations
        backup_paths = [
            "/sdcard/Android/data/com.oneplus.backuprestore",
            "/storage/emulated/0/Android/data/com.oneplus.backuprestore"
        ]
        
        found_folders = []
        
        for path in backup_paths:
            self.log(f"Checking OnePlus backup folder: {path}")
            try:
                # Check if the backup folder exists and has content
                out = adb(["shell", "ls", "-la", path])
                if out and "No such file" not in out and "Permission denied" not in out:
                    # Check if it has the Backup subfolder
                    backup_folder = f"{path}/Backup"
                    backup_out = adb(["shell", "ls", "-la", backup_folder])
                    if backup_out and "No such file" not in backup_out and "Permission denied" not in backup_out:
                        # Get folder size
                        try:
                            size_out = adb(["shell", "du", "-sh", backup_folder])
                            size_info = "Unknown size"
                            if size_out and size_out.strip():
                                size_parts = size_out.strip().split()
                                if size_parts:
                                    size_info = size_parts[0]
                        except Exception:
                            size_info = "Unknown size"
                        
                        found_folders.append({
                            'path': path,
                            'backup_path': backup_folder,
                            'size': size_info
                        })
                        self.log(f"Found OnePlus backup folder: {backup_folder} ({size_info})")
                        break  # Use first valid path found
            except Exception as e:
                self.log(f"Error checking {path}: {e}")
                continue
        
        if not found_folders:
            self.log("No OnePlus backup folders found. Create a backup first using device settings.")
            return
        
        # Display found backup folders
        for idx, folder_info in enumerate(found_folders):
            var = tk.IntVar(value=1)
            display_text = f"OnePlus Backup Folder ({folder_info['size']})"
            cb = ttk.Checkbutton(self.device_backup_frame["inner"], text=display_text, variable=var)
            cb.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            self.device_backup_vars[folder_info['backup_path']] = var
            
            # Add info label
            info_label = ttk.Label(self.device_backup_frame["inner"], 
                                 text=f"Path: {folder_info['backup_path']}", 
                                 foreground="gray", font=("Arial", 9))
            info_label.grid(row=idx+1, column=0, sticky="w", padx=20, pady=(0,5))
        
        self.log(f"Found {len(found_folders)} OnePlus backup folders.")

    # ---------- Select All/Unselect All Methods ----------
    def select_all_sd(self):
        for var in self.sd_folder_vars.values():
            var.set(1)

    def unselect_all_sd(self):
        for var in self.sd_folder_vars.values():
            var.set(0)

    def select_all_device_backups(self):
        for var in self.device_backup_vars.values():
            var.set(1)

    def unselect_all_device_backups(self):
        for var in self.device_backup_vars.values():
            var.set(0)

    # ---------- Backup ----------
    def backup_selected(self):
        confirm = messagebox.askyesno("Confirm Backup", "Backup selected SD folders and device backup files?")
        if not confirm:
            return
        threading.Thread(target=self._backup_worker, daemon=True).start()

    def _backup_worker(self):
        adb_root()
        # 1. SD Card
        sd_selected = [f for f, v in self.sd_folder_vars.items() if v.get() == 1]
        if sd_selected:
            sd_parent = os.path.join(self.backup_dir, "sdcard")
            os.makedirs(sd_parent, exist_ok=True)
            for folder in sd_selected:
                remote = f"/sdcard/{folder}"
                self._run_command_with_progress(["adb", "pull", remote, sd_parent], "SD Card", remote)

        # 2. OnePlus Backups (Complete Folder)
        device_backups_selected = [f for f, v in self.device_backup_vars.items() if v.get() == 1]
        if device_backups_selected:
            device_backup_dir = os.path.join(self.backup_dir, "oneplus_backups")
            os.makedirs(device_backup_dir, exist_ok=True)
            
            for backup_folder in device_backups_selected:
                # Pull the entire OnePlus backup folder
                folder_name = backup_folder.split("/")[-1]  # Get "Backup" from the path
                local_dest = os.path.join(device_backup_dir, folder_name)
                self._run_command_with_progress(["adb", "pull", backup_folder, local_dest], "OnePlus Backup", backup_folder)

        self._enqueue_progress("Complete", 100, "Backup finished")
        messagebox.showinfo("Backup Completed", f"Backup completed. Saved in:\n{self.backup_dir}")
        self.log("Backup finished.")

    # ---------- Restore ----------
    def restore_selected(self):
        """Open separate restore window"""
        RestoreWindow(self, self.backup_dir)
    
    def _restore_worker_new(self, selected_items):
        """New restore worker for separate UI"""
        adb_root()
        
        total_items = len(selected_items)
        
        for idx, item in enumerate(selected_items):
            local_path = item['local_path']
            device_path = item['device_path']
            item_type = item['type']
            
            # Update progress
            progress_percent = int((idx / total_items) * 100)
            item_name = os.path.basename(local_path)
            self._enqueue_progress("Restoring", progress_percent, f"{item_name} -> {device_path}")
            
            try:
                if item_type == 'folder':
                    # First remove existing folder if it exists to avoid nesting
                    subprocess.run(["adb", "shell", "rm", "-rf", device_path], 
                                 capture_output=True, check=False)
                    
                    # Create parent directory on device
                    parent_dir = "/".join(device_path.split("/")[:-1])
                    subprocess.run(["adb", "shell", "mkdir", "-p", parent_dir], 
                                 capture_output=True, check=False)
                    
                    # Push folder contents to exact location
                    # Use "folder/." syntax to push contents instead of creating nested folder
                    source_contents = f"{local_path}/."
                    self._run_command_with_progress(["adb", "push", source_contents, device_path], 
                                                  "Restore Folder", item_name)
                
                elif item_type == 'file':
                    # Create parent directory on device
                    parent_dir = "/".join(device_path.split("/")[:-1])
                    subprocess.run(["adb", "shell", "mkdir", "-p", parent_dir], 
                                 capture_output=True, check=False)
                    
                    # Push file to exact location (this will overwrite existing file)
                    self._run_command_with_progress(["adb", "push", local_path, device_path], 
                                                  "Restore File", item_name)
                
                self.log(f"Restored: {item_name} -> {device_path}")
            
            except Exception as e:
                self.log(f"Failed to restore {item_name}: {e}")
        
        self._enqueue_progress("Restore Complete", 100, f"Restored {total_items} items")
        messagebox.showinfo("Restore Completed", f"Successfully restored {total_items} items.\nReboot recommended.")
        self.log("Restore operation completed.")

# ---------- Separate Restore Window ----------
class RestoreWindow:
    def __init__(self, parent, backup_dir):
        self.parent = parent
        self.backup_dir = backup_dir
        self.restore_items = {}
        
        self.window = tk.Toplevel(parent)
        self.window.title("OnePlus Restore Tool")
        self.window.geometry("900x700")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
        self.center_window()
        self.scan_available_backups()
    
    def center_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Restore Tool - Select Files and Folders", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Backup folder selection
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(folder_frame, text="Backup Folder:").pack(side="left")
        self.folder_var = tk.StringVar(value=self.backup_dir)
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, width=60)
        self.folder_entry.pack(side="left", padx=(5, 5), fill="x", expand=True)
        
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side="right")
        ttk.Button(folder_frame, text="Scan", command=self.scan_available_backups).pack(side="right", padx=(0, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="gray")
        self.status_label.pack(pady=(0, 10))
        
        # Tree view for file selection
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Tree with scrollbars
        self.tree = ttk.Treeview(tree_frame, columns=("checked", "type", "size", "device_path"), show="tree headings")
        self.tree.heading("#0", text="File/Folder Name")
        self.tree.heading("checked", text="✓")
        self.tree.heading("type", text="Type")
        self.tree.heading("size", text="Size")
        self.tree.heading("device_path", text="Device Path")
        
        # Column widths
        self.tree.column("#0", width=260)
        self.tree.column("checked", width=50)
        self.tree.column("type", width=100)
        self.tree.column("size", width=100)
        self.tree.column("device_path", width=340)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack tree and scrollbars
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Selection buttons
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(select_frame, text="Select All", command=self.select_all).pack(side="left", padx=(0, 5))
        ttk.Button(select_frame, text="Unselect All", command=self.unselect_all).pack(side="left", padx=(0, 5))
        ttk.Button(select_frame, text="Expand All", command=self.expand_all).pack(side="left", padx=(0, 5))
        ttk.Button(select_frame, text="Collapse All", command=self.collapse_all).pack(side="left")
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        # Warning
        warning_frame = ttk.Frame(button_frame)
        warning_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(warning_frame, text="⚠️ WARNING: Restore will overwrite existing data on device!", 
                 foreground="red", font=("Arial", 10, "bold")).pack()
        
        # Buttons
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Restore Selected", command=self.restore_selected).pack(side="right")
        
        # Enable checkboxes for tree items
        self.setup_tree_checkboxes()
    
    def setup_tree_checkboxes(self):
        """Enable checkbox functionality for tree items"""
        def on_click(event):
            # Get clicked item and region
            item = self.tree.identify('item', event.x, event.y)
            region = self.tree.identify('region', event.x, event.y)
            
            if item:
                column = self.tree.identify('column', event.x, event.y)
                # Check if clicked on checkbox column (#1 is the first column after #0)
                if column == "#1" or region == "tree":  # Allow clicking on item text or checkbox column
                    # Toggle checkbox
                    current_value = self.tree.set(item, "checked")
                    if current_value == "☑":
                        self.tree.set(item, "checked", "☐")
                        # Also uncheck children
                        self._select_item_recursive(item, False, True)
                    else:
                        self.tree.set(item, "checked", "☑")
                        # Also check children
                        self._select_item_recursive(item, True, True)
        
        self.tree.bind("<Button-1>", on_click)
        
        # Add hover effect
        def on_motion(event):
            item = self.tree.identify('item', event.x, event.y)
            column = self.tree.identify('column', event.x, event.y)
            if item and column == "#1":
                self.tree.config(cursor="hand2")
            else:
                self.tree.config(cursor="")
        
        self.tree.bind("<Motion>", on_motion)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.backup_dir, title="Select backup folder")
        if folder:
            self.folder_var.set(folder)
    
    def scan_available_backups(self):
        """Scan the backup folder and populate the tree"""
        self.progress.start()
        self.status_label.config(text="Scanning backups...")
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        backup_folder = self.folder_var.get()
        if not os.path.exists(backup_folder):
            self.status_label.config(text="Backup folder not found")
            self.progress.stop()
            return
        
        try:
            self.restore_items.clear()
            
            # Scan SD Card backups
            sdcard_dir = os.path.join(backup_folder, "sdcard")
            if os.path.exists(sdcard_dir):
                sdcard_node = self.tree.insert("", "end", text="📱 SD Card Data", 
                                              values=("☐", "Category", "", "/sdcard"), tags=["category"])
                self.scan_directory(sdcard_dir, sdcard_node, "/sdcard")
            
            # Scan OnePlus backups
            oneplus_dir = os.path.join(backup_folder, "oneplus_backups")
            if os.path.exists(oneplus_dir):
                oneplus_node = self.tree.insert("", "end", text="🔧 OnePlus Backups", 
                                               values=("☐", "Category", "", "/sdcard/Android/data/com.oneplus.backuprestore"), 
                                               tags=["category"])
                self.scan_directory(oneplus_dir, oneplus_node, "/sdcard/Android/data/com.oneplus.backuprestore")
            
            # Scan legacy device backups
            device_dir = os.path.join(backup_folder, "device_backups")
            if os.path.exists(device_dir):
                device_node = self.tree.insert("", "end", text="📦 Legacy Device Backups", 
                                              values=("☐", "Category", "", "/sdcard/Android/data/com.oneplus.backuprestore"), 
                                              tags=["category"])
                self.scan_directory(device_dir, device_node, "/sdcard/Android/data/com.oneplus.backuprestore")
            
            self.status_label.config(text=f"Found {len(self.restore_items)} items")
            
        except Exception as e:
            self.status_label.config(text=f"Error scanning: {e}")
        
        self.progress.stop()
    
    def scan_directory(self, local_path, parent_node, device_base_path):
        """Recursively scan directory and add to tree"""
        try:
            for item in sorted(os.listdir(local_path)):
                item_path = os.path.join(local_path, item)
                device_path = f"{device_base_path}/{item}"
                
                if os.path.isdir(item_path):
                    # Get folder size
                    try:
                        total_size = 0
                        file_count = 0
                        for dirpath, dirnames, filenames in os.walk(item_path):
                            for filename in filenames:
                                fp = os.path.join(dirpath, filename)
                                total_size += os.path.getsize(fp)
                                file_count += 1
                        
                        if total_size > 1024*1024*1024:  # GB
                            size_text = f"{total_size/(1024*1024*1024):.1f} GB ({file_count} files)"
                        elif total_size > 1024*1024:  # MB
                            size_text = f"{total_size/(1024*1024):.1f} MB ({file_count} files)"
                        else:  # KB
                            size_text = f"{total_size/1024:.1f} KB ({file_count} files)"
                    except Exception:
                        size_text = "Unknown"
                    
                    # Add folder node
                    folder_node = self.tree.insert(parent_node, "end", text=f"📁 {item}", 
                                                  values=("☐", "Folder", size_text, device_path), 
                                                  tags=["folder"])
                    
                    # Store restore info
                    self.restore_items[folder_node] = {
                        'local_path': item_path,
                        'device_path': device_path,
                        'type': 'folder'
                    }
                    
                    # Recursively scan subdirectories (limit depth for performance)
                    if parent_node != "":  # Only go 2 levels deep
                        self.scan_directory(item_path, folder_node, device_path)
                
                else:
                    # File
                    try:
                        file_size = os.path.getsize(item_path)
                        if file_size > 1024*1024:  # MB
                            size_text = f"{file_size/(1024*1024):.1f} MB"
                        else:  # KB
                            size_text = f"{file_size/1024:.1f} KB"
                    except Exception:
                        size_text = "Unknown"
                    
                    # Determine file type icon
                    ext = os.path.splitext(item)[1].lower()
                    if ext in ['.apk']:
                        icon = "📱"
                        file_type = "App"
                    elif ext in ['.db', '.db-journal']:
                        icon = "🗃️"
                        file_type = "Database"
                    elif ext in ['.xml', '.conf']:
                        icon = "⚙️"
                        file_type = "Config"
                    elif ext in ['.vcf']:
                        icon = "👥"
                        file_type = "Contacts"
                    elif ext in ['.vmsg']:
                        icon = "💬"
                        file_type = "Messages"
                    elif ext in ['.jpg', '.png', '.gif']:
                        icon = "🖼️"
                        file_type = "Image"
                    else:
                        icon = "📄"
                        file_type = "File"
                    
                    file_node = self.tree.insert(parent_node, "end", text=f"{icon} {item}", 
                                                values=("☐", file_type, size_text, device_path), 
                                                tags=["file"])
                    
                    # Store restore info
                    self.restore_items[file_node] = {
                        'local_path': item_path,
                        'device_path': device_path,
                        'type': 'file'
                    }
        
        except Exception:
            pass  # Skip inaccessible directories
    
    def select_all(self):
        """Select all items"""
        for item in self.tree.get_children():
            self._select_item_recursive(item, True)
    
    def unselect_all(self):
        """Unselect all items"""
        for item in self.tree.get_children():
            self._select_item_recursive(item, False)
    
    def _select_item_recursive(self, item, select, avoid_self=False):
        """Recursively select/unselect items"""
        if not avoid_self:
            if select:
                self.tree.set(item, "checked", "☑")
            else:
                self.tree.set(item, "checked", "☐")
        
        # Recursively handle children
        for child in self.tree.get_children(item):
            self._select_item_recursive(child, select, False)
    
    def expand_all(self):
        """Expand all tree nodes"""
        for item in self.tree.get_children():
            self._expand_item_recursive(item)
    
    def collapse_all(self):
        """Collapse all tree nodes"""
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
    
    def _expand_item_recursive(self, item):
        """Recursively expand items"""
        self.tree.item(item, open=True)
        for child in self.tree.get_children(item):
            self._expand_item_recursive(child)
    
    def restore_selected(self):
        """Restore selected items"""
        selected_items = []
        
        for item in self.tree.get_children():
            self._collect_selected_items(item, selected_items)
        
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select at least one item to restore.")
            return
        
        # Confirm restore
        count = len(selected_items)
        confirm_text = f"Restore {count} selected items to device?\n\nThis will overwrite existing data!"
        
        if not messagebox.askyesno("Confirm Restore", confirm_text):
            return
        
        # Start restore process
        self.window.destroy()
        threading.Thread(target=self._restore_selected_items, args=(selected_items,), daemon=True).start()
    
    def _restore_selected_items(self, selected_items):
        """Restore selected items using parent's methods"""
        self.parent._restore_worker_new(selected_items)
    
    def _collect_selected_items(self, item, selected_list):
        """Recursively collect selected items"""
        checked_value = self.tree.set(item, "checked")
        if checked_value == "☑" and item in self.restore_items:
            selected_list.append(self.restore_items[item])
        
        # Check children
        for child in self.tree.get_children(item):
            self._collect_selected_items(child, selected_list)



# ---------- Run ----------
if __name__=="__main__":
    app = OnePlusBackupTool()
    app.mainloop()
