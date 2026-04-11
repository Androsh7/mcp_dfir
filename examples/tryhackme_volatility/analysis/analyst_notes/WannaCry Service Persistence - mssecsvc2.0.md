# WannaCry Service Persistence - mssecsvc2.0

## Registry Key Confirmed
`SYSTEM\CurrentControlSet\Services\mssecsvc2.0` present across ALL registry hives:
- `WINDOWS\system32\config\system` (primary system hive)
- `WINDOWS\system32\config\software`
- User hives for: donny, LocalService, NetworkService

## Service Binary
- Service name: **mssecsvc2.0**
- Executable: **mssecsvc.exe** (found in memory strings)
- Typical path: `%SystemRoot%\mssecsvc.exe` (i.e., `C:\WINDOWS\mssecsvc.exe`)

## Function
The `mssecsvc2.0` service is WannaCry's worm component — it listens for SMB connections and propagates to other machines via the **EternalBlue (MS17-010)** exploit. This allows WannaCry to spread laterally without user interaction.

## Subkey
`SYSTEM\CurrentControlSet\Services\mssecsvc2.0\Parameters` also confirmed — service configuration data stored here.