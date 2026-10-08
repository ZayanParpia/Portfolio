\# 🛡️ Home SIEM Lab Project Outline



\## 📌 Project Title

\*\*Home SIEM Lab: Ubuntu Server + Ubuntu Endpoint for Centralized Logging and Detection\*\*



\---



\# 📖 Project Summary



This project builds a small, realistic security monitoring lab for a student portfolio. The goal is to collect logs from an Ubuntu server and one Ubuntu Linux endpoint, analyze security events in a SIEM platform, and document the process in a way that reflects how a SOC analyst would work in an enterprise environment.



Future additions will include events such as controlled attacks, detection validation, additional endpoints, MITRE ATT\&CK mapping, alert tuning, and expanded monitoring to simulate a more realistic SOC environment.

\---



\# 🎯 Project Goal



The purpose of this lab is to practice:



\- Deploying a SIEM

\- Forwarding endpoint logs to a central server

\- Reviewing alerts and events

\- Learning how centralized monitoring works in real environments



This project is designed to stay:



\- 💸 Free

\- ⚡ Lightweight

\- 🖥️ Stable on older hardware

\- 📚 Beginner friendly



\---



\# 📦 Current Project Scope



This version of the project includes:



\- 🖥️ One Ubuntu Server instance as the SIEM host

\- 💻 One Ubuntu Linux endpoint as the monitored device



This version does \*\*not\*\* include yet:



\- ❌ Windows endpoints

\- ❌ Tablets

\- ❌ Attack simulations

\- ❌ Multiple virtual machines



These features will be added later as the lab expands.



\---



\# 🏗️ Lab Architecture



The old PC will act as the \*\*central SIEM server\*\*.



It will run:



\- 🐧 Ubuntu Server

\- 🛡️ Wazuh all-in-one stack



The Ubuntu laptop will act as the \*\*monitored endpoint\*\* and send logs to the SIEM server using the Wazuh agent.



This setup demonstrates centralized logging and endpoint monitoring in a simple but realistic environment.



\---



\# 🖥️ Hardware Overview



\## 🛡️ SIEM Server (Old PC)



| Component | Specification |

|---|---|

| 🧠 CPU | Intel Core i5-6400 @ 2.70GHz |

| 🧬 RAM | 16 GB DDR3 |

| 💾 Storage | Fanxiang S101 512GB SATA SSD |

| 🎮 GPU | Intel HD Graphics 530 |

| 🐧 OS | Ubuntu Server |



\### ✅ Why This Works



This hardware is strong enough for a lightweight SIEM lab if unnecessary services and virtual machines are avoided.



\---



\## 💻 Ubuntu Endpoint Laptop



| Component | Specification |

|---|---|

| 🧠 CPU | Intel Core i3-1005G1 |

| 🧬 RAM | 8 GB DDR4 |

| 💾 Free Storage | \~200 GB |

| 🐧 OS | Ubuntu Desktop |



This laptop will act as the monitored Linux endpoint.



\---



\# 🧰 Free Tools Used



\## 🐧 Ubuntu Server



Ubuntu Server provides a lightweight and stable Linux operating system for hosting the SIEM environment.



\### ✅ Why It Matters



\- Widely used in enterprise environments

\- Stable for server workloads

\- Free and open source

\- Excellent documentation and community support



\---



\## 🛡️ Wazuh



Wazuh is the main SIEM platform used in this project.



The Wazuh all-in-one installation includes:



\- 📥 Wazuh Server

\- 🗂️ Wazuh Indexer

\- 📊 Wazuh Dashboard



\### ✅ Why It Matters



\- Collects and analyzes logs

\- Detects suspicious activity

\- Provides dashboards and alerts

\- Commonly used in labs and professional environments

\- Completely free



\---



\## 📡 Wazuh Agent



The Wazuh agent will be installed on the Ubuntu endpoint.



\### ✅ Why It Matters



\- Sends logs from the endpoint to the SIEM server

\- Gives visibility into system activity

\- Allows centralized monitoring



Enterprise SOC teams commonly use endpoint agents for visibility and detection.



\---



\# 🛠️ Planned Build Order



\## 1️⃣ Install Ubuntu Server



Install Ubuntu Server on the old PC using a bootable USB drive.



\### 🎯 Purpose



\- Create the foundation for the SIEM environment

\- Provide a lightweight operating system for server workloads



\---



\## 2️⃣ Install Wazuh All-in-One



Install the Wazuh stack on the Ubuntu Server machine.



\### 🎯 Purpose



\- Create centralized log collection

\- Enable alerting and dashboard functionality

\- Store and visualize endpoint activity



\---



\## 3️⃣ Verify Dashboard Access



Access the Wazuh dashboard from another machine on the network.



\### 🎯 Purpose



\- Confirm the SIEM is working properly

\- Verify dashboard communication and web access



\---



\## 4️⃣ Prepare Ubuntu Endpoint



Install Ubuntu Desktop on the endpoint laptop if needed and fully update the system.



\### 🎯 Purpose



\- Create a monitored Linux endpoint

\- Simulate a real client machine



\---



\## 5️⃣ Install the Wazuh Agent



Install and register the Wazuh agent on the Ubuntu endpoint.



\### 🎯 Purpose



\- Forward logs to the SIEM server

\- Allow centralized monitoring and alerting



\---



\## 6️⃣ Verify Log Ingestion



Confirm the Ubuntu endpoint appears inside the Wazuh dashboard and verify logs are arriving correctly.



\### 🎯 Purpose



\- Ensure endpoint communication works properly

\- Validate the logging pipeline



\---



\## 7️⃣ Documentation



Document every major step using:



\-  📸 Screenshots

\- 📝 Configuration notes

\- 🗺️ Architecture diagrams

\- 📚 Short explanations



\### 🎯 Purpose



\- Make the project portfolio-ready

\- Demonstrate understanding of SIEM deployment workflows and Attack Methods



\---



\# 🌍 Why This Project Matters



This project demonstrates foundational SOC and SIEM concepts including:



\- 📡 Centralized logging

\- 👀 Endpoint visibility

\- 🚨 Security monitoring

\- 🔎 Alert analysis

\- 🖥️ Infrastructure management



These concepts are heavily used in:



\- 🏢 Security Operations Centers (SOCs)

\- ☁️ Cloud security environments

\- 🛡️ Enterprise security teams

\- 🧑‍💻 Managed Security Service Providers (MSSPs)



Building this lab helps develop practical skills that are difficult to learn through theory alone.



\---



\# 🚀 Future Expansion



After the base lab is stable, future improvements may include:



\- 🐧 Additional Linux endpoints

\- 🪟 Windows endpoints

\- 📊 Sysmon integration

\- ⚔️ Safe attack simulation

\- 🗺️ MITRE ATT\&CK mapping

\- 🔧 Detection tuning

\- 🖥️ Additional virtual machines

\- 🌐 Network monitoring tools



The goal is to expand gradually while keeping the environment stable and understandable.



\---



\# 📚 Documentation Standard



Every meaningful step in this project should include:



\- ✅ What was installed

\- ✅ Why it was installed

\- ✅ How it works

\- ✅ Screenshots when relevant

\- ✅ Problems encountered and fixes used



After each meaningful milestone, changes should be committed to GitHub.



\### 📌 Example Milestones



\- Ubuntu Server installation

\- Wazuh installation

\- Endpoint connection

\- Dashboard verification

\- Configuration changes



\---



\# ⏭️ Next Step



The next phase of the project is creating the detailed Ubuntu Server installation and Wazuh deployment guide.

