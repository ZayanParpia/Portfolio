# Terraform Capstone: Screenshot Explanations

Each entry covers what the screenshot shows, what Terraform created, and why it matters. Screenshots are grouped in the order the infrastructure is built: network, internet access, routing, load balancing, compute, security, and supporting services.

---

## 1. Network Foundation

### 1. VPC (`VPC.png`)

Shows **Terraform Web VPC**, the private network that holds everything else in the project. It uses the `10.0.0.0/16` range, is not the default VPC, and has DNS resolution enabled. Everything else (subnets, load balancer, servers) lives inside this boundary, which keeps the project isolated from other AWS resources.

### 2. VPC Connections (`VPC Connections.png`)

The VPC resource map is an at-a-glance view of the finished network: 5 subnets across `us-east-1a` and `us-east-1b`, 4 route tables, and 2 network connections (the main internet gateway and the NAT gateway). It proves that the pieces are wired together the way the design intended, with every subnet attached to the correct route table.

### 3. Subnet A (`Subnet A.png`)

A **private** subnet (`10.0.1.0/24`) in `us-east-1a`. It does not auto-assign public IPs and uses the "Subnet A & B" route table. The web server runs here, so it is never directly reachable from the internet, which is the main security benefit of a private subnet.

### 4. Subnet B, private (`Route Table Subnet B.png`)

The second private subnet (`10.0.2.0/24`) in `us-east-1b`, using the same "Subnet A & B" route table. It gives the Auto Scaling Group a second Availability Zone to launch servers in if one zone has problems or if the group scales out.

### 5. ALB Subnet (`ALB Subnet.png`)

A **public** subnet (`10.0.3.0/24`) in `us-east-1a` that auto-assigns public IPs and uses the ALB route table. The load balancer needs a public-facing home in this zone to accept traffic from the internet and forward it to the private servers.

### 6. ALB Subnet B (`Subnet B.png`)

The matching public subnet (`10.0.5.0/24`) in `us-east-1b`, also on the ALB route table. An Application Load Balancer must span at least two Availability Zones, so this subnet is what makes the ALB highly available. (Note: the file is named "Subnet B" but the screenshot is the *ALB* subnet B.)

### 7. NAT Subnet (`NAT Subnet.png`)

A small public subnet (`10.0.4.0/24`) in `us-east-1a` dedicated to the NAT gateway. NAT gateways have to sit in a public subnet with a route to the internet gateway, so this subnet exists purely to host it.

---

## 2. Internet Access

### 8. Main Internet Gateway (`Main IGW.png`)

The internet gateway named **main**, attached to the VPC. It is the VPC's door to the internet. Without it, nothing in the VPC (including the ALB and NAT gateway) could send or receive public traffic.

### 9. NAT Gateway (`IGW for NAT A.png`)

Shows **gw NAT A**, a public NAT gateway living in the NAT subnet with a private address of `10.0.4.179`. It lets servers in the private subnets reach out to the internet (for updates, package installs, and so on) while blocking anyone on the internet from connecting in.

### 10. Elastic IP for NAT (`Elastic IP for NAT A.png`)

The Elastic IP `44.217.254.54` (tagged **NAT-A-EIP**) attached to the NAT gateway. A public NAT gateway requires a fixed public address, and this is it. All outbound traffic from the private servers appears to come from this single IP.

---

## 3. Routing

### 11. Route Table NAT (`Route Table NAT.png`)

Attached to the NAT subnet. It sends `0.0.0.0/0` (all internet traffic) to the **internet gateway** and keeps `10.0.0.0/16` local. This is what makes the NAT subnet "public" and lets the NAT gateway actually reach the internet.

### 12. Route Table for Subnets A & B (`Route Table Conf for NAT.png`)

Attached to both private subnets. It sends `0.0.0.0/0` to the **NAT gateway** instead of the internet gateway. This is the key to the design: the private servers get outbound-only internet access through NAT, with no inbound exposure.

