import sys
def isIn(w):
	with open('Data/NLSPARQL.train.feats.txt','r') as f:
		for line in f:
			a = line.split()
			if a!=[] and a[0] == w:
				return True
	return False

def map(w):
	with open('word.mapper','r') as f:
		for line in f:
			a = line.split()
			if a[0] == w:
				return a[1]
	with open('word.mapper','r') as f:
		for line in f:
			a = line.split()
			if a[1] == w:
				return a[1]
	return "<unk>"

arr = sys.argv
del(arr[0])
st=0

for s in arr:
	if not isIn(s):
		s="<unk>"
	print(str(st)+"\t"+str((st+1)) +"\t"+ str(s) + "\t" + str(s))
	st+=1

print(str(st))
