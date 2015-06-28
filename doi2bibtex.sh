#!/bin/bash

dir=`dirname $0`
cat \
    | python3 $dir/get_bibtex.py \
    | python3 $dir/do_abbrv.py \
    | bibtool -r $dir/bibtool.conf
