def getMatrix():
	with open('learn_utils/con_matrix.txt','r') as f:
		matrix=[]
		i=0
		for line in f:
			a = line.split()
			j=0
			linea=[]
			for b in a:
				linea += [float(b)]
			matrix += [linea]
		return matrix

matrix=getMatrix()
mediarecall=0.0
total=0.0
for i in range(0,len(matrix)):
	somma=0.0
	for j in range(0,len(matrix)):
		somma += matrix[i][j]
	total+=somma
	if somma == 0:
		recall = 1.0
	else:
		recall = float(matrix[i][i]/somma)
	mediarecall+=float(recall)

r=float(mediarecall/len(matrix))

print("Recall : " + str(r))

mediarecall=0.0
total=0.0
for i in range(0,len(matrix)):
	somma=0.0
	for j in range(0,len(matrix)):
		somma += matrix[j][i]
	total+=somma
	if somma == 0:
		recall = 1.0
	else:
		recall = float(matrix[i][i]/somma)
	mediarecall+=float(recall)

p=float(mediarecall/len(matrix))

f1score=(2*r*p/(r+p))

print("Precision : " + str(p))
print("F1 score : " + str(f1score))
