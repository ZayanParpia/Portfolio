This is now a highly professional, evidence-based security report. It documents not just the *plan*, but the **validated outcomes** of your testing.

---

# Security Simulation Report: Linux Privilege Escalation & Persistence

**Date:** June 29, 2026

**Target:** Ubuntu CLI Endpoint (Endpoint II)

**Status:** In Progress (Phases 1-4 Verified)

## 1. Overview

This simulation validates Wazuh’s capability to detect Linux privilege escalation, persistence mechanisms, and suspicious administrative behavior. By performing controlled attacks and verifying detection logic, we move from theoretical monitoring to validated defense.

---

## 2. Infrastructure & Scope

* **Wazuh Infrastructure:** Manager, Sysmon for Linux, Auditd, Wazuh Dashboard.
* **Target:** Ubuntu CLI Endpoint (Endpoint II).

---

## 3. Simulation Execution & Results

| Phase | Activity | Status | Detection / Rule Logic |
| --- | --- | --- | --- |
| **1** | Failed Sudo Attempts | **Verified** | Custom Rule 100002 (3 attempts in 300s). |
| **2** | Successful Sudo Usage | **Verified** | Standard Wazuh alerts triggered. |
| **3** | Sudoers Modification | **Verified** | FIM alert generated on `/etc/sudoers`. |
| **4** | Persistence (Sudo Group) | **Verified** | Auditd tracked group membership change. |


---

## 4. Key Findings & Observations

* **Password Guessing:** The custom rule `100002` successfully identifies brute-force patterns on `sudo`.
* *Rule Logic:* `frequency="3"`, `timeframe="300"`, `if_matched_sid="5557"`.


* **Persistence Caveat:** Adding `testuser` to the `sudo` group grants passwordless access. This bypasses the logic for Phase 1 (Failed Sudo) for this specific account.
* **Visibility:** Successful integration of Auditd and FIM is providing high-fidelity logs for configuration changes.

---

