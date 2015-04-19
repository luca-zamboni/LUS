
def getLemma(w):
	with open('Data/NLSPARQL.train.feats.txt','r') as f:
		for line in f:
			a = line.split()
			if len(a)>0:
				if a[0] == w:
					return a[2]

		return w

with open('Data/NLSPARQL.train.tok','r') as f:

	label = open("Data/lemmedTrain.txt", "w")

	for line in f:
		a = line.split()
		for w in a:
			label.write(getLemma(w) + " ")
		label.write("\n")