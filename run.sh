#!/bin/bash

#/usr/local/openmpi/bin/mpirun -np 6 ./lmp < wlc_n400_p_input.txt

for n in 200 300 400 500 600 700 800
do
    /usr/local/openmpi/bin/mpirun -np 6 ./lmp < wlc_lj_n${n}_input.txt
done
