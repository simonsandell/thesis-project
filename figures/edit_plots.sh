#!/bin/bash

for filename in ./*.agr; do
    ex -s $filename < edits.vim
done
