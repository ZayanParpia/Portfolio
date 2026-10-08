&#x20;       try:

&#x20;           check\_rule = subprocess.run(\["/usr/sbin/iptables", "-C", "INPUT", "-s", src\_ip, "-j", "DROP"],

&#x20;                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

&#x20;           if check\_rule.returncode != 0:

&#x20;               subprocess.run(\["/usr/sbin/iptables", "-A", "INPUT", "-s", src\_ip, "-j", "DROP"], check=True)

&#x20;               log\_action(f"SUCCESS: Blocked source IP via iptables: {src\_ip}")

&#x20;           else:

&#x20;               log\_action(f"NOTICE: IP {src\_ip} is already blocked.")

&#x20;       except Exception as e:

&#x20;           log\_action(f"ERROR applying network block for {src\_ip}: {e}")

&#x20;   else:

&#x20;       log\_action(f"NOTICE: Skipping IP block, invalid src\_ip: {src\_ip}")



&#x20;   # Action 4: Terminate Active Sessions

&#x20;   try:

&#x20;       subprocess.run(\["/usr/bin/pkill", "-u", user], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

&#x20;       log\_action(f"SUCCESS: Terminated active sessions for user: {user}")

&#x20;   except Exception as e:

&#x20;       log\_action(f"ERROR terminating sessions: {e}")



&#x20;   log\_action("SOAR Response execution cycle finished for Rule 100012.")

&#x20;   sys.exit(0)



if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   main()

