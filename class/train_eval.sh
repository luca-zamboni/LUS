#!/bin/bash

ARGS=$@
T="-t"
TRAIN="--train"

isSet() {
    for i in $ARGS ; do
        [[ $i == "$1" ]] && return 0 && break ; 
    done
    return 1
}

if  isSet $T  ||  isSet $TRAIN  ; then
    DATA_TEST=Data/short_test.txt
    python bayes.py -t > outcome.txt
else
	python bayes.py > outcome.txt
fi


perl conlleval.pl -d "\t" < outcome.txt