### 13. ALB Route Table (`ALB RT.png`)

Attached to both ALB subnets. It sends `0.0.0.0/0` to the **internet gateway**, which makes those subnets public so the load balancer can receive requests from users.

---

## 4. Load Balancing

### 14. Application Load Balancer (`ALB.png`)

**Terraform-Capstone-ALB** is an internet-facing Application Load Balancer, active across the two ALB subnets in `us-east-1a` and `us-east-1b`. It is the single public entry point: users hit its DNS name, and it forwards requests to healthy servers behind it. This hides the servers and spreads traffic across zones.

### 15. Target Group (`ALB Target Group.png`)

**terraform-capstone-tg** is the list of servers the ALB sends traffic to (instance targets, HTTP on port 80). It shows 1 total target and 1 healthy, 0 unhealthy, confirming the ALB can reach the application and that health checks pass.

### 16. EC2 on the Target Group (`EC2 On Target Group.png`)

Shows the registered target: the capstone web server instance on port 80 in `us-east-1a` with a **Healthy** status. This proves the Auto Scaling Group successfully registered its instance with the load balancer and that the app is responding.

---

## 5. Compute

### 17. EC2 Running (`Ec2 Running.png`)

The **capstone-web-server** instance, a running `t3.micro` in Subnet A. It has only a private IP (`10.0.1.34`) and no public IP, runs with the `test-ec2-role` IAM role, and requires IMDSv2 (a more secure way for the instance to read its own metadata). It was launched by the Auto Scaling Group and is the actual server hosting the app.

### 18. Auto Scaling Group (`Autoscale Group.png`)

Shows the Auto Scaling Group with desired capacity 1 and scaling limits of 1 to 3, built from a launch template (`t3.micro`, attached security group). It keeps one server running at all times, replaces it if it fails, and can scale up to three if needed. The launch template was created by the `GitHubActionsTerraform` role, showing that the deployment ran through the CI/CD pipeline.

---

## 6. Security

### 19. Security Group Rules (`Security Rules for Port 443 and 80 .png`)

**Security Rules Terraform Capstone** allows inbound HTTPS (TCP 443) and HTTP (TCP 80) from `0.0.0.0/0`, with one outbound rule. It acts as the firewall for the web traffic, opening only the two ports a website needs and nothing else (no SSH, no database ports).

### 20. IAM Roles (`IAM Roles.png`)

Three roles were created:

- **GitHubActionsTerraform** lets GitHub Actions deploy Terraform through OIDC, so no long-lived access keys are stored.
- **terraform-capstone-traffic-log-role** lets VPC Flow Logs write network traffic logs.
- **test-ec2-role** is the instance role attached to the web server.

Using roles instead of stored credentials follows least-privilege and keeps secrets out of the repository.

---

## 7. Supporting Services

### 21. S3 Buckets (`S3 Buckets.png`)

Four buckets in `us-east-1`:

- `terraform-capstone-s3` for project storage.
- `terraform-capstone-s3-logs` for logs.
- `terraform-capstone-s3-states` for Terraform's remote state file (created earlier, on October 2).
- `portfolio-web-logs-...` from an earlier project.

Keeping state in S3 makes deployments consistent and shareable, and the log bucket gives a place for audit and traffic records.

### 22. Docker Image (`Docker Image.png`)

A local Docker image named `terraform-capstone:latest` (about 1.22 GB, built 6 days earlier). It appears to be the containerized version of the project's app or deployment environment, used to build and test before pushing to AWS so the workflow is repeatable on any machine.

---

## How it all fits together

Users reach the **ALB** in the public subnets through the **internet gateway**. The ALB forwards requests on port 80 to the **web server** in a private subnet, managed by an **Auto Scaling Group**. The private server reaches the internet only outward, via the **NAT gateway** and its **Elastic IP**. **Security groups** limit the open ports, **IAM roles** handle permissions without stored keys, and **S3** holds the Terraform state and logs.