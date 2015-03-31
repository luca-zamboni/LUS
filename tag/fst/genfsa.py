import sys
def isIn(w):
	with open('lex.lex','r') as f:
		for line in f:
			a = line.split()
			if a[0] == w:
				return True
	return False

arr = sys.argv
del(arr[0])
st=0

for s in arr:
	if not isIn(s):
		s = "<unk>"
	print(str(st)+"\t"+str((st+1)) +"\t"+ s + "\t" + s)
	st+=1

print(str(st))
