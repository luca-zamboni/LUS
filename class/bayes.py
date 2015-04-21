
import os
import sys

MODEL_PROBS = "model/prob.model"
MODEL_WORD_LABEL = "model/word.model"
MODEL_TOTAL= "model/total.model"

UNK = '<unk>'
LEMMA_TRAIN = "Data/lemmedTrain.txt"
LEMMA_TEST = "Data/lemmedTest.txt"
TRAIN = "Data/NLSPARQL.train.tok"
TEST = "Data/NLSPARQL.test.tok"
LABEL = "Data/NLSPARQL.train.utt.labels.txt"
LABEL_TEST = "Data/NLSPARQL.test.utt.labels.txt"
TAG_TRAIN = "Tag-train.txt"
TAG_TEST =  "Tag-test.txt"
STOP_WORD = "english.stop.txt"
TRAIN_FLAG = "--train"
T_FLAG="-t"

def getStopWord():
	with open(STOP_WORD,'r') as f:
		stop = []
		for line in f:
			a = line.split()
			stop += a
		return stop

def removeStop(string):
	ret = ""
	stop = getStopWord()
	for w in string.split():
		if not w in stop:
			ret +=  " " + w
	return ret

def removeStopTags(string,tags):
	ret = ""
	ret2 = ""
	stop = getStopWord()
	lista=string.split()
	listatags=tags.split()
	for i in range(0,len(lista)):
		if not lista[i] in stop:
			ret +=  " " + lista[i]
			ret2 += " " + listatags[i]
	return ret,ret2

def removeStopInList(list):
	ret = []
	stop = getStopWord()
	for w in list:
		if not w in stop:
			ret +=  [w]
	return ret

def countWordString(text):
	ret = {}
	for word in text.split():
		if word in ret:
			ret[word] += 1.0
		else:
			ret[word] = 1.0
	return ret

def countWordList(listW):
	ret = {}
	for word in listW:
		if word in ret:
			ret[word] += 1.0
		else:
			ret[word] = 1.0
	return ret

def countForLabel(json):
	ret = 0
	for w in json:
		ret += json[w]
	return ret

def calcProb(wordForLabels,countTotal):
	probs = {}
	for lbl in wordForLabels:
		probs[lbl] = {}
		for word in wordForLabels[lbl]:
			probs[lbl][word] = wordForLabels[lbl][word]/countTotal[word]
	return probs

def predict(probs,phrase,total,wordForLabels):
	
	maxProb=0.0
	maxTag = ""

	for lbl in probs:

		tempProb = 1.0

		for w in phrase:
			if not w in probs[lbl]:
				w=UNK
			
			tempProb *= probs[lbl][w]

		tempProb *= countForLabel(wordForLabels[lbl])/len(total)

		if tempProb > maxProb:
			maxProb = tempProb
			maxTag = lbl

	return maxTag,maxProb

#Smoothing function
def smoothPlusOne(allLables,wordForLabels,countTotal,testo):
	incrementalFactor=1.0
	totalPlus=0
	for lbl in allLables:
		for x in wordForLabels[lbl]:
			wordForLabels[lbl][x] += incrementalFactor
			countTotal[x] += incrementalFactor
		wordForLabels[lbl][UNK] = incrementalFactor

	countTotal[UNK] = float(len(testo))

	return wordForLabels,countTotal

def nGramList(words):
	ret=[]
  	word = zip(words, words[1:])
  	for w,x in word:
  		ret = ret + [w + "_" +x]
  	word = zip(words[1:], words)
  	for w,x in word:
  		ret = ret + [w + "_" +x]


  	#word = zip(words,words[1:],words[2:])
  	#for w,x,z in word:
  	#	ret = ret + [w + "_" +x+ "_"+z]
  	
  	return ret

def mergeList(l1,l2):
	ret = []
	for i in range(0,len(l1)):
		ret += [l1[i] + "_" +l2[i]]

	return ret

