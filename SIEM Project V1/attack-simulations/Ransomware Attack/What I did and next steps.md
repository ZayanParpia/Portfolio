August 25, 2026

Today I learned how to encrypt and decrypt files in python using the cryptography library



Next Steps for Next Session

Find out how to use asymmetric encryption on directories (https://www.youtube.com/watch?v=n0uJsqFGO4k)

test script on vm

find trigger for it on SIEM



August 26-28, 2026

I was learning how to make the python script to encrypt files in directories.

I learned about the cryptography library and the rsa library.



September 1, 2026

After a few days of learning how to make the script, I made the script using AESGCM for bulk encryption, I put the script in /scripts.



September 4, 2026



After a few hours of getting the errors



Sep 04 15:14:15 endpoint4 audisp-af\_unix\[35406]: Using default queue depth

Sep 04 15:14:15 endpoint4 audisp-af\_unix\[35406]: Couldn't bind af\_unix socket (Address already in use)

Sep 04 15:14:15 endpoint4 audisp-af\_unix\[35406]: audisp-af\_unix plugin exiting due to errors setting up socket

Sep 04 15:14:15 endpoint4 auditd\[35205]: plugin /sbin/audisp-af\_unix terminated unexpectedly

Sep 04 15:14:15 endpoint4 auditd\[35205]: plugin /sbin/audisp-af\_unix was restarted (10x)

Sep 04 15:14:15 endpoint4 audisp-af\_unix\[35413]: Using default queue depth

Sep 04 15:14:15 endpoint4 audisp-af\_unix\[35413]: Couldn't bind af\_unix socket (Address already in use)

Sep 04 15:14:15 endpoint4 audisp-af\_unix\[35413]: audisp-af\_unix plugin exiting due to errors setting up socket

Sep 04 15:14:16 endpoint4 auditd\[35205]: plugin /sbin/audisp-af\_unix terminated unexpectedly

Sep 04 15:14:16 endpoint4 auditd\[35205]: plugin /sbin/audisp-af\_unix has exceeded max\_restarts

PUT SCRIPT HERE

look at

https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/advanced-settings.html#who-data-monitoring



September 5, 2026



Today I found out that the whodata fires properly when using the /etc folder, going to dive into why now



September 6, 2026



I finally figured it out as to why whodata is only working inside the /etc folder, I found out that when I make new things inside the /root directory, whether it be a new file or directory, and make it track inside the ossec.conf file, then when I make changes to a file, it works completely fine. I realized that it wasn't working for user documents and user directories because when I tried making a new directory inside my user account and tried tracking it by adding a new monitoring line inside the ossec.conf file for that file using whodata, it worked perfectly.



I believe that this worked now because I needed to make a new file or directory that wasn't already there. The folders and files I was trying to track existed before I started configuring Whodata which likely caused an error because it didn't register it and it only registers new files/folders that I make after configuring the ossec.conf.



Next steps for September 7, 2026

Try to get the rule to fire

SO far i tested it and it dosent seem to be working for some reason. Fix it

Possibly because mock did something

SYNTAX ERROR IN CUSTOM RULES



September 7, 2026

I kinda got my custom rule to fire, I found out that syscheck.audit.process.ppid is blocking my rule from firing by removing that line and testing, so Im going to try and figure out why that is.



Steps for Sep 8

Figure out why rule isn't firing with same syscheck.audit.process.id



I found out that I needed to put just ppid ( I read the docs properly this time) for the rule to fire.

I got it to fire and will work on SOAR response next session



Sep 9, 2026



Create script for snapshot reverse



Today I looked at the script pipeline i wanted to create and It will go as follows



Ransomware is detected - Ransomware file is deleted - Script fires that goes to cloud and restores set files with same names and locations based on a json file that shows what files are where in the vm.



<<<<<<< HEAD
Sep 12, 2026



Today I created the script for the backup

I am now going to test it on the active response on wazuh



Sep 14, 2026

Right now Im deciding to add a HITL for the SOAR response when I restore the files


next steps for Sep 15, 2026

Remake script for no decrypt asking ✅

Create video demo ✅


next steps for Sep 17, 2026

Edit Video ✅

next steps for Sep 17, 2026

Collect Screenshots ✅

Disable API key ✅

Create README.md for what this attack vector did, false positives and any other information. ✅

Sanitize Scripts ✅

Create what I could do better doc  ✅

Create Pipeline doc  ✅

Edit Video ✅




>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa

Collect Screenshots for pipeline idea ✅


Format GitHub repo and portfolio website ✅

Create Diagram


<<<<<<< HEAD
Post on linkedin
=======
Post on github
>>>>>>> bf2ef8665fa386a8c6b9e8e1994a2a31b812cfaa





