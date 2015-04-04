TRAIN = "NLSPARQL.train.tok"
TEST = "NLSPARQL.test.tok"
LABEL = "NLSPARQL.train.utt.labels.txt"
STOP_WORD = "english.stop.txt"

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
			#probs[lbl][word] *= countForLabel(wordForLabels[lbl])/countForLabel(countTotal)
	return probs

def predict(probs,phrase):
	
	maxProb=0.0
	maxTag = ""

	for lbl in probs:

		tempProb = 1.0

		for w in phrase.split():
			if not w in probs[lbl]:
				w='<unk>'

			tempProb *= probs[lbl][w]

		if tempProb > maxProb:
			maxProb = tempProb
			maxTag = lbl

	return maxTag,maxProb

def main():

	train = open(TRAIN, "r")
	label = open(LABEL, "r")

	text=""

	wordForLabels = {}
	allLables = []

	while True:
	    sent = train.readline()
	    labels = label.readline()

	    if not labels or not sent: break

	    #words = sent.split()
	    words = removeStopInList(sent.split())
	    lbls = labels.split()

	    lcw = countWordList(words)

	    for lbl in lbls:
			if lbl in wordForLabels:
				for w in countWordList(words):
					if w in wordForLabels[lbl]:
						wordForLabels[lbl][w] += lcw[w]
					else:
						wordForLabels[lbl][w] = lcw[w]
			else:
				wordForLabels[lbl] = lcw

	    text+=sent
	    allLables += lbls

	allLables = list(set(allLables))

	text = removeStop(text)

	countTotal = countWordString(text)

	for w in countTotal:
		countTotal[w] += 1.0

	for lbl in allLables:
		for x in wordForLabels[lbl]:
			wordForLabels[lbl][x] += 1.0
		wordForLabels[lbl]['<unk>'] = 1.0

	countTotal['<unk>'] = len(allLables)

	probs = calcProb(wordForLabels,countTotal)
	
	with open(TEST,'r') as f:
		for line in f:
			line = removeStop(line)
			print(predict(probs,line)[0])

	
	#print(maxTag + " " + str(maxProb))
				

main()