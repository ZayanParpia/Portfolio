\# 🦠 Ransomware Attack Simulation


<p align="center">
  <img src="Diagram.png" alt="Ransomware Detection and Recovery Pipeline" width="900">
</p>

\*\*Date:\*\* September 18, 2026

\*\*Platform:\*\* Wazuh SIEM

\*\*Attack Type:\*\* Ransomware / Mass File Encryption

\*\*MITRE ATT\&CK:\*\* `T1486 — Data Encrypted for Impact`



\---



\## 📌 Overview



This project demonstrates a \*\*ransomware attack-vector simulation\*\* inside my Wazuh SIEM lab.



The simulation uses a Python script to perform \*\*bulk file encryption\*\* against a monitored directory. The activity generates a large number of file modifications in a short period of time, followed by the creation of a ransomware-style note such as a `.txt`, `.md`, `.html`, or similar file.



The Wazuh detection pipeline correlates these events to identify behavior consistent with ransomware activity.



Once the final detection rule is triggered, a response workflow can be initiated to \*\*restore the affected files from a backup source\*\*.





\---



\## 🎯 Project Objectives



The goal of this simulation was to demonstrate how a SIEM can detect ransomware based on \*\*behavioral indicators\*\* rather than relying solely on a known malware signature.



The detection focuses on:



\* Rapid modification of multiple files

\* Multiple file changes originating from the same process

\* Creation of ransomware-style notification files

\* Event correlation across multiple Wazuh rules

\* MITRE ATT\&CK technique mapping

\* Triggering a recovery workflow after detection



\---



\## 🔄 Detection Pipeline



The detection logic follows a two-stage process:



```text

&#x20;                ┌───────────────────────┐

&#x20;                │   File Modification   	│

&#x20;                │       Events          	│

&#x20;                └───────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                ┌───────────────────────┐

&#x20;                │     Rule 550          	│

&#x20;                │  File Change Event    	│

&#x20;                └───────────┬───────────┘

&#x20;                            │

&#x20;                            │ Same PPID

&#x20;                            │ 10 events

&#x20;                            │ within 2 sec

&#x20;                            ▼

&#x20;                ┌───────────────────────┐

&#x20;                │     Rule 100234       	│

&#x20;                │ Possible Mass         	│

&#x20;                │ Encryption Detected   	│

&#x20;                └───────────┬───────────┘

&#x20;                            │

&#x20;                            │ Within 5 sec

&#x20;                            │

&#x20;                            ▼

&#x20;                ┌───────────────────────┐

&#x20;                │     Rule 100235       	│

&#x20;                │ Ransomware Detected   	│

&#x20;                └───────────┬───────────┘

&#x20;                            │

&#x20;                            ▼

&#x20;                ┌───────────────────────┐

&#x20;                │ Backup / Recovery     	│

&#x20;                │ Workflow Initiated    	│

&#x20;                └───────────────────────┘

```



\### Detection Logic



The pipeline is designed to reduce false positives by correlating \*\*two different behavioral indicators\*\*.



\### Stage 1 — Mass File Modification



If the \*\*same PPID\*\* is responsible for at least \*\*10 file-change events within 2 seconds\*\*, Wazuh generates a high-severity alert indicating possible mass encryption.



\### Stage 2 — Ransomware Note Detection



If the mass-encryption rule fires and a file with a ransomware-associated extension is subsequently created within \*\*5 seconds\*\*, the second rule triggers the final ransomware detection.



Examples of monitored extensions include:



```text

.md

.txt

.html

.htm

.png

.jpg

```



This combination provides stronger evidence than detecting either behavior independently.



\---



\# 🛡️ Wazuh Detection Rules



\## Rule 100234 — Possible Mass Encryption



```xml

<!-- Ransomwhere Attack -->

<group name="Ransomwhere Attack">



&#x20; <rule id="100234" level="15" frequency="10" timeframe="2">

&#x20;   <if\_matched\_sid>550</if\_matched\_sid>

&#x20;   <same\_field>ppid</same\_field>



&#x20;   <description>Possible Mass Encryption Detected</description>



&#x20;   <mitre>

&#x20;     <id>T1486</id>

&#x20;   </mitre>



&#x20;   <group>ransomware,</group>

&#x20; </rule>

```



\### What it detects



Rule `100234` looks for a rapid sequence of file-change events associated with the \*\*same PPID\*\*.



| Condition         |       Value |

| ----------------- | ----------: |

| Base Rule         |       `550` |

| Required Events   |        `10` |

| Time Window       | `2 seconds` |

| Correlation Field |      `PPID` |

| Severity          |        `15` |

| MITRE ATT\&CK      |     `T1486` |



This provides the first indication that a single process may be performing mass file modifications.



