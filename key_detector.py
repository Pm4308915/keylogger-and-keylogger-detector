# Import the 'psutil' library, which helps us see running processes
# it has detected the .exe file

import psutil

def detect_keylogger():
    # 1. Create a list of "suspicious" words
    suspicious_names = ['keylogger', 'logkeys', 'xinput','key_logger','keylog']

    # 2. Create a "flag" to track if we find anything
    # We'll set this to True if we find a suspicious process
    found_suspicious_process = False

    print("[+] Starting scan for suspicious process names...")

    # 3. Loop through every single process currently running
    for proc in psutil.process_iter(['pid', 'name']):       # psutil.process_iter is main command for detection
        try:
            # 4. Get the process info
            process_info = proc.info
            process_name = process_info['name'].lower() # Get name and make it lowercase like Chrome.exe to chrome.exe

            # 5. Check if any suspicious word is in the process name
            for name in suspicious_names:   
                if name in process_name:    # if "key_logger" in "key_logger.exe":
                    # 6. If we find a match, print a warning...
                    print(f"\n[!] WARNING! Suspicious process found:")
                    print(f"    Name: {process_info['name']}")
                    print(f"    PID:  {process_info['pid']}")
                    # ...and set our flag to True
                    found_suspicious_process = True
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # If we can't access a process, just ignore it and continue
            pass

    # 7. After the loop, check our flag
    print("\n[+] Scan complete.")
    if not found_suspicious_process:
        print("[+] All clear! No suspicious process names were found.")

# --- This line runs the function when you start the script ---
if __name__ == "__main__":
    detect_keylogger()