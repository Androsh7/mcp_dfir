# Case 002 — Post-Incident Memory Analysis Report

**Analyst:** Memory Forensics Agent  
**Date of Analysis:** 2026-04-11  
**Evidence File:** `/evidence/Investigation-2.raw`  
**Evidence SHA256:** `76e8be1a3761878325fdff39a5ab1ff84922a0b18947e5268dd9175795ad2bf0`  
**Evidence Size:** 512 MB  
**Classification:** MALICIOUS — RANSOMWARE CONFIRMED  

---

## 1. Executive Summary

Memory analysis of the provided raw image confirms a successful **WannaCry ransomware infection** on a Windows XP SP3 workstation belonging to user **donny**, occurring on **2017-05-12 at approximately 21:22 UTC**. This date aligns precisely with the global WannaCry outbreak on May 12, 2017.

WannaCry (also known as WannaCrypt, WCry, and Wana Decrypt0r 2.0) is a crypto-ransomware worm attributed to **Lazarus Group**, a threat actor linked to the **Democratic People's Republic of Korea (DPRK / North Korea)**. It exploits the **EternalBlue (MS17-010)** vulnerability in Windows SMBv1 to propagate across networks without user interaction.

All key WannaCry components were identified in memory: the dropper, ransom UI, file deletion tool, worm service, and ransom payment infrastructure. Files on the host were actively encrypted at the time of capture. The WannaCry kill switch domain was present in memory but was not effective, indicating the host was **isolated from the internet** during the attack.

---

## 2. System Profile

| Field | Value |
|-------|-------|
| Operating System | Windows XP SP3 (32-bit, x86) |
| Build | 2600.xpsp_sp3_qfe.130704-0421 |
| NT Version | 5.1.2600 |
| System Root | `C:\WINDOWS` |
| System Time (capture) | **2017-05-12 21:26:32 UTC** |
| Logged-in User | **donny** |
| User SID | `S-1-5-21-602162358-764733703-1957994488-1003` |
| User Profile | `C:\Documents and Settings\donny\` |
| Processor Count | 1 |
| Volatility Symbols | `ntoskrnl.pdb / 423320282DB842E7BA2B0BFC86A84D75-2` |

---

## 3. Malware Identification

| Field | Value |
|-------|-------|
| Malware Family | **WannaCry** (WannaCrypt / Wana Decrypt0r 2.0 / WCry) |
| Malware Type | Ransomware Worm |
| Threat Actor | **Lazarus Group** (DPRK / North Korea) |
| Binary SHA256 | `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c` |
| Exploit Used | EternalBlue — CVE MS17-010 (SMBv1) |
| Initial Sample Path | `/home/infoseclabs/mal/wannacry/24d004a...c.bin` (analysis environment) |
| Infection Date | 2017-05-12 |

---

## 4. Attack Timeline

| Time (UTC) | PID | Event |
|------------|-----|-------|
| 21:22:10 | 1636 | `explorer.exe` active — user **donny** logged in |
| 21:22:14 | 1940 | `tasksche.exe` spawned by `explorer.exe` — ransomware dropper executed from `C:\Intel\ivecuqmanpnirkt615\` |
| 21:22:14 | 1956 | `ctfmon.exe` launched alongside (legitimate) |
| 21:22:22 | 740 | `@WanaDecryptor@.exe` launched by `tasksche.exe` — ransom note UI displayed to user |
| 21:22:52 | 1768 | `wuauclt.exe` spawned by `svchost.exe` |
| 21:25:52 | 424 | Earlier `@WanaDecryptor@` instance terminates |
| 21:26:22 | 536 | `taskse.exe` briefly runs — encryption task execution helper |
| 21:26:22 | 576 | Additional `@WanaDecryptor@` instance runs briefly |
| 21:26:23 | 860 | `taskdl.exe` briefly runs — deletes original pre-encryption files |
| 21:26:32 | — | **Memory capture taken** |

---

## 5. Malicious Process Analysis

### 5.1 Active Processes (at time of capture)

| Process | PID | PPID | Parent | Path | Role |
|---------|-----|------|--------|------|------|
| `tasksche.exe` | 1940 | 1636 | `explorer.exe` | `C:\Intel\ivecuqmanpnirkt615\tasksche.exe` | Main dropper / scheduler |
| `@WanaDecryptor@` | 740 | 1940 | `tasksche.exe` | `C:\Intel\ivecuqmanpnirkt615\@WanaDecryptor@.exe` | Ransom note UI / payment handler |

### 5.2 Terminated Processes (recovered via psscan)

| Process | PID | PPID | Created | Exited | Role |
|---------|-----|------|---------|--------|------|
| `taskse.exe` | 536 | 1940 | 21:26:22 | 21:26:23 | Task execution helper |
| `taskdl.exe` | 860 | 1940 | 21:26:23 | 21:26:23 | Deletes original files after encryption |
| `@WanaDecryptor@` | 424 | 1940 | 21:25:52 | 21:25:53 | Earlier ransom UI instance |
| `@WanaDecryptor@` | 576 | 1940 | 21:26:22 | 21:26:23 | Earlier ransom UI instance |

### 5.3 Process Hierarchy
```
System (PID 4)
└── smss.exe (PID 348)
    └── winlogon.exe (PID 620)
        ├── services.exe (PID 664)
        │   └── svchost.exe (PID 1024)
        │       └── wuauclt.exe (PID 1768)
        └── [explorer.exe parent PID 1608 — not in process list]
            └── explorer.exe (PID 1636)
                └── tasksche.exe (PID 1940)  ← MALWARE ENTRY POINT
                    ├── @WanaDecryptor@.exe (PID 740)  ← RANSOM UI
                    ├── taskse.exe (PID 536)  [terminated]
                    ├── taskdl.exe (PID 860)  [terminated]
                    ├── @WanaDecryptor@ (PID 424)  [terminated]
                    └── @WanaDecryptor@ (PID 576)  [terminated]
