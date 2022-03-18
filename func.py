#!/usr/local/bin/python3

import time
import sys

# Color class for console
class bcolors:
	ERR	 = '\033[41m\033[30m'
	INFO = '\033[42m\033[30m'
	OBJ = '\033[47m\033[30m'
	WARN = '\033[43m\033[30m'
	OKGREEN = '\033[92m'
	ENDC = '\033[0m'

eipList = []
eipStringList = []

region = 'us-east-1'
freetire = True

def eip():
	eipList = []
	eipDiscoveredStr = 'eipalloc-0515386b6d9e01fff	None	test	54.88.193.11\neipalloc-8015386b6d9e01ddd	i-45238759873	test2	100.99.193.7\neipalloc-7015386b6d9e01sss	i-95238759873	test3	110.77.193.8\n'
	eipDiscoveredList = eipDiscoveredStr[:-1].split('\n')
	newEipDiscoveredStr = f'[{region}]\n'
	for i in range(len(eipDiscoveredList)):
		eipStringList = eipDiscoveredList[i].split('\t')
		if eipStringList[1] == 'None':
			newEipDiscoveredStr += f'{eipStringList[0]}\tnot associated\t{eipStringList[2]}\t{eipStringList[3]}\n'
		else:
			newEipDiscoveredStr += f'{eipDiscoveredList[i]}\n'

	eipList.append(newEipDiscoveredStr)

	for res in eipList:
		sys.stderr.write(res)

def snap():
	snapshotSum = 0
	snapshotList = []
	snapshotDiscoveredStr = 'snap-0764aab316279fc88	2022-03-18T11:18:52.965Z	2\nsnap-6664aab316279fc88	2022-03-18T11:18:52.965Z	5\nsnap-9064ccb316279fc88	2022-03-18T11:18:52.965Z	3\n'
	if snapshotDiscoveredStr:
		snapshotDiscoveredList = snapshotDiscoveredStr[:-1].split('\n')
		newSnapshotDiscoveredStr = f'[{region}]\n'
		for i in range(len(snapshotDiscoveredList)):
			snapshotStringList = snapshotDiscoveredList[i].split('\t')
			snapshotSum += int(snapshotStringList[2])
			if int(snapshotStringList[2]) >= 5 and freetire:
				newSnapshotDiscoveredStr += f'{snapshotDiscoveredList[i]} >= 5Gb freetire overuse\n'
			else:
				newSnapshotDiscoveredStr += f'{snapshotDiscoveredList[i]}\n'
		if freetire and snapshotSum > 5:
			newSnapshotDiscoveredStr += f'{bcolors.WARN}Sum of snapshots overuse freetire -> {snapshotSum}Gb{bcolors.ENDC}\n'

		snapshotList.append(newSnapshotDiscoveredStr)

		for res in snapshotList:
			sys.stderr.write(res)


if __name__ == '__main__':

	eip()
	snap()

	exit(0)