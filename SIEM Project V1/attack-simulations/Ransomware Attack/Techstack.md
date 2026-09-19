# Tech Stack — Ransomware Detection & Automated Response Project

## Core Infrastructure
| Component | Role |
|---|---|
| Wazuh (Manager + Agent) | SIEM/XDR — FIM, log analysis, correlation rules, active response |
| Ubuntu Server 24.04 LTS | Victim host — runs Wazuh agent, target directory, backups |
| Kali Linux | Attacker host — delivers/executes the simulator, optional reverse shell |
| VMware (host-only/NAT network) | Virtualization/isolation for the lab |

## Attack Simulation
| Component | Role |
|---|---|
| `ransomware_sim.py` (Python 3 + `cryptography`/Fernet) | **The ransomware file** — safe, self-contained simulator: recursively walks the target directory, encrypts files in place with a Fernet key, and drops a ransom note (`README_RESTORE.txt`) in each affected folder. This is the artifact detected, killed, and remediated by the rest of the stack. |
| Delivery method (Netcat / Metasploit `msfvenom`) | Optional — reverse shell from Kali used to transfer and execute `ransomware_sim.py` on the victim host remotely, simulating initial access → execution |
| Atomic Red Team | Optional — standardized technique tests (T1486-aligned) to validate detections beyond the custom script |

## Detection Layer
| Component | Role |
|---|---|
| Wazuh syscheck (FIM) | Real-time monitoring of the target directory for mass file changes caused by `ransomware_sim.py` |
| auditd | Linux audit subsystem — watches the target directory, captures `exe=` and PID of the process (`ransomware_sim.py`) making changes |
| Wazuh `local_rules.xml` | Custom correlation rule: mass FIM events + auditd exe/PID → high-severity alert |

## Response / Recovery Layer
| Component | Role |
|---|---|
| Wazuh Active Response | Triggers the kill + delete + restore script on rule match |
| Bash script (active response) | Kills the `ransomware_sim.py` PID, deletes/quarantines the offending exe, rsyncs snapshot back |
| cron + rsync | Scheduled snapshot backups of the target directory (`/backup/snapshots/<timestamp>/`) |

## SOAR / Orchestration Layer
| Component | Role |
|---|---|
| Shuffle (self-hosted, free/open-source) or n8n | Receives Wazuh webhook, orchestrates notification/case creation |
| Slack or Email | Incident notification (process killed, file deleted, snapshot restored) |

## Frameworks / References
| Component | Role |
|---|---|
| MITRE ATT&CK | T1486 (Data Encrypted for Impact) primary mapping — maps directly to `ransomware_sim.py`'s behavior; T1059, T1490 as supporting techniques |
| Atomic Red Team | Technique-aligned test cases referenced for detection validation |

## Documentation / Version Control
| Component | Role |
|---|---|
| Git / GitHub | Version control, portfolio repo, README, architecture diagram |