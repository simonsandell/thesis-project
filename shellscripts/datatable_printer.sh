#!/bin/bash

for filename in ./*$1*.txt; do
	echo "$(basename $filename)"
	head -n 2 $filename | tail -n 1 | awk -F "    " '{print $1,$30}';
done
