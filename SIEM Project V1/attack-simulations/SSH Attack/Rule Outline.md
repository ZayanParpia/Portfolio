\### 📋 Custom Correlation Rule Outline: Multi-Stage SSH Kill-Chain



To achieve high-fidelity alerting, the SIEM tracks a stateful 15-minute correlation window across distinct event types mapped to the MITRE ATT\&CK Framework:



Phase 1: Reconnaissance (T1595.001)

&#x20; └── \[Log Ingestion]: Capture inbound network scanning signatures or port probing anomalies.

&#x20; └── \[Condition]: Match Nmap/recon network traffic indicators targeting the host.



Phase 2: Credential Access (T1110.001)

&#x20; └── \[Log Ingestion]: Track authentication subsystem telemetry.

&#x20; └── \[Condition]: Identify ≥ 3 sequential failed SSH authentication events from the same source IP.



Phase 3: Initial Access (T1021.004)

&#x20; └── \[Log Ingestion]: Monitor successful session initiation.

&#x20; └── \[Condition]: Capture a successful SSH authentication coming from that exact same source IP.



Phase 4: Persistence / Account Manipulation (T1098.004)

&#x20; └── \[Log Ingestion]: Core Syscheck File Integrity Monitoring (FIM).

&#x20; └── \[Condition]: Flag any creation, write, or modification event on the "\~/.ssh/authorized\_keys" file.



\[🚨 CRITICAL TRIGGER CONDITION]:

If Phase 1, Phase 2, Phase 3, and Phase 4 occur sequentially from the same Source IP within a strict 15-minute timeframe, escalate immediately to a High-Severity Alert (Level 15).





REFRENCES

https://attack.mitre.org/techniques/T1595/001/

https://attack.mitre.org/techniques/T1110/001/

https://attack.mitre.org/techniques/T1021/004/

https://attack.mitre.org/techniques/T1098/004/



