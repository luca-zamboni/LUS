#!/bin/bash

SHORT="-s"
ARGS=$@

FILE_OUT=Outtest/tagged_word.txt
FILE_OUT2=Outtest/tagged_word2.txt

sent=""
tags=""

GOOD=0
WRONG=0

tagger () {
	./tagger.sh "$1"
}

calc(){ 
	awk "BEGIN { print "$*" }"
}

isSet() {
    for i in $ARGS ; do
        [[ $i == "$1" ]] && return 0 && break ; 
    done
    return 1
}


DATA_TEST=Data/NLSPARQL.test.feats.txt
if isSet $SHORT; then
    DATA_TEST=Data/short_test.txt
fi

rm -rf $FILE_OUT
rm -rf $FILE_OUT2
touch $FILE_OUT
touch $FILE_OUT2

while read token tag token2         
do      

    sent="$sent $token"
    tags="$tags $tag"
    if [ -z "$token" ]; then
        tempo="$(echo $sent | tr ' ' '#')"
        if ! [[ -z $tempo ]]; then

        	tagger "$sent" > learn_utils/temp.txt

        	IFS=' ' read -a array <<< "$tags"

        	i=0

        	while read s1 s2 w mytag prob
        	do
                if ! [ -z "$mytag" ]; then
                    echo -e "$w T-${array[i]} T-$mytag" >> $FILE_OUT2
                    i=$((i+=1))
                fi
        	done < learn_utils/temp.txt
            
            echo "" >> $FILE_OUT2
        	rm -f learn_utils/temp.txt

        	sent=""
        	tags=""
        fi

    fi

done < $DATA_TEST

perl conlleval.pl -d " " < Outtest/tagged_word2.txt