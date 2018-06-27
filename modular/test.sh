#!/bin/bash
mpirun main.exe 16 > old_o
mpirun new.exe 16 > new_o
diff old_o new_o > difference
