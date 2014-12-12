#!/bin/bash

G=0

# simulate in a periodic boundary condition to compare the result with shrink-wrapping condition
#python polymer_datafile.py -n 400 -l 1.13 -f p -o wlc_n400_p_data -v -a
#python polymer_inputfile.py -i wlc_n400_p_data -o wlc_n400_p -t 1.2 -d 50000000 -l 1.13 -f p -v -a wlc_n400_p_input
#mkdir wlc_n400_data_p_traj

for n in 4000
do
	for j in 1
	do
		python polymer_restart.py -i restart.restart.wlc_lj_n${n}_G${G}_${j}.15000000 -o restart.wlc_lj_n${n}_G${G}_${j} -n ${n} -t 1.2 -d 10000000 -v lj -f s restart.wlc_lj_n${n}_G${G}_input_${j}
	done
done
