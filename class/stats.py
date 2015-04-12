

LABEL = "NLSPARQL.test.utt.labels.txt"

pred = open("outcome.txt", "r")
testlbl = open(LABEL, "r")

good=0.0
wrong=0.0

while True:
    sent = pred.readline()
    labels = testlbl.readline()

    #print(sent)

    if not labels or not sent: break

    #print(labels.split())
    for lll in labels.split():
	    if lll in sent:
	    	good+=1
	    	break;
	    else:
	    	wrong+=1


print("Good : " + str(good))
print("Wrong : " + str(wrong))
print("Accuracy : " + str(good/(good+wrong)))

