#!/bin/bash

rm -rf *.png
rm -rf *.fst

FLAGS_ISYMB=--isymbols=lex.lex 
FLAG_OSYMB=--osymbols=lex.lex
FLAG_SYM=--symbols=lex.lex

UNK_SYMB='<unk>'

INPUT_WORD=input-word
FST_PROB=fst-prob
LMTAG=lmtag
FINAL_TAGGER=ftag

function compilefst {
	fstcompile $FLAGS_ISYMB $FLAG_OSYMB $1.txt > $1.fst
}

function drawfst {
	fstdraw $FLAGS_ISYMB $FLAG_OSYMB $1.fst | dot -Tpng > $1.png 
	convert $1.png -rotate 90 $1.png
}

function compilefst-image {
	compilefst $1
	drawfst $1
}

function train-lm-tag {
	farcompilestrings $FLAG_SYM --unknown_symbol=$UNK_SYMB $1.txt > $1.far
	ngramcount --order=3 --require_symbols=false $1.far > $1.cnt
	ngrammake --method=witten_bell $1.cnt > $1.lm
}

#GENERATE TXT FOR FST
python fst-prob.py > $FST_PROB.txt
python genfsa.py $1 > $INPUT_WORD.txt

#SIMPLE TAGGER
compilefst-image $FST_PROB

#INPUT WORD FST
compilefst-image $INPUT_WORD

#BIGRAM TAG
train-lm-tag $LMTAG


#COMPOSE EVERY FST TO CREATE THE FINAL TAGGER
fstcompose $INPUT_WORD.fst $FST_PROB.fst |\
fstcompose - $LMTAG.lm |\
fstrmepsilon |\
fstshortestpath > $FINAL_TAGGER.fst

drawfst $FINAL_TAGGER

fstprint $FLAGS_ISYMB $FLAG_OSYMB $FINAL_TAGGER.fst
