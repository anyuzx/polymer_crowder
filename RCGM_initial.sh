#!/bin/bash

n=300
c=1

for i in {1..100}
do
	#python RCGM_datafile.py -n ${n} -l 1.0 -f s -v -c ${c} -o RCGM_n${n}_c${c}.dat 
	python RCGM_inputfile.py -i RCGM_n${n}_c${c}_${i}.dat -o RCGM_n${n}_c${c}_${i} -n ${n} -t 1.0 -d 50000000 -l 1.0 -k 1.5 -f s RCGM_n${n}_c${c}_${i}.in
done