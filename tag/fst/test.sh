#!/bin/bash

SHORT="-s"
ARGS=$@

FILE_OUT=Outtest/tagged_word.txt

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

rm -rf $FILE_OUT

DATA_TEST=Data/NLSPARQL.test.feats.txt
if isSet $SHORT; then
    DATA_TEST=Data/short_test.txt
fi

declare -A CONF_MATRIX
num_rows=49
num_columns=49

for ((i=1;i<=num_rows;i++)) do
    for ((j=1;j<=num_columns;j++)) do
        CONF_MATRIX[$i,$j]=0
    done
done

touch $FILE_OUT

while read token tag token2         
do      

    sent="$sent $token"
    tags="$tags $tag"
    if [ -z "$token" ]; then
        tempo="$(echo $sent | tr ' ' '#')"
        if ! [[ -z $tempo ]]; then

        	tagger "$sent" > learn_utils/temp.txt

            cat learn_utils/temp.txt >> $FILE_OUT

        	IFS=' ' read -a array <<< "$tags"

        	i=0

        	while read s1 s2 w mytag prob
        	do
        		if ! [ -z "$mytag" ]; then

        			real="$(python python_utils/getNumTag.py $mytag)"
        			hyp="$(python python_utils/getNumTag.py ${array[i]})"
        			CONF_MATRIX[$real,$hyp]="$((CONF_MATRIX[$real,$hyp]+1))"
    	    		if [ "${array[i]}" = "$mytag" ]; then
    	    			GOOD=$((GOOD+1))
    	    		else
    	    			WRONG=$((WRONG+1))
    	    		fi
    	    	fi
    	    	i=$((i+=1))
        	done < learn_utils/temp.txt
            
        	rm -f learn_utils/temp.txt

        	sent=""
        	tags=""
        fi

    fi

done < $DATA_TEST

#recall
for ((j=1;j<=num_columns;j++)) do
    for ((i=1;i<=num_rows;i++)) do
        printf "%d " ${CONF_MATRIX[$i,$j]}
    done
    echo 
done > learn_utils/con_matrix.txt


echo "Good : $GOOD"
echo "Wrong : $WRONG"
TOT="$((GOOD+WRONG))"
RESULT=$(awk "BEGIN {printf \"%.2f\",${GOOD}/${TOT}}")
echo "Accuracy : $RESULT"
python python_utils/stat.py