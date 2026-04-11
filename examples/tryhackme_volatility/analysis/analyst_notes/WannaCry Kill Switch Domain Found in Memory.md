# WannaCry Kill Switch Domain Found in Memory

**URL found:** `http://www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`

This is the hardcoded WannaCry kill switch domain. WannaCry performs an HTTP GET to this URL before encrypting files. If a valid response is received, the malware terminates without encrypting.

## Significance
The domain was registered on 2017-05-12 ~15:00 UTC by security researcher Marcus Hutchins (MalwareTech). The system time of this capture is **21:26:32 UTC** (after the kill switch was activated). Since files ARE encrypted (`.WNCRY` files found), the machine was **unable to reach the kill switch domain** — indicating the machine was likely **network-isolated** or blocked from reaching the internet at the time of infection.

The domain being present in memory confirms the malware code was resident and executed, consistent with WannaCry behavior.