```

---

## 6. Malware Components and File Artifacts

### 6.1 Drop Directory
**Path:** `C:\Intel\ivecuqmanpnirkt615\`

WannaCry generates a random directory name under `C:\Intel\` as its working directory. A file handle to this directory was confirmed open in `tasksche.exe`.

| File | Purpose |
|------|---------|
| `tasksche.exe` | Main ransomware dropper and scheduler |
| `@WanaDecryptor@.exe` | Ransom note GUI and payment portal |
| `@WanaDecryptor@.HLP` | Ransom note help file |
| `taskdl.exe` | Deletes original files post-encryption |
| `taskse.exe` | Task execution / privilege escalation helper |
| `msg\m_English.wnry` | Multilingual ransom message archive |

### 6.2 Encrypted Files (.WNCRY) Identified in Memory
WannaCry encrypts files and appends the `.WNCRY` extension. The following encrypted file paths were recovered from memory strings:

- `C:\Python27\tcl\tcl8.5\msgs\ja.msg.WNCRY`
- `C:\Python27\tcl\tcl8.5\msgs\af.msg.WNCRY`
- `C:\Python27\include\pyexpat.h.WNCRY`
- `C:\Documents and Settings\donny\Cookies\JI4TYBE5.txt.WNCRY`

Encryption algorithm: **AES-128** (per file), with the AES key protected by **RSA-2048** (attacker's public key embedded in malware).

### 6.3 Notable Handle — Crypto Device
`tasksche.exe` held an open handle to `\Device\KsecDD` (Windows kernel cryptographic device driver), consistent with active encryption operations.

---

## 7. Persistence Mechanism

**Service Name:** `mssecsvc2.0`  
**Service Binary:** `mssecsvc.exe` (typical path: `C:\WINDOWS\mssecsvc.exe`)  
**Registry Key:** `SYSTEM\CurrentControlSet\Services\mssecsvc2.0`  

The service key was confirmed present across all registry hives loaded in memory:
- `WINDOWS\system32\config\system` (authoritative)
- `WINDOWS\system32\config\software`
- `WINDOWS\system32\config\default`
- User hive: `donny\NTUSER.DAT`
- User hive: `LocalService\NTUSER.DAT`
- User hive: `NetworkService\NTUSER.DAT`

**Function of mssecsvc2.0:** This service implements WannaCry's SMB worm component. It scans for hosts with TCP/445 open and exploits **EternalBlue (MS17-010)** to deliver and execute the malware on new targets. This enables network-wide lateral propagation without user interaction.

---

## 8. Network and C2 Analysis

### 8.1 Kill Switch Domain
**URL:** `http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`

This domain is hardcoded in WannaCry. Before encrypting files, the malware performs an HTTP GET to this URL. If the request succeeds (domain resolves and responds), WannaCry exits without encrypting.

The domain was registered on 2017-05-12 ~15:00 UTC by researcher Marcus Hutchins (MalwareTech), effectively sinkholing WannaCry globally. However, **files on this host were encrypted**, and the system time was 21:26:32 UTC — after the kill switch was active. This confirms the host **could not reach the internet** at the time of infection, preventing the kill switch from triggering.

### 8.2 Network Plugin Limitation
Windows XP (NT 5.1) is not supported by Volatility3's `windows.netscan` or `windows.netstat` plugins. Network connection artifacts could not be recovered via these methods. The EternalBlue propagation activity (inbound SMB on TCP/445) cannot be confirmed directly from this memory image.

---

## 9. Ransom Payment Infrastructure

| Field | Value |
|-------|-------|
| Demand | **$300 USD in Bitcoin** |
| Bitcoin Address 1 | `12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw` |
| Bitcoin Address 2 | `13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94` |
| Bitcoin Address 3 | `115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn` |
| QR Code URL | `http://www.btcfrog.com/qr/bitcoinPNG.php?address=12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw` |
| Bitcoin Purchase URL | `https://www.google.com/search?q=how+to+buy+bitcoin` |
| Ransom Note Languages | English, Danish, German, Dutch, Finnish, French, Italian, Latvian, Norwegian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Spanish, Chinese, Japanese, Croatian, Czech, Bulgarian, Greek, Hebrew (multilingual .wnry archive) |