\---



\## Rule 100235 — Ransomware Detected



```xml

&#x20; <rule id="100235" level="16" timeframe="5">

&#x20;   <if\_matched\_sid>100234</if\_matched\_sid>

&#x20;   <if\_sid>554</if\_sid>



&#x20;   <field name="file" type="pcre2">

&#x20;     (?i)\\.(md|txt|html|htm|png|jpg)$

&#x20;   </field>



&#x20;   <description>

&#x20;     Ransomwhere Detected. Run Backup Scripts!...

&#x20;   </description>

&#x20; </rule>



</group>

```



\### What it detects



Rule `100235` acts as the \*\*final correlation rule\*\*.



It requires:



1\. Rule `100234` to have already triggered.

2\. A file-change event associated with Rule `554`.

3\. The affected file to match one of the monitored extensions.

4\. The event to occur within the configured `5-second` timeframe.



When these conditions are met, Wazuh raises a \*\*Level 16 ransomware detection\*\*.



\---



\# 🧠 Why Correlate Multiple Events?



Detecting a single modified file is not enough to confidently identify ransomware.



Legitimate applications constantly modify files. A text editor, image editor, compiler, browser, or software updater could all generate file-change events.



Instead, this project looks for a \*\*sequence of behaviors\*\*:



```text

Single File Change

&#x20;      │

&#x20;      ▼

&#x20;  Normal Activity

&#x20;      

&#x20;      ↓



10+ File Changes

Same PPID

Within 2 Seconds

&#x20;      │

&#x20;      ▼

Possible Mass Encryption

&#x20;      │

&#x20;      ▼

Ransomware-Style File Created

&#x20;      │

&#x20;      ▼

Ransomware Detected

```



The correlation between these events provides a stronger behavioral signal for ransomware activity.



\---



\# 🧪 Attack Simulation



The simulation uses a Python script to perform \*\*bulk encryption\*\* against files inside a monitored directory.



The simulated attack demonstrates:



\* Python-based encryption

\* AES-GCM encryption

\* Bulk file processing

\* Symmetric encryption

\* File modification at scale

\* Ransomware-note creation

\* SIEM event generation

\* Wazuh rule correlation



The objective is not to create real-world malware, but to reproduce the \*\*observable behaviors\*\* that a defensive security system should be capable of detecting.



\---



\# 💾 Recovery Workflow



After the ransomware detection is triggered, a recovery workflow can be initiated to restore the affected files from a backup source.



For this project, the recovery workflow uses \*\*Google Drive\*\* as the backup location.



```text

Ransomware Detection

&#x20;       │

&#x20;       ▼

Wazuh Alert

&#x20;       │

&#x20;       ▼

Recovery Script

&#x20;       │

&#x20;       ▼

Google Drive Backup

&#x20;       │

&#x20;       ▼

Restore Files

&#x20;       │

&#x20;       ▼

Working Directory Recovered

```



This demonstrates how SIEM detection can be connected to a broader \*\*incident-response and recovery workflow\*\*.



\---



\# 🧰 Technologies \& Concepts



\### SIEM \& Detection



\* \*\*Wazuh\*\*

\* Wazuh custom rules

\* Event correlation

\* File Integrity Monitoring

\* Behavioral detection

\* MITRE ATT\&CK mapping



\### Programming



\* \*\*Python\*\*

\* File automation

\* Encryption libraries

\* Backup/recovery scripting



\### Cryptography



\* \*\*AES-GCM\*\*

\* Symmetric encryption

\* Asymmetric encryption

\* Encryption at scale



\### Incident Response



\* Ransomware detection

\* Automated response

\* Backup restoration

\* File recovery

\* Detection → Response → Recovery workflow



\---



\# 🧠 What I Learned



Through this simulation, I gained practical experience with:



\* Designing behavioral SIEM detections

\* Creating custom Wazuh rules

\* Correlating multiple security events

\* Using process information such as PPIDs for detection

\* Mapping detections to \*\*MITRE ATT\&CK\*\*

\* Writing Python security automation scripts

\* Understanding AES-GCM encryption

\* Understanding the difference between symmetric and asymmetric encryption

\* Simulating bulk file encryption

\* Building a basic ransomware response workflow

\* Connecting detection with backup and recovery



\---



\# 🔧 Areas for Improvement



There are several areas I would improve in a future version of this project.



\### 1. Automated Response with SOAR



I could integrate a \*\*SOAR platform\*\* or open-source automation tooling to automatically respond to the alert.



A future workflow could:



```text

Ransomware Detected

&#x20;       ↓

Isolate Endpoint

&#x20;       ↓

Terminate Malicious Process

&#x20;       ↓

Preserve Evidence

&#x20;       ↓

Restore Files

&#x20;       ↓

Generate Incident Report

```



