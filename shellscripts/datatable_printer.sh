#!/bin/bash

for filename in ./*$1*.txt; do
	head -n 67 $filename | tail -n 1 | awk -F "    " '{print $1,$2,$40,$30}';
	# print system size, N_mc_avgs, error_m
        # indices start at 1... 
        # m has index 10
        # deltas start at index 31
        # L has idx 1, Delta L has index 31


done
