import os
import psutil  # For scanning processes
import time

# --- These are the "signatures" we are looking for ---
SUSPICIOUS_SCRIPT_NAME = "key_listener.py"
SUSPICIOUS_LOG_FILE = "key_log.txt"
# ---------------------------------------------------

def scan_running_processes():
    """
    Scans all running processes to find one that matches our
    suspicious script name in its command line.
    """
    print(f"\n[+] Scanning running processes for '{SUSPICIOUS_SCRIPT_NAME}'...")
    found_process = False
    
    # Iterate over all running processes
    # 'pid', 'name', 'cmdline' are the details we want to check
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # proc.info['cmdline'] is a list of strings, like:
            # ['C:\\Python\\python.exe', 'key_listener.py']
            if proc.info['cmdline'] and SUSPICIOUS_SCRIPT_NAME in proc.info['cmdline']:
                print(f"  [!!!] THREAT DETECTED: Suspicious process found!")
                print(f"    - PID: {proc.info['pid']}")
                print(f"    - Name: {proc.info['name']}")
                print(f"    - Command: {' '.join(proc.info['cmdline'])}")
                found_process = True
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Some processes might die or be protected, so we just skip them
            pass
            
    return found_process

def scan_filesystem():
    """
    Scans the user's home directory to find the suspicious log file.
    """
    print(f"\n[+] Scanning filesystem for '{SUSPICIOUS_LOG_FILE}'...")
    
    # We will scan the user's "home" directory.
    # To scan your *entire* C: drive (which takes longer), 
    # change this to: start_path = 'C:\\'
    start_path = os.path.expanduser('~') 
    
    print(f"  > Starting scan from: {start_path}")
    
    found_file = False
    
    # os.walk() goes through every folder and file starting from 'start_path'
    for root_dir, directories, files in os.walk(start_path):
        
        # --- FIX: Added 'try' here ---
        # We try to scan the files in the current directory
        try:
            if SUSPICIOUS_LOG_FILE in files:
                full_path = os.path.join(root_dir, SUSPICIOUS_LOG_FILE)
                print(f"  [!!!] THREAT DETECTED: Suspicious log file found!")
                print(f"    - Location: {full_path}")
                found_file = True
                # We found it, so we can stop scanning
                break
        
        # --- FIX: 'except' is now correctly indented and part of the 'try' block ---
        except PermissionError:
            # If we get a permission error (e.g., trying to look in a 
            # protected system folder), just print a note and skip it.
            # print(f"  > Skipping protected directory: {root_dir}")
            pass
            
    return found_file

# --- Main part of the script ---
if __name__ == "__main__":
    print("--- Starting Cybersecurity System Scanner ---")
    start_time = time.time()
    
    process_found = scan_running_processes()
    file_found = scan_filesystem()
    
    end_time = time.time()
    print("\n--- Scan Complete ---")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
    
    if not process_found and not file_found:
        print("\n[OK] No suspicious files or processes found. System appears clean.")
    else:
        print("\n[DANGER] Scan finished. Threats were detected.")