\# SQL INJECTION DETECTION



\*\*Date:\*\* July 30, 2026

\*\*Target:\*\* Vulnerable Web Server

\*\*Status:\*\* Completed



\## 1. Overview



This simulation validates the ability of SIEM/Wazuh to detect SQL injection attempts against a vulnerable web application. The goal is to generate controlled SQL injection activity and determine whether Wazuh can identify suspicious requests and generate appropriate security alerts.



\## 2. Infrastructure \& Scope



\* \*\*SIEM Infrastructure:\*\* Wazuh Manager \& Dashboard, Sysmon for Linux, Auditd, journald

\* \*\*Target:\*\* Vulnerable Web Server running Apache 

\* \*\*Scope:\*\* SQL injection detection and alerting



\## 3. Simulation Execution \& Results



| Phase                             | Attack Simulation                                                                                                            | Target Log Source                                          | Detection / Rule Logic                                                                                                                                      |

| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |

| \*\*Attack: SQL Injection Attempt\*\* | Attacker sends controlled SQL injection payloads through vulnerable application parameters to test input validation          | Apache/NGINX access logs, application logs, Wazuh archives | Detect SQL injection indicators such as SQL keywords, suspicious query parameters, encoded payloads, and abnormal request patterns using custom Wazuh rules |

| \*\*Detection \& Alerting\*\*          | Wazuh analyzes the generated web server and application logs                                                                 | Wazuh Manager                                              | Generate an alert when requests match defined SQL injection indicators                                                                                      |

| \*\*Investigation\*\*                 | Security analyst reviews the generated alerts and identifies the source IP, timestamp, requested URL, and payload indicators | Wazuh Dashboard, OpenSearch, archived logs                 | Confirm that the SQL injection attempt was detected and determine the affected endpoint                                                                     |

| \*\*Response Validation\*\*           | Analyst documents the event and verifies that the detection provides enough information for investigation                    | Wazuh Dashboard and collected logs                         | Validate that the SIEM provides sufficient telemetry to investigate and respond to the SQL injection attempt                                                |

