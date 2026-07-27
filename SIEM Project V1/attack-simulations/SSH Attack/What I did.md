2026-07-05



Created username and password list to brute force using hydra

Tested Hydra on Endpoint IV

Successful SSH brute force attack

Saw logs on SIEM system



2026-07-06

Simulated Attack again and this time captured on Wazuh



2026-07-09

Today I edited the videos of the DEMO(s)



2026-07-10

Today I ran into a problem where I cant find the keys for when I logged into ssh, I then learned that I used password login instead of key login, I can add a new part of this attack simulation by enabling key login and generating a new key to copy, so now I learned about that attack vector aswell, where a bad actor can enable key login and use a key to login instead of a password or vise versa.



I ran cat /etc/ssh/sshd\_config to see if key authentication is enabled

I learned that it is already enabled, so I just have to generate a new key and save it



I ran ssh-keygen -t ed25519 to generate a new key



Its not working so im going to watch a tutorial on how to use SSH key login

I watched a tutorial and learned that, to generate ssh keys I type ssh-keygen -t Encryption Algorithm, then to add it to the server I do ssh-copy-id USERNAME@USERNAME



2026-07-12



Today I documented what happens when I add a ssh key to the authorized key file for ssh and I saw I could login even though the password was changed. I also saw that it wasn't being detected on the SIEM so I edited the ossec.conf so that it monitors that file for changes



2026-07-14

Today I reset my vms to be fresh when I initiate the real attack vector.



2026-07-15

Today I downloaded suricata so that my wazuh can see the nmap scans. I changed the ossec.conf file so that it attaches to it properly.



2026-07-16

Today I configured suricata by adding a custom rule where if any scanner touches port 22, it triggers and alert.

alert tcp any any -> any 22 (msg:"SIEM PROJECT: Nmap Scan to SSH Port 22"; flags:S; sid:1000002; rev:1;)

I also made the rule for this entire attack simulation, I learned to read the docs and do it all myself



2026-07-17

Today I tested my rules to see if they worked, they didn't seem to be working as intended so I spent today adjusting my rules and testing



2026-07-18

Today I learned that the rule 86601 for Nmap Scan also triggers when I just ssh into the machine, which is a false positive.

I fixed it by excluding my ip address as the admin by using

suppress gen\_id 1, sig\_id 1000002, track by\_src, ip 10.0.0.xxx



I noticed that any time I just normally SSH into the target machine, my nmap scan rule would get triggered and I realize that that's a false positive so I try to adjust it. What I did was I excluded the admin IP, aka my IP address, from the rule so that I can SSH into it normally. I noticed that when I tried SSHing from my Kali Linux machine, it didn't trigger and I was looking into why. I realized that my Kali Linux virtual machine is set to NAT instead of bridge mode, which used the same IP as my computer, so it used the exclusion on that machine as well. I changed it to bridge mode and it worked and it was triggered. From the Kali Linux machine when I ran nmap and I logged into it



I then ran the script for me to run the entire attack simulation and it triggered rule 10012, which is the rule for the final account lockout. The target machine should be locked down now because it detected this attack pipeline where someone brute-forced into SSH and put a key there. Even though they change the password, they can still log



2026-07-19

I played around with some theory of how a SOAR will work and will implement a third party SOAR instead of writing local scripts for realism



2026-07-20

I tried to implement the SOAR response but I keep running into errors, I will try again next session



2026-07-21

Today I changed the script to a Python script and I tried to play around with the configuration and I'm getting really close to it because it's showing that it's showing on sudo tail -f /var/ossec/logs/active-responses.log that my script is running is just not running as intended so I'm just very close to solving that issue.



2026-07-22

Today I think I found the main problem as to why my script isn't triggering, I see that it's triggering sometimes even when I reset the environment so I can resimulate the attack but it doesn't seem to be triggering at the right time. That's when I noticed that it seems to trigger because the wool gets fired even after I reset the environment because I was testing it previously. I know that it fires as soon as the rule is triggered. I learned that I should reset all the log files and restart from scratch and then do it instantly and then simulate the attack as soon as I turn on the system, as soon as I turn on the siem system for fresh logs so that it triggers the first time.



My theory is right. It only triggers one time until I restart the agent.



It worked

Will Document what I did next session



Here is the precise breakdown of the changes we made and the exact files we edited:



\### 1. Python Remediation Script



\* \*\*File Edited:\*\* `/var/ossec/active-response/bin/soar-remediate-100012.py`

\* \*\*What we did:\*\*

\* Replaced the blocking, interactive `/usr/bin/passwd` command with the non-interactive `/usr/sbin/chpasswd` utility to prevent the script from hanging on input prompts.

\* Added secure string encoding (`.encode()`) to pass the emergency password directly into `chpasswd`.

\* Configured proper standard output and error redirection (`subprocess.PIPE`) for all system commands (including `iptables`, `passwd -e`, and `pkill`) to ensure clean execution.

\* Added an explicit `sys.exit(0)` at the end of the script to ensure clean termination.







\### 2. Bash Active Response Wrapper Script



\* \*\*File Edited:\*\* `/var/ossec/active-response/bin/soar-remediate-100012` (the Wazuh wrapper)

\* \*\*What we did:\*\*

\* Initially updated it to use `exec` and backgrounding (`\&`) to detach the Python process from Wazuh's tracking pipe, preventing Wazuh's execution queue from locking up.

\* Refined the wrapper to explicitly capture Wazuh's incoming JSON payload upfront using `read -r INPUT` and feed it back into the backgrounded Python process via `<<< "$INPUT"`, resolving the standard input starvation error.



2026-07-23 \*Simulation Day\*

I simulated the attack fully





