#!/bin/bash

for filename in ./*$1*.txt; do
	awk '{print $1,$3/$5}' $filename 
	# print system size, N_mc_avgs, error_m
done
