#!/usr/local/bin/python3

import time
import sys

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
	snapshotList = []
	snapshotDiscoveredStr = 'snap-0764aab316279fc88	2022-03-18T11:18:52.965Z	2\nsnap-6664aab316279fc88	2022-03-18T11:18:52.965Z	5\nsnap-9064ccb316279fc88	2022-03-18T11:18:52.965Z	4\n'
	if snapshotDiscoveredStr:
		snapshotDiscoveredList = snapshotDiscoveredStr[:-1].split('\n')
		newSnapshotDiscoveredStr = f'[{region}]\n'
		for i in range(len(snapshotDiscoveredList)):
			snapshotStringList = snapshotDiscoveredList[i].split('\t')
			if int(snapshotStringList[2]) >= 5 and freetire:
				newSnapshotDiscoveredStr += f'{snapshotStringList[0]}\t{snapshotStringList[1]}\t{snapshotStringList[2]} >= 5Gb included in freetire\n'
			else:
				newSnapshotDiscoveredStr += f'{snapshotDiscoveredList[i]}\n'

		snapshotList.append(newSnapshotDiscoveredStr)

		for res in snapshotList:
			sys.stderr.write(res)


if __name__ == '__main__':

	eip()
	snap()

	exit(0)