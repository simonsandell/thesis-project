#!/bin/bash

for filename in ./*.agr; do
    vim -c "%s/char size 1\.0/char size 1\.5/g" -c "%s/prec \d/prec 9/g" -c "%s/prec \d, \d/prec 9, 9" -c "wq" $filename
done
