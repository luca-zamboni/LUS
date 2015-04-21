#!/bin/bash

rm -rf Output/*
#rm -rf *.fst

FLAGS_ISYMB=--isymbols=learn_utils/lex2.lex 
FLAG_OSYMB=--osymbols=learn_utils/lex2.lex
FLAG_SYM=--symbols=learn_utils/lex2.lex

UNK_SYMB='<unk>'


INPUT_WORD=learn_utils/input-word
FST_PROB=learned/fst-prob
LMTAG=learned/lmtag
FINAL_TAGGER=Output/tagger

ARGS=$@
DRAW="-d"

compilefst (){
	fstcompile $FLAGS_ISYMB $FLAG_OSYMB $1.txt > $1.fst
}

drawfst() {
	fstdraw $FLAGS_ISYMB $FLAG_OSYMB $1.fst | dot -Tpng > $1.png 
	convert $1.png -rotate 90 $1.png
}

compilefst-image (){
	compilefst $1
	drawfst $1
}

train-lm-tag (){
	farcompilestrings $FLAG_SYM --unknown_symbol=$UNK_SYMB $1.txt > $1.far
	ngramcount --order=2 --require_symbols=false $1.far > $1.cnt
	ngrammake --method=witten_bell $1.cnt > $1.lm
}

isSet() {
	for i in $ARGS ; do
		[[ $i == "$1" ]] && return 0 && break ; 
	done
	return 1
}

#GENERATE TXT FOR FST
python python_utils/fst-prob.py > $FST_PROB.txt
python python_utils/genfsa.py $1 > $INPUT_WORD.txt

#SIMPLE TAGGER
#compilefst $FST_PROB

#INPUT WORD FST
compilefst $INPUT_WORD
rm -rf $INPUT_WORD.txt

#BIGRAM TAG
#train-lm-tag $LMTAG


#COMPOSE EVERY FST TO CREATE THE FINAL TAGGER
fstcompose $INPUT_WORD.fst $FST_PROB.fst |\
fstcompose - $LMTAG.lm |\
fstrmepsilon |\
fstshortestpath > $FINAL_TAGGER.fst

if isSet $DRAW; then
	drawfst $FINAL_TAGGER
fi

fstprint $FLAGS_ISYMB $FLAG_OSYMB $FINAL_TAGGER.fst | sort -g -r


