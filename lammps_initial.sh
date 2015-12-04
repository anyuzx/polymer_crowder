#!/bin/bash

l0=1.13
K=100.0
n=4000
temp=2.0
duration=10000000

#G=2.4
# simulate in a periodic boundary condition to compare the result with shrink-wrapping condition
#python polymer_datafile.py -n ${n} -l ${l0} -f s -v -a -o wlc_lj_n${n}_G${G}_data
#python polymer_inputfile.py -i wlc_n400_p_data -o wlc_n400_p -t 1.2 -d 50000000 -l 1.13 -f p -v -a wlc_n400_p_input
#mkdir wlc_n400_data_p_traj

for G in 0
do
	for j in {1..50}
	do
		#python polymer_datafile.py -n ${n} -l ${l0} -f s -v -a -o wlc_lj_n${n}_G${G}_data_${j}
		python polymer_inputfile.py -i wlc_lj_n${n}_G${G}_data_${j} -o wlc_lj_n${n}_G${G}_T${temp}_${j} -n ${n} -a ${G} -t ${temp} -d ${duration} -l ${l0} -v lj -k ${K} -f s wlc_lj_n${n}_G${G}_T${temp}_input_${j}
		#mkdir wlc_lj_n${n}_G${G}_${j}_traj
	done
done
