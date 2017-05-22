#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

dir=$(dirname `realpath $0`)
cat \
    | python3 $dir/get_bibtex.py \
    | $dir/unicode2latex/unicode2latex.py -rb \
    | python3 $dir/do_abbrv.py \
    | python3 $dir/gen_keys.py
