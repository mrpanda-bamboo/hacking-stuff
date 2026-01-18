This tool automates the dumping of SAM and SYSTEM registry hives, handles UAC escalation, compresses data to bypass Discord's 25MB limit, exfiltrates via Webhooks, and performs a secure cleanup of all temporary files post-exfiltration.

## Quick Start
Open exfiltrator.py and replace YOUR_WEBHOOK with your Discord Webhook URL.

Run the script on a Windows target

## Extraction & Cracking (Kali Linux)
1. Extract Hashes
Use mimikatz to dump the hashes from the exfiltrated hives:

start mimikatz:

``wine /usr/share/windows-resources/mimikatz``

dump the hashes:

``lsadumpsam /system:/PATH_TO_SYSTEM /sam:/PATH_TO_SAM``

2. Crack with Hashcat
Save the NT-Hash to a file named hashes.txt or insert it into command and run a dictionary attack:

``hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt.gz`` / ``hashcat -m 1000 HASH /usr/share/wordlists/rockyou.txt.gz``

⚠️ Disclaimer
Educational and authorized security testing only. The author is not responsible for any misuse, illegal activity, or damage caused by this script.
