#!/bin/bash
import sys
import os
import subprocess

args = sys.argv;
rootdir = args[1]
pattern =args[2]
ans = input("Delete files matching "+ pattern +"  in "+rootdir + " ?");

if (ans == 'Y'):
    for subdirs, dirs, files in os.walk(rootdir):
        for subfile in files:
            if (pattern in subfile):
                print("deleting " + subfile)
                subprocess.call(['rm',os.path.join(subdirs,subfile)])
