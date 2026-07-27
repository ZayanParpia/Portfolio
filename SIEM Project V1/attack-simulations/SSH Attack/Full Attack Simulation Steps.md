\# SSH Attack Simulation and Automated Incident Response Lab



This document outlines the step-by-step process for executing a real-world SSH brute-force attack simulation and the corresponding automated SIEM detection and containment configurations.



\---



\## ⚔️ Part 1: Attack Simulation Steps



\### Step 1: Reconnaissance

\* \*\*Action:\*\* Run an `nmap` scan against the target to verify port 22 is open.

\* \*\*SIEM Capture:\*\* Log network scanning activity, port probing anomalies, and initial connection attempts.



\### Step 2: Payload Preparation

\* \*\*Action:\*\* Create custom target lists in Kali Linux containing specific username and password combinations.

\* \*\*SIEM Capture:\*\* N/A (Local attacker activity).



\### Step 3: Brute Force Execution

\* \*\*Action:\*\* Execute a `hydra` command to launch the dictionary attack against the target's SSH service.

\* \*\*SIEM Capture:\*\* Detect high-frequency failed authentication attempts from a single source IP.



\### Step 4: Persistence Establishment

\* \*\*Action:\*\* Generate a new SSH keypair on the Kali machine (`ssh-keygen`) and plant it on the compromised host using `ssh-copy-id -i KEYNAME.pub SSHATTACK@XXX.XXX.XXX.XXX`.

\* \*\*SIEM Capture:\*\* Trigger the custom Wazuh detection rule for successful unauthorized SSH authentication and key modifications.



\---



\## 🛡️ Part 2: Automated Response Execution



Once the Wazuh custom detection rule fires, the active response script immediately executes the following containment steps:



\* \*\*Ingestion:\*\* Parses the Wazuh JSON alert to extract the attacker's source IP and the compromised target username.

\* \*\*Network Isolation:\*\* Commands `fail2ban` to instantly block the attacker's IP address at the firewall level.

\* \*\*Session Termination:\*\* Forcefully terminates (`pkill -9`) all active sessions, shells, and processes currently running under the target user.

\* \*\*Persistence Revocation:\*\* Empties the target user's `authorized\_keys` file to completely revoke planted SSH key access.

\* \*\*Credential Lockdown:\*\* Locks the target user's password by instantly rotating it to a highly secure, predetermined string to block future interactive password logins.

\* \*\*Access Level Demotion:\*\* Changes the target user's login shell to `/sbin/nologin` to completely prevent OS-level system access.



\---



\## ⚙️ Part 3: Automated Response Safeguard Configurations



To maintain administrative availability and server integrity during containment, ensure the following logic rules are explicitly configured:



\* \*\*Administrator Whitelisting:\*\* The specific Admin IP network is statically defined in the Wazuh global configurations to ensure legitimate administrative sessions are never disconnected or banned.

\* \*\*Root Protection Clause:\*\* The containment script contains an explicit safety check to ensure that if the targeted user is `root`, it bypasses user deletion/shell modification steps and instead safely rotates the root password to a secure emergency break-glass password without locking administrators out.