This would provide a more complete \*\*detection → containment → recovery\*\* workflow.



\---



\### 2. Snapshot-Based Recovery



Another improvement would be implementing \*\*snapshot-based restoration\*\*.



Instead of relying solely on a backup copy, filesystem or virtual-machine snapshots could provide a faster method of reverting affected files to a known-good state.



This would also allow me to investigate how snapshot-based recovery can be incorporated into ransomware response procedures.



\---



\### 3. Persistence Removal



A future version of the project could also investigate how to identify and remove potential \*\*persistence mechanisms\*\* following a ransomware incident.



This would expand the project beyond simply detecting encryption activity and into the broader incident-response lifecycle.



\---



\# 📚 MITRE ATT\&CK Mapping



| Technique                 | ID        | Relevance                                                                         |

| ------------------------- | --------- | --------------------------------------------------------------------------------- |

| Data Encrypted for Impact | \*\*T1486\*\* | Simulated ransomware encrypts files to demonstrate encryption-for-impact behavior |



\*\*MITRE ATT\&CK:\*\* `T1486 — Data Encrypted for Impact`



\---



\# 📊 Project Workflow



Overall, the project demonstrates the following security workflow:



```text

┌──────────────┐

│ Attack       │

│ Simulation   │

└──────┬───────┘

&#x20;      │

&#x20;      ▼

┌──────────────┐

│ File Changes │

│ Generated    │

└──────┬───────┘

&#x20;      │

&#x20;      ▼

┌──────────────┐

│ Wazuh FIM    │

│ Events       │

└──────┬───────┘

&#x20;      │

&#x20;      ▼

┌──────────────┐

│ Rule 100234  │

│ Mass Changes │

└──────┬───────┘

&#x20;      │

&#x20;      ▼

┌──────────────┐

│ Ransomware   │

│ Note Created │

└──────┬───────┘

&#x20;      │

&#x20;      ▼

┌──────────────┐

│ Rule 100235  │

│ Detection    │

└──────┬───────┘

&#x20;      │

&#x20;      ▼

┌──────────────┐

│ Recovery     │

│ Workflow     │

└──────────────┘

```



\---



\## 🚀 Future Improvements



\* Integrate SOAR automation

\* Automatically isolate the affected endpoint

\* Automatically terminate the responsible process

\* Implement snapshot-based recovery

\* Improve ransomware-note detection

\* Expand file-extension detection

\* Add additional MITRE ATT\&CK mappings

\* Improve false-positive resistance

\* Add automated incident reporting

\* Investigate persistence detection and removal



\---



\## 📸 Evidence \& Project Structure



The ransomware simulation is organized into separate directories for \*\*screenshots, scripts, detection rules, and demonstration footage\*\*.



```text

Ransomware/

│

├── 📸 Screenshots/

│   └── Pipeline for Rules Working.png

│       └── Shows the Wazuh detection pipeline

│           and the rules being triggered

│

├── 🐍 Scripts/

│   ├── Mock\_data.py

│   │   └── Creates mock file-change data for testing

│   │

│   ├── Ransomware Script.py

│   │   └── Simulates the ransomware attack

│   │

│   └── RestoreBackup.py

│       └── Restores affected files from backup

│

├── 🛡️ Rules/

│   └── Ransomwhere Attack.xml

│       └── Wazuh detection rules used for

│           the ransomware attack simulation

│

└── 🎥 Video/

&#x20;   └── Demo.mp4

&#x20;       └── Demonstrates the complete detection

&#x20;           and response pipeline

```



\### 📂 Directory Overview



| Directory         | Purpose                                                                |

| ----------------- | ---------------------------------------------------------------------- |

| 📸 `Screenshots/` | Visual evidence of the Wazuh detection pipeline                        |

| 🐍 `Scripts/`     | Python scripts used to generate, simulate, and recover from the attack |

| 🛡️ `Rules/`      | Custom Wazuh rules used to detect the simulated ransomware activity    |

| 🎥 `Video/`       | Demonstration of the complete attack and detection pipeline            |



\### 📸 Screenshot



\*\*`Pipeline for Rules Working.png`\*\*



Shows the Wazuh detection pipeline in action, including the custom ransomware rules being triggered during the simulation.



\### 🐍 Scripts



\* \*\*`Mock\_data.py`\*\* — Generates mock data used to test the detection pipeline.

\* \*\*`Ransomware Script.py`\*\* — Simulates bulk file encryption and ransomware-style activity.

\* \*\*`RestoreBackup.py`\*\* — Restores the affected files from the backup source.



\### 🛡️ Detection Rules



\*\*`Ransomwhere Attack.xml`\*\*



