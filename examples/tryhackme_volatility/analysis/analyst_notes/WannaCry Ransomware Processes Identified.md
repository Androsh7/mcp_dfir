# WannaCry Ransomware Processes Identified

Two processes clearly associated with WannaCry ransomware found in process list:

## `tasksche.exe` (PID: 1940)
- **PPID:** 1636 (explorer.exe) — spawned directly from user shell
- **Created:** 2017-05-12 21:22:14 UTC
- **Handles:** 51, Threads: 7
- **Significance:** Known WannaCry dropper/task scheduler component

## `@WanaDecryptor@` (PID: 740)
- **PPID:** 1940 (tasksche.exe) — child of WannaCry dropper
- **Created:** 2017-05-12 21:22:22 UTC
- **Handles:** 70, Threads: 2
- **Significance:** This IS the WannaCry ransom note/decryptor UI process — unmistakable WannaCry indicator

## System Time Correlation
System time 2017-05-12 aligns exactly with the global WannaCry outbreak date (May 12, 2017).

**Attribution: WannaCry ransomware (WCry/WannaCrypt) — attributed to Lazarus Group (North Korea / DPRK)**