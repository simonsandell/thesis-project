#!/bin/bash

for filename in ./*$1*.txt; do
	head -n 67 $filename | tail -n 1 | awk -F "    " '{print $1,$2,$30,$39,$41 / $30}';
	# print system size, N_mc_avgs, error_m
done
