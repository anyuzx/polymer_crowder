#!/bin/bash

l0=1.13
K=100.0
G=5.2

# simulate in a periodic boundary condition to compare the result with shrink-wrapping condition
#python polymer_datafile.py -n 400 -l 1.13 -f p -o wlc_n400_p_data -v -a
#python polymer_inputfile.py -i wlc_n400_p_data -o wlc_n400_p -t 1.2 -d 50000000 -l 1.13 -f p -v -a wlc_n400_p_input
#mkdir wlc_n400_data_p_traj

for n in 100 125 159 200 252 317 400 501 600 631 700 795 900 1000
do
	python polymer_datafile.py -n ${n} -l ${l0} -f s -v -a -o wlc_n${n}_data
	for j in {1..10}
	do
		python polymer_inputfile.py -i wlc_n${n}_data -o wlc_n${n}_${j} -n ${n} -t 1.2 -d 50000000 -l ${l0} -v wca -a ${G} -k ${K} -f s wlc_n${n}_input_${j}
		#mkdir wlc_lj_n${n}_G${G}_${j}_traj
	done
done
