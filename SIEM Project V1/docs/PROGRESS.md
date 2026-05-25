\## 2026-05-06

\- Created the GitHub repository structure for the Home SIEM Lab project.

\- Organized initial project directories to establish a clean and scalable foundation.



\## 2026-05-10

\- Verified system services using:

&#x20; - `sudo systemctl status wazuh-manager`

&#x20; - `sudo systemctl status wazuh-dashboard`

&#x20; - `sudo systemctl status wazuh-indexer`

\- Confirmed Wazuh components were installed and running on the system.

\- Identified that the current Wazuh version (4.7.5) is outdated and requires an upgrade to a supported version (4.14+).



\## 2026-05-11

\- Troubleshot Wazuh upgrade issues for several hours due to installation and dependency errors.

\- Followed the official Wazuh installation documentation to resolve upgrade-related issues:

&#x20; https://documentation.wazuh.com/current/installation-guide/wazuh-server/step-by-step.html

\- Continued debugging the upgrade process to ensure compatibility with the latest supported Wazuh release (V4.14.5.)


\## 2026-05-12
\- Used sudo systemctl status wazuh-manager to check the SIEM manager service status and confirmed it was not running
\- Started the Wazuh manager using sudo systemctl start wazuh-manager and verified it was active
\- Downloaded and installed the Wazuh all-in-one SIEM stack using curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh followed by bash wazuh-install.sh --all-in-one
\- Restarted all Wazuh services using sudo systemctl restart wazuh-manager, sudo systemctl restart wazuh-indexer, and sudo systemctl restart wazuh-dashboard to ensure full SIEM functionality
\- Configured Ubuntu laptop endpoint and registered it to the SIEM using agent-auth -m <SIEM_IP>
\- Successfully connected the Ubuntu laptop endpoint to the Wazuh SIEM server and verified active log forwarding and monitoring

## 2026-05-14 - Sysmon Installation & Endpoint Telemetry Setup

### Actions
- Learned to format GitHub project logs more effectively for SOC lab documentation and reproducibility
- Updated and upgraded Ubuntu system packages to ensure stability and compatibility
  sudo apt update && sudo apt upgrade -y
- Installed prerequisite packages required for secure repository management and software installation
  sudo apt install wget curl gnupg apt-transport-https -y
- Added official Microsoft package repository to enable installation of Sysmon for Linux
  wget -q https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  sudo apt update
- Installed Sysmon for Linux for enhanced endpoint telemetry collection
  sudo apt install sysmonforlinux -y
- Created a custom Sysmon configuration file to enable core telemetry visibility (process creation, network connections, file creation)

### Outcome
- Endpoint telemetry collection successfully enabled on Ubuntu system using Sysmon for Linux
- System is now capable of generating enhanced security logs suitable for SIEM ingestion
- Environment is prepared for next phase: integration with Wazuh agent and centralized log analysis

## 2026-05-15 
### Actions
- Downloaded Linux Audit Logging by using sudo apt install auditd audispd-plugins -y
- Edited Diagram

## 2026-05-17
### Actions
- Refined README.md to include polished documentation of project 
- Refined OUTLINE.md

### 2026-05-22
## Actions
- Toady I collected the screenshots for the project
-Create .gitignore file to ignore screenshots for now
