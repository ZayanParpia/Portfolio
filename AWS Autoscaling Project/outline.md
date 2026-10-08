PROJECT GOAL



In this project, I built a secure and scalable AWS web architecture centered around an EC2 Auto Scaling Group. My objective was to handle changing traffic automatically, maintain high availability, and apply real-world cloud security best practices. I designed the environment to behave like a production-ready system with stronger security, monitoring, and automation.



WHAT EACH PART DOES



ROUTE 53

I used Route 53 as the DNS layer so users can access my application through a domain name instead of an IP address. It routes incoming traffic to my load balancer efficiently.



AWS CERTIFICATE MANAGER (ACM)

I used ACM to provision and manage SSL/TLS certificates. This allowed me to enforce HTTPS so all user traffic is encrypted in transit.



APPLICATION LOAD BALANCER (ALB)

The ALB distributes incoming requests across multiple EC2 instances. It also performs health checks to ensure traffic is only sent to healthy instances.



VPC AND PRIVATE SUBNETS

I placed my EC2 instances inside private subnets within a VPC. This prevents direct internet access to the instances, reducing exposure and attack surface.



AUTO SCALING GROUP + EC2 INSTANCES

The Auto Scaling Group automatically launches or terminates EC2 instances based on demand. It keeps the application available and allows it to scale during traffic spikes.



CLOUDWATCH + CLOUDWATCH ALARMS

I used CloudWatch to monitor metrics like CPU usage and trigger alarms. These alarms help the system react to load changes by scaling the number of instances up or down.



CUSTOM IAM ROLES WITH LEAST PRIVILEGE

I created custom IAM roles for the project instead of using broad default permissions. Each role only had the exact permissions it needed, which strengthened security and followed the Principle of Least Privilege.



AWS SYSTEMS MANAGER (SESSION MANAGER)

Instead of opening SSH ports, I used Systems Manager Session Manager to securely access my EC2 instances. This removed the need for public access and reduced attack vectors.



AMAZON S3

I used S3 to store static assets and logs. This also helped with monitoring, auditing, and keeping important files separate from the application servers.



AMAZON CLOUDFRONT (OPTIONAL)

I added CloudFront to deliver static content faster through edge locations, improving performance and reducing latency.



HOW IT RELATES TO SECURITY



This architecture follows a defense-in-depth strategy. I secured the system at multiple layers by enforcing HTTPS with ACM, keeping EC2 instances private inside subnets, using security groups and NACLs to control traffic, eliminating SSH exposure with Session Manager, and applying custom IAM roles with strict least privilege.



My IAM design was one of the most important parts. I made sure that every service and instance only had the permissions it absolutely needed, which reduced the risk of privilege escalation or misuse.



WHAT I DID WITH CLI



I used the AWS CLI to go beyond the basic setup and build out the extra pieces of the project. Instead of relying only on the console, I used the CLI to create and configure additional IAM policies, automate parts of the Auto Scaling setup, and manage resources more efficiently and consistently.



This made my project feel closer to how cloud engineers work in real environments, where automation and repeatability matter.



WHAT I LEARNED



From this project, I learned how to design a system that is scalable, highly available, and secure at the same time.



I learned that Auto Scaling is not just about performance, but also resilience. I learned that security must be built into every layer, not added later. I also learned that least privilege IAM is critical for protecting cloud environments, private networking reduces risk, and monitoring plus automation are essential for real-world systems.



Using the CLI also showed me how deployments can be faster, more consistent, and easier to reproduce.



FINAL PROFESSIONAL SUMMARY



I built a secure AWS architecture where users connect through DNS and HTTPS, traffic is distributed by a load balancer, and EC2 instances run in private subnets managed by an Auto Scaling Group. Monitoring is handled through CloudWatch, access is secured using IAM and Session Manager, and my custom least-privilege IAM design ensures strong access control.



This project demonstrates my ability to combine scalability, security, and automation into a real-world cloud solution.

