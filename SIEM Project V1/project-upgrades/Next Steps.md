\## Endpoint Expansion \& Monitoring Configuration



\### Virtualized Endpoints (VMware)



\#### Security Monitoring Lab

\- Add \*\*2 Ubuntu CLI endpoints\*\* using VMware.

\- Add \*\*1 Ubuntu CLI endpoint\*\* and \*\*1 Windows endpoint\*\* using VMware on the gaming laptop.



\### Endpoint Logging \& Telemetry



\#### Windows Endpoints

\- Install \*\*Sysmon\*\* on all Windows endpoints.



\#### Linux Endpoints

\- Install \*\*Sysmon for Linux\*\* on all Ubuntu endpoints.

\- Install \*\*auditd\*\* on all Linux endpoints for system auditing and event loggin

\- configure new endpoints to have auditd and Sysmon connected to Wazuh Server Logs



\### Wazuh Integration



\#### Centralized Monitoring

\- Connect all endpoints to the \*\*Wazuh Server\*\*.

\- Verify successful agent registration and communication.

\- Confirm log ingestion from:

&#x20; - Sysmon (Windows)

&#x20; - Sysmon for Linux

&#x20; - auditd

\- Validate all endpoints are functional and visible within the Wazuh dashboard.



\### STEPS FOR 2026-06-10

\- Installed and configured \*\*Sysmon for Linux\*\* on Endpoint IV. ✅

\- Installed and configured \*\*auditd\*\* on Endpoint IV. ✅



\### STEPS FOR 2026-06-11



\- Connected Ubuntu Endpoint IV to the \*\*Wazuh Server\*\*. ✅

\- Verified that endpoint IV is actively reporting to Wazuh. ✅

\- Confirmed log collection and endpoint visibility within the Wazuh dashboard. ✅



\### STEPS FOR 2026-06-12

Set up Sysmon for Windows on Windows Endpoint ✅



\### STEPS FOR 2026-06-14

Ensure that Sysmon is sending logs to Wazuh Server ✅



\### STEPS FOR 2026-06-15

Ensure all Endpoints work all together and collect screenshots to prove each endpoint is generating logs. ✅\*

Install Kali Linux to perform pen testing. ✅



\### STEPS FOR 2026-06-17

Make doc to collect screenshots ✅

Collect screenshots for lab ✅



List Attack Methods to use ✅







\### STEPS FOR 2026-06-18

Edit Screenshots to remove any sensitive information ✅

Recreate Diagram ✅



\### STEPS FOR 2026-06-19

Edit README.md for this dir for screenshots ✅

Post upgrades on LinkedIn and portfolio project ✅





\### STEPS FOR 2026-06-20



Start Creating Simulated Attacks from List and Document and add more simulations

Make what I learned doc for it to

