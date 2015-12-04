#!/bin/bash

for c in {1..100}
do
	python plot_rg_c.py log.RCGM_c${c}.txt Rg_c.dat
done