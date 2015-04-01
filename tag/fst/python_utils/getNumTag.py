import sys
arr = sys.argv
with open('learn_utils/tag2.txt','r') as f:
	for line in f:
		a = line.split()
		if arr[1] == a[1]:
			print a[0]