#Given text and tags retrun unigram of combined features
def featurExtract(text,tags):
	#text,tags = removeStopTags(text,tags)
	ret = []
	ret += text.split()
	nG = text.split()
	#Ngramm of text
	ret += nGramList(nG)
	ret += nGramList(nG)

	#Bigram of tags

	#tagBi=[]
	#tagBigram = zip(tags.split(), tags.split()[1:])
  	#for w,x in tagBigram:
  	#	tagBi = tagBi + [w + "_" +x]
  	#ret += tagBi

  	#Unigram Text with relative Tag

  	#ret += mergeList(text.split()[1:],tagBi)

	#ret += mergeList(text.split(),tags.split())

  	#print(ret)

	return ret

def train():
	train = open(TRAIN, "r")
	label = open(LABEL, "r")
	tag = open(TAG_TRAIN, "r")

	text=""
	textTags=""

	wordForLabels = {}
	allLables = []
	total = []

	while True:
		#Iterating over 3 files
		sent = train.readline()
		labels = label.readline()
		tags = tag.readline()

		if not labels or not sent: break

		lbls = labels.split()
		allLables += lbls

		total += featurExtract(sent,tags)

		words = featurExtract(sent,tags)

		#Counting word for labels
		for lbl in lbls:
			lcw = countWordList(words)
			if lbl in wordForLabels:

				for w in lcw:

					if w in wordForLabels[lbl]:
						wordForLabels[lbl][w] += lcw[w]

					else:

						wordForLabels[lbl][w] = lcw[w]

			else:
			    wordForLabels[lbl] = lcw


	allLables = list(set(allLables))

	countTotal = countWordList(total)

	wordForLabels,countTotal = smoothPlusOne(allLables, wordForLabels,countTotal,total)

	#Precalculating Probabilities
	probs = calcProb(wordForLabels,countTotal)

	return probs,total,wordForLabels

def saveModel(probs,total,wordForLabels):

	probF = open(MODEL_PROBS, "w")
	totalF = open(MODEL_TOTAL, "w")
	wordForLabelsF = open(MODEL_WORD_LABEL, "w")

	for lbl in probs:
		for w in probs[lbl]:
			probF.write(lbl  +" " +w + " " + str(probs[lbl][w]) + "\n")
			wordForLabelsF.write(lbl +" " +w +  " " + str(wordForLabels[lbl][w]) + "\n")

	for w in total:
		totalF.write(w + "\n")

def loadModel():
	probF = open(MODEL_PROBS, "r")
	totalF = open(MODEL_TOTAL, "r")
	wordForLabelsF = open(MODEL_WORD_LABEL, "r")

	probs = {}
	wordForLabels = {}
	total=[]
		
	while True:
		probString = probF.readline()
		wordForLabelString = wordForLabelsF.readline()
		if not probString or not wordForLabelString: break
		p=probString.split()
		w=wordForLabelString.split()
		if not p[0] in probs:
			probs[p[0]]={}
			wordForLabels[p[0]]={}
		probs[p[0]][p[1]]=float(p[2])
		wordForLabels[w[0]][w[1]]=float(w[2])

	while True:
		totalString = totalF.readline()
		if not totalString: break
		total += totalString.split()[0]

	return probs,total,wordForLabels


def main(argv):

	if TRAIN_FLAG in argv or T_FLAG in argv:
		probs,total,wordForLabels = train()
		saveModel(probs,total,wordForLabels)
	else:
		if os.path.isfile(MODEL_PROBS) and os.path.isfile(MODEL_TOTAL) and os.path.isfile(MODEL_WORD_LABEL) :
			probs,total,wordForLabels = loadModel()
		else:
			probs,total,wordForLabels = train()
			saveModel(probs,total,wordForLabels)

	# TEST

	test = open(TEST, "r")
	tag = open(TAG_TEST, "r")
	label = open(LABEL_TEST, "r")

	while True:
		sent = test.readline()
		tags = tag.readline()
		labels = label.readline()

		if not tags or not sent: break

		l = featurExtract(sent,tags)

		print("a " + "\tL-" + labels.split()[0] + "\tL-" + predict(probs,l,total,wordForLabels)[0] + "\n")
				

if __name__ == "__main__":
	 main(sys.argv)