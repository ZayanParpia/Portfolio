

\# 🛡️ Linux Privilege Escalation Detection Project



Welcome to the \*\*Linux Privilege Escalation Detection\*\* project. This repository documents a systematic security simulation aimed at validating the detection capabilities of the \*\*Wazuh SIEM\*\* against common Linux exploitation techniques.



\---



\## 📋 Project Summary



This project follows a structured approach to security validation:



\* \*\*Phase 1: Failed Sudo Attempts\*\* – Detection of brute-force password guessing.





\* \*\*Phase 2: Successful Sudo Usage\*\* – Monitoring legitimate and escalated administrative activity.





\* \*\*Phase 3: Sudoers File Modification\*\* – Tracking unauthorized configuration changes via File Integrity Monitoring (FIM).





\* \*\*Phase 4: Persistence\*\* – Detecting when an account is added to the `sudo` group.





\* \*\*Phases 5-6 (Upcoming):\*\* Testing SUID binary creation and unauthorized `chmod`/`chown` abuse.







\---



\## 📂 Repository Structure



\* `Attack Simulation 1.png`: Lab architecture and simulation diagram.

\* `Outline.md`: The detailed strategic plan for the simulation.

\* `Next steps.md`: Roadmap for upcoming detection modules.

\* `What I learned.md`: Key takeaways and insights from this engineering exercise.

\* `Prompt.txt`: The original technical prompts used to structure this project.

\* `screenshots/`: Visual evidence of detection and Wazuh rule triggers.

\* `Endpoint II active.png`: Lab verification showing active host and failed sudo attempts.

\* `Rule 5557.png`: Detailed log of the failed password attempt detection.

\* `Rule 5403.png`: Alert verification for the first successful sudo session.

\* `Wazuh 510 Triggered.png`: Confirmation of system-level alerts.

\* `sudoers file edit.png`: Evidence of FIM alerts triggered by file modification.

\* `User Group MOD.png`: Documentation of user group escalation detection.







\---



\## 🚀 Key Technical Achievements



\* \*\*Custom Correlation Rules:\*\* Developed a specific rule (ID: 100002) to detect password guessing by correlating 3 failed attempts within a 5-minute window.





\* \*\*Layered Visibility:\*\* Combined \*\*Auditd\*\* for syscall monitoring and \*\*Wazuh FIM\*\* for critical file integrity, ensuring no configuration changes go unnoticed.





\* \*\*MITRE ATT\&CK Mapping:\*\* All activities have been mapped to MITRE tactics, providing a defensible framework for security posture evaluation.







\---



\## 🛠️ Infrastructure



\* \*\*SIEM:\*\* Wazuh (Manager \& Dashboard)

\* \*\*Monitoring Agents:\*\* Sysmon for Linux, Auditd

\* \*\*Target:\*\* Ubuntu CLI Endpoint (Endpoint II)



\---



\## 🚧 Status



> \[!NOTE]

> This project is currently \*\*Active\*\*. We have successfully verified Phases 1 through 4. SUID and Defense Evasion testing (Phases 5 \& 6) are currently in progress.



\---



\*Documentation maintained by Zayan Parpia\* 🚀

