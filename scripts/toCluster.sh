#!/bin/bash
scp $1 simsan@octopus.theophys.kth.se:~/$(basename $PWD)/$2
