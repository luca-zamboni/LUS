

  crf_learn template.txt NLSPARQL.train.data model.ml

  crf_test -m model.ml NLSPARQL.test.data > out.txt

  perl conlleval.pl -d "\t" < out.txt
