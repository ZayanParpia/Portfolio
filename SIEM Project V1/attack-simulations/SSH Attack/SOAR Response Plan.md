\# SOAR Response: Rule 100012 Triggered



\## Trigger Condition

When Wazuh rule \*\*100012\*\* is triggered, the following automated response actions will be executed on the affected system.



\## Automated Response Actions



\### 1. Remove SSH Authorized Keys and Terminate Attackers Session

The contents of the SSH authorized keys file will be cleared to prevent unauthorized persistence through previously added SSH keys.



Target file: \~/.ssh/authorized\_keys





Action:

* Remove all existing SSH public keys.
* Prevent attackers from continuing access through compromised keys.
* Terminate Attackers session via their IP



\---



\### 2. Reset User Password

The affected user's password will be changed to a predefined secure emergency password (New password is NEWPASSWORD2468).



Action:

\- Replace the current password with a preset strong password.

\- Require password rotation after incident containment.



\---



\### 3. Block Network Traffic From Attacking IP (IP src from rule 100012)

All network traffic originating from the detected malicious IP address will be blocked.



Action:

\- Add a firewall rule blocking all traffic from the source IP.

\- Apply the block to all ports and protocols.



Example:

Source IP: <Detected\_Attacker\_IP>

Blocked Ports: All (-1)

Protocol: All

Action: Deny





\### 4. If attacker is inside machine terminate session.



\---



\## Incident Containment Goal

These actions are designed to immediately:

\- Remove potential attacker persistence.

\- Prevent continued unauthorized access.

\- Isolate the malicious source IP.

\- Reduce the impact of an active compromise.



\## Logging and Monitoring

After execution:

\- Record all response actions.

\- Generate an incident response log.

\- Continue monitoring for additional suspicious activity.

