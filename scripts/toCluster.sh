#!/bin/bash
scp $1 simsan@octopus.theophys.kth.se:~/exjobb/$(basename $PWD)/$2
