#!/usr/local/bin/python3

from curses.ascii import NUL
import os
import sys
import argparse
import subprocess

# Color class for console
class bcolors:
	ERR	 = '\033[41m\033[30m'
	INFO = '\033[42m\033[30m'
	OBJ = '\033[47m\033[30m'
	WARN = '\033[43m\033[30m'
	OKGREEN = '\033[92m'
	ENDC = '\033[0m'

# Key Options
def createParser():
	parser = argparse.ArgumentParser(prog = 'AWSdsr',
									usage = '%(prog)s --profile [PROFILE] --freetire -o [ojects ...]',
									description = 'Checking AWS Objects',
									allow_abbrev = False)
	parser.add_argument('--profile',
						type = str,
						nargs = '?',
						help = 'AWS IAM profile')
	parser.add_argument('--freetire',
						action='store_true',
						help = 'Show freetire overrun warnings')
	parser.add_argument('-o',
						dest = 'obj',
						nargs = "*",
						metavar = 'objects',
						help = 'Objects are we looking for')

	return parser

def lineCleaner(strLen_):
	cleaner = ' ' * strLen_
	return cleaner

# Methods for getting aws infrastructure objects in a profile
class getAwsObj:
# Instances
	def instance(self, profile_, regions_):
		dot = ''
		instanceList = []
		for region in regions_:
			searchStr = '| Searching Instances ' + dot
			sys.stdout.write(searchStr + '\r')
			instanceDiscovered = subprocess.check_output("aws ec2 describe-instances --query 'Reservations[*].Instances[*].{InstanceId:InstanceId,Name:Tags[?Key==`Name`].Value|[0]}' --profile %s --region %s --output text" % (profile_, region), shell = True).decode()
			if instanceDiscovered:
				if instanceDiscovered.count('\n') >= 2 and namespace.freetire:
					instanceList.append(f'{bcolors.WARN}[WARN]{bcolors.ENDC}[{region}] ! possible overrun freetire !\n' + f'{instanceDiscovered} \n')
				else:
					instanceList.append(f'[{region}]\n' + f'{instanceDiscovered}\n')
			dot += '.'
		sys.stdout.write(f'{lineCleaner(len(searchStr))}\r')
		return instanceList
# VPCs
	def vpc(self, profile_, regions_):
		dot = ''
		vpcList = []
		for region in regions_:
			searchStr = '| Searching VPC ' + dot
			sys.stdout.write(searchStr + '\r')
			vpcDiscovered = subprocess.check_output("aws ec2 describe-vpcs --query 'Vpcs[*].{VpcId:VpcId,Name:Tags[?Key==`Name`].Value|[0],CidrBlock:CidrBlock}' --profile %s --region %s --output text" % (profile_, region), shell = True).decode()
			if vpcDiscovered:
				vpcList.append(f'[{region}]\n' + f'{vpcDiscovered}\n')
			dot += '.'
		sys.stdout.write(f'{lineCleaner(len(searchStr))}\r')
		return vpcList
# EIPs
	def eip(self, profile_, regions_):
		dot = ''
		eipList = []
		eipStringList = []
		eipDiscoveredList = []
		for region in regions_:
			searchStr = '| Searching Elastic IP ' + dot
			sys.stdout.write(searchStr + '\r')
			eipDiscovered = subprocess.check_output("aws ec2 describe-addresses --query 'Addresses[*].{AllocationId:AllocationId,Name:Tags[?Key==`Name`].Value|[0],InstanceId:InstanceId,PublicIp:PublicIp}' --profile %s --region %s --output text" % (profile_, region), shell = True).decode()
			#print(eipDiscovered)
			if eipDiscovered:
				eipDiscoveredList = eipDiscovered[:-1].split('\n')
				for i in range(len(eipDiscoveredList)):
					eipStringList = eipDiscoveredList[i].split('\t')
					if eipStringList[1] == 'None':
						#eipList.append(f'{eipDiscoveredList[i]} !!! not associated \n')
						eipList.append(f'{bcolors.WARN}[WARN]{bcolors.ENDC}[{region}]\n{eipStringList[0]}\t{bcolors.WARN}not associated{bcolors.ENDC}\t{eipStringList[2]}\t{eipStringList[3]}\n')
					else:
						eipList.append(f'{eipDiscoveredList[i]}\n')
			#	eipList.append(f'[{region}]\n' + f'{eipDiscovered}\n')
			dot += '.'
		sys.stdout.write(f'{lineCleaner(len(searchStr))}\r')
		return eipList
# Snapshots
	def snapshots(self, profile_, regions_):
		dot = ''
		snapshotList = []
		for region in regions_:
			searchStr = '| Searching Snapshots ' + dot
			sys.stdout.write(searchStr + '\r')
			snapshotDiscovered = subprocess.check_output("aws ec2 describe-snapshots --owner-id self --query 'Snapshots[*].{SnapshotId:SnapshotId,VolumeSize:VolumeSize,Time:StartTime}' --profile %s --region %s --output text" % (profile_, region), shell = True).decode()
			if snapshotDiscovered:
				if snapshotDiscovered.count('\n') >= 2 and namespace.freetire:
					snapshotList.append(f'{bcolors.WARN}[WARN]{bcolors.ENDC}[{region}] ! possible overrun freetire !\n' + f'{snapshotDiscovered} \n')
				else:
					snapshotList.append(f'[{region}]\n' + f'{snapshotDiscovered}\n')
			dot += '.'
		sys.stdout.write(f'{lineCleaner(len(searchStr))}\r')
		return snapshotList

if __name__ == '__main__':

	parser = createParser()
	namespace = parser.parse_args()

	if not namespace.profile:
		sys.stderr.write(f"{bcolors.ERR}[err]{bcolors.ENDC} Profile not specified... exit \n")
		exit(1)

	USER_ID_command = "aws iam get-user --output text --profile %s | awk -F ':' '{print $5}'" % (namespace.profile)
	REGIONS_command = "aws --region us-east-1 ec2 describe-regions --output text --profile %s | cut -f4" % (namespace.profile)
	regionsList = subprocess.check_output(REGIONS_command, shell = True).decode().split()
	sys.stdout.write(bcolors.OKGREEN + 'Profile: ' + namespace.profile + '@' + subprocess.check_output(USER_ID_command, shell = True).decode() + bcolors.ENDC + '\n')

	#print(list(filter(lambda y: '__' not in y, dir(getAwsObj))))

	awsObj = getAwsObj()

	for method in filter(lambda x: x in filter(lambda y: '__' not in y, dir(getAwsObj)), namespace.obj):
		result = getattr(awsObj, method)(namespace.profile, regionsList)
		if result:
			sys.stderr.write(f'{bcolors.INFO}[info]{bcolors.ENDC} {method} found: \n')
			for res in result:
				sys.stderr.write(res)
		else:
			sys.stderr.write(f'{bcolors.INFO}[info]{bcolors.ENDC} {method} not found \n')

	sys.stderr.write('Search is over, bye. \n')
	exit(0)