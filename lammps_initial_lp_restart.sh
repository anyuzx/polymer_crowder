#!/bin/bash

G=5.2

# simulate in a periodic boundary condition to compare the result with shrink-wrapping condition
#python polymer_datafile.py -n 400 -l 1.13 -f p -o wlc_n400_p_data -v -a
#python polymer_inputfile.py -i wlc_n400_p_data -o wlc_n400_p -t 1.2 -d 50000000 -l 1.13 -f p -v -a wlc_n400_p_input
#mkdir wlc_n400_data_p_traj

for n in 100 125 159 200 252 317 400 501 600 631 700 795 900 1000
do
	for j in {1..10}
	do
		python polymer_restart.py -i restart.wlc_n${n}_${j}.50000000 -o restart.wlc_n${n}_${j} -n ${n} -t 1.2 -d 50000000 -v wca -f s restart.wlc_n${n}_input_${j}
	done
done
