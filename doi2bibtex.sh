#!/bin/bash

dir=`dirname $0`
cat \
    | python3 $dir/get_bibtex.py \
    | $dir/unicode2latex/unicode2latex.py -rb \
    | python3 $dir/do_abbrv.py \
    | bibtool -r $dir/bibtool.conf
    | $dir/unicode2latex/unicode2latex.py -b