Contains the custom Wazuh rules used to correlate file-change activity and identify the simulated ransomware behavior.



\### 🎥 Demonstration



\*\*`Demo.mp4`\*\*



Demonstrates the complete ransomware simulation pipeline, from the simulated attack through Wazuh detection and the recovery process.


## 📸 Ransomware Attack Simulation Screenshots

The `/screenshots` directory contains screenshots documenting the different stages of the ransomware attack simulation, from the initial backup process through file encryption, detection, and recovery.

## 1. 💾 Backup Script Running

**`Backup Script Running.png`**

Shows the backup script actively running before the ransomware simulation. The script creates backups of the files that will later be affected by the simulated attack.

![Backup Script Running](<screenshots/Backup Script Running.png>)

---

## 2. 📁 Files Before the Attack

**`Files of DIR before.png`**

Shows the contents of the target directory **before** the ransomware simulation begins. The files are still in their original, readable state.

![Files Before Attack](<screenshots/Files of DIR before.png>)

---

## 3. 📄 Plaintext Files Before Ransomware

**`Files in DIR in plaintext before Ransomware Script.png`**

Provides a closer view of the target files while they are still stored as normal plaintext files immediately before the ransomware script is executed.

![Plaintext Files Before Ransomware](<screenshots/Files in DIR in plaintext before Ransomware Script.png>)

---

## 4. 🐍 Ransomware Simulation Running

**`Running Ransomware Script.png`**

Shows the ransomware simulation script being executed against the test directory.

This represents the **attack simulation phase** of the project.

![Running Ransomware Script](<screenshots/Running Ransomware Script.png>)

---

## 5. 🔐 Files Being Encrypted

**`Ransomware Script Encrypted Contents.png`**

Shows the ransomware simulation processing the files and encrypting their contents.

This demonstrates the simulated impact of the attack on the test data.

![Ransomware Script Encrypted Contents](<screenshots/Ransomware Script Encrypted Contents.png>)

---

## 6. 🔒 Directory After Encryption

**`Files in DIR now Encrypted.png`**

Shows the target directory after the ransomware simulation has completed.

The previously readable files are now represented in their encrypted state.

![Encrypted Files](<screenshots/Files in DIR now Encrypted.png>)

---

## 7. 📝 Ransomware Note Created

**`Ransomware Note Made.png`**

Shows the ransom note generated by the simulation after the files have been encrypted.

This represents the notification behavior commonly associated with ransomware and provides an additional detection indicator for the SIEM.

![Ransomware Note](<screenshots/Ransomware Note Made.png>)

---

## 8. 🛡️ Wazuh Detection Pipeline

**`Pipeline for Rules Working .png`**

Shows the Wazuh detection pipeline processing the simulated ransomware activity.

This demonstrates the custom security rules being triggered and the detection pipeline functioning as designed.

![Wazuh Detection Pipeline](<screenshots/Pipeline for Rules Working .png>)

---

## 9. 🚨 Bulk File Changes Detected by SIEM

**`Bulk File Changes Detected by SIEM.png`**

Shows the SIEM detecting the large number of file changes generated by the ransomware simulation.

The rapid modification activity serves as an indicator of potentially malicious behavior.

![Bulk File Changes Detected](<screenshots/Bulk File Changes Detected by SIEM.png>)

---

## 10. ♻️ Files Restored

**`Files back in Plaintext.png`**

Shows the files after the recovery process has restored them to their original readable state.

This demonstrates the **final recovery stage** of the simulation.

![Files Restored](<screenshots/Files back in Plaintext.png>)

---

### 🔄 Simulation Flow

The screenshots collectively demonstrate the complete lifecycle of the lab:

```text
Backup
  ↓
Files in Original State
  ↓
Ransomware Simulation Executed
  ↓
Files Encrypted
  ↓
Ransom Note Created
  ↓
SIEM Detects Bulk File Changes
  ↓
Security Rules / Pipeline Responds
  ↓
Files Restored from Backup
  ↓
Files Back in Plaintext

\# 🏁 Conclusion



This project demonstrates how a SIEM can detect ransomware-like behavior by correlating \*\*rapid file modifications, process relationships, and ransomware-note creation\*\*.



Rather than relying on a single indicator, the detection pipeline uses multiple events to increase confidence that the activity represents a potential ransomware attack.



The project also demonstrates the importance of connecting \*\*detection with response and recovery\*\*, creating a workflow that extends beyond simply generating a SIEM alert.



> \*\*Attack Simulation → Detection → Correlation → Response → Recovery\*\*



This project forms part of my broader \*\*Wazuh Home SIEM Lab\*\*, where I am building and testing practical security monitoring, detection engineering, attack simulation, and incident-response capabilities.



