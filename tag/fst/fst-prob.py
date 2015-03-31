import math

def getTagCount(tag):
	with open('tag.count','r') as f:
		for line in f:
			a = line.split()
			if a[1] == tag:
				return a[0]

def getTags():
	with open('tag.txt','r') as f:
		tag = []
		for line in f:
			a = line.split()
			tag = tag + [a[0]]
		return tag

with open('tok-tag.count','r') as f:
	for line in f:
		a = line.split()
		prob =  - math.log(float(a[0]) / float(getTagCount(a[2])))

		print("0 0 " + a[1] + " " + a[2] + " " + str(prob))

	tags = getTags()
	for tag in tags:
		print("0 0 <unk> " + tag + " " + str(1.0/len(tags)))
	print("0")