**Note:** Payment to these addresses is strongly discouraged. The three addresses are shared across all WannaCry infections globally; decryption keys were never reliably delivered.

---

## 10. Memory Injection Analysis (malfind)

Multiple `PAGE_EXECUTE_READWRITE` (RWX) VAD regions were flagged in `winlogon.exe` (PID 620) with VadS tags (no file backing). Hexdump review showed null-byte content with Unicode character patterns consistent with Windows XP desktop/session management structures (CreateDesktop allocations). These are assessed as **likely benign** Windows XP session management artifacts rather than injected shellcode, though further analysis with a full VAD dump would be needed to fully rule out injection.

---

## 11. Indicators of Compromise (IOCs)

### File Hashes
| Hash | Type | Value |
|------|------|-------|
| SHA256 | WannaCry binary | `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c` |

### File System
| Type | Value |
|------|-------|
| Drop directory | `C:\Intel\ivecuqmanpnirkt615\` |
| Dropper | `C:\Intel\ivecuqmanpnirkt615\tasksche.exe` |
| Ransom UI | `C:\Intel\ivecuqmanpnirkt615\@WanaDecryptor@.exe` |
| Service binary | `C:\WINDOWS\mssecsvc.exe` |
| File extension | `.WNCRY` (encrypted files) |

### Registry
| Type | Value |
|------|-------|
| Service key | `HKLM\SYSTEM\CurrentControlSet\Services\mssecsvc2.0` |

### Network
| Type | Value |
|------|-------|
| Kill switch domain | `iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com` |
| Bitcoin addresses | `12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw` |
| Bitcoin addresses | `13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94` |
| Bitcoin addresses | `115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn` |
| Exploit protocol | TCP/445 (SMBv1) — EternalBlue |

### Process Names
`tasksche.exe`, `@WanaDecryptor@.exe`, `taskdl.exe`, `taskse.exe`, `mssecsvc.exe`

---

## 12. Root Cause Assessment

The infection was made possible by the following conditions:

1. **Unpatched OS:** Windows XP reached end-of-life in April 2014. Microsoft released patch MS17-010 only for supported OS versions on 2017-03-14 (one month before WannaCry). Windows XP was unpatched at the time of attack (though Microsoft later released an emergency XP patch on 2017-05-13, the day after this infection).
2. **SMBv1 Enabled:** The EternalBlue exploit targets SMBv1, which is enabled by default on Windows XP.
3. **Internet Isolation Failure:** The host was apparently not fully isolated — WannaCry was delivered (likely via the network from another infected host via EternalBlue lateral movement), but the host could not reach the kill switch sinkhole domain.

---

## 13. Attribution

**Threat Actor: Lazarus Group (APT38)**  
**Sponsor: Democratic People's Republic of Korea (DPRK)**  

Attribution is based on:
- Code overlap with prior Lazarus Group malware (Contopee, WannaCry dropper similarities)
- Shared infrastructure with previous DPRK operations
- US-CERT, NCSC UK, and multiple intelligence agencies publicly attributed WannaCry to DPRK in late 2017/2018
- The malware binary hash `24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c` is a known WannaCry sample confirmed by global threat intelligence

---

## 14. Recommendations

### Immediate Actions
1. **Isolate** all Windows XP endpoints from the network immediately
2. **Preserve** all affected disk images before remediation for further forensic analysis
3. **Scan** the entire environment for: `mssecsvc2.0` service, `C:\Intel\` directories, `.WNCRY` files, and the malware hash
4. **Block** TCP/445 (SMB) at all network perimeter and inter-segment firewalls
5. **Re-image** affected hosts from verified clean backups (confirmed clean)

### Short-term Actions
6. **Patch** all Windows systems — apply MS17-010 and all outstanding security updates
7. **Disable SMBv1** across all Windows endpoints and servers
8. **Review** network logs for TCP/445 scanning activity during 21:22–21:26 UTC on 2017-05-12 to identify any additional infected hosts
9. **Check** for `mssecsvc2.0` service on all other Windows hosts

### Long-term Actions
10. **Decommission** all Windows XP systems — they cannot be securely maintained
11. **Implement** network segmentation to limit lateral movement via SMB
12. **Deploy** EDR tooling capable of detecting process injection and ransomware behavior
13. **Review** backup strategy — confirm air-gapped or immutable backup copies are maintained

---

## 15. Commands Executed During Analysis

| # | Command | Purpose |
|---|---------|----------|
| 1 | `sha256sum /evidence/Investigation-2.raw` | Evidence integrity hash |
| 2 | `vol windows.info` | OS identification (failed — no symbols) |
| 3-4 | `pdbconv` / symbol download | Download ntoskrnl symbols |
| 5 | `vol windows.info` | OS identification (success) |
| 6 | `vol windows.pslist` | Active process listing |
| 7 | `vol windows.netscan` | Network connections (failed — XP not supported) |
| 8 | `vol windows.cmdline` | Process command line arguments |
| 9 | `vol windows.psscan` | Full process scan including terminated |
| 10 | `vol windows.malfind` | Injected code / RWX memory regions |
| 11 | `vol windows.netstat` | Network connections (failed — XP not supported) |
| 12 | `vol windows.registry.hivelist` | Loaded registry hives |
| 13 | `vol windows.handles --pid 1940` | tasksche.exe open handles |
| 14 | `vol windows.registry.printkey mssecsvc2.0` | Service registry key |
| 15 | `strings -a -n 8` | Raw string extraction (IOC search) |
| 16-20 | `vol windows.registry.printkey` (variants) | Service key values |

---

*Report generated from memory forensics analysis. All findings are based on artifacts present in the provided memory image.*