#!/usr/local/bin/python3

import boto3

boto3.setup_default_session(profile_name='admin')
ec2_client = boto3.client("ec2", region_name="us-east-1")
response = ec2_client.describe_vpcs()
print(response)
for vpc in response['Vpcs']:
	print(vpc['VpcId'])
	print(vpc['CidrBlock'])
