2026-04-27
Today I will make the IAM role for this project
I will use PoLP by only giving the IAM role what it needs for the project, which consists of the following

------------------------------------------------------

EC2 Permissions

	ec2:CreateLaunchTemplate
	ec2:DescribeLaunchTemplates
	ec2:ModifyLaunchTemplate
	ec2:RunInstances
	ec2:TerminateInstances
	ec2:DescribeInstances
	ec2:DescribeInstanceStatus
	ec2:CreateSecurityGroup
	ec2:AuthorizeSecurityGroupIngress
	ec2:DescribeSecurityGroups
	ec2:CreateTags
	ec2:DescribeTags

Auto Scaling Permissions
	autoscaling:CreateAutoScalingGroup
	autoscaling:UpdateAutoScalingGroup
	autoscaling:DescribeAutoScalingGroups

VPC / Networking Permissions
	ec2:CreateVpc
	ec2:DescribeVpcs
	ec2:CreateSubnet
	ec2:DescribeSubnets
	ec2:CreateInternetGateway
	ec2:AttachInternetGateway
	ec2:DescribeInternetGateways
	ec2:CreateRouteTable
	ec2:CreateRoute
	ec2:AssociateRouteTable
	ec2:DescribeRouteTables

Load Balancing (ALB) Permissions
	elasticloadbalancing:CreateLoadBalancer
	elasticloadbalancing:DescribeLoadBalancers
	elasticloadbalancing:CreateListener
	elasticloadbalancing:DescribeListeners
	elasticloadbalancing:CreateTargetGroup
	elasticloadbalancing:RegisterTargets
	elasticloadbalancing:DescribeTargetGroups
	elasticloadbalancing:ModifyTargetGroup

IAM Permissions
	iam:PassRole

------------------------------------------------------

I created the IAM JSON in IAM_POLICY_AUTO_SCALING.txt
I also created the GitHub Repo for this project and init it

NEXT STEPS

Create the Main Auto-Scaling Feature

Create Outline.txt 


__________________________

2026-04-28
Today I created the VPC, SG, IGW, ALB, TG, and refined the IAM policy for my Account.

Next Steps

Design the Launch Template, create working ALB and create working Auto Scale group 

__________________________

2026/04/29
Today I created the Launch Template, Created the working ALB and created the Auto Scale Group.

Next 
Test Auto Scaling to see if it works as intended 
Create SSM login to EC2 Instances by creating SSM role for Launch Template 

2026-04-30

Tested Auto Scaling to see if it works as intended ✅
Create SSM login to EC2 Instances by creating SSM role for Launch Template ✅

NEXT STEPS  
Update Diagram ✅ 
Add CloudWatch and CloudWatch Alarms ✅

2026-05-05
Collect Screenshots and Videos ✅
Edit Video demo ✅
Create script for video ✅

2026-05-06
Edit Screenshots to blur private info ✅
Create Screenshot Explanations ✅

NEXT STEPS

2026-05-07
Edit Video demo 
Refine Outline
Upload to portfolio 
Upload to GitHub

Upload to portfolio 
Upload to GitHub

Get Final Screenshots from Auto-Scaling and target