#!/bin/bash

dir=`dirname $0`
cat | python3 $dir/get_bibtex.py | bibtool -r $dir/bibtool.conf
