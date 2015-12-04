################################################################
# Generate a polymer chain simulation input file for LAMMPS
################################################################
import getopt, sys
import numpy as np

################################################################
# define several default values
temp = 1.2
duration = 50000000
ve = False
sf = False
random_seed = np.random.randint(1,10000000,size=2)
################################################################

try:
	input_filename = sys.argv[1:][-1]
except:
	print "Error: please input LAMMPS input file name you want"
	sys.exit()

try:
	optlist, args = getopt.getopt(sys.argv[1:-1],'n:i:o:t:d:l:f:v:a:k:h')
except getopt.GetoptError as err:
	print str(err)
	print "Command syntax: -i <data file> -o <output file> -t <temperature> -d <duration of simulation> -l <bond length> -f <boundary condition>"
	sys.exit()

for opt, arg in optlist:
	if opt == '-i':
		try:
			data_name = arg
		except:
			print "Error: Please input LAMMPS data file"
			sys.exit()
	elif opt == '-n':
		try:
			n = int(arg)
		except:
			print "Error: Please input the number of monomers"
			sys.exit()
	elif opt == '-o':
		try:
			output_name = arg
		except:
			print "Error: Please input LAMMPS log file name you want"
			sys.exit()
	elif opt == '-t':
		try:
			temp = float(arg)
		except:
			print "Error: Please input temperature. Default value is 1.2 in LJ unit"
			sys.exit()
	elif opt == '-d':
		try:
			duration = int(arg)
		except:
			print "Error: Please input simulation duration. Default value is 50000000"
			sys.exit()
	elif opt == '-l':
		try:
			l0 = float(arg)
		except:
			print "Error: bond length need to be a real number"
			sys.exit()
	elif opt == '-k':
		try:
			k = float(arg)
		except:
			print "Error: bond potential spring constant need to be a real number"
			sys.exit()
	elif opt == "-f":
		try:
			pc = arg
			if pc not in ['s','p']:
				print "Error: -f <boundary condition> s: shrink-wrapping p: periodic boundary"
				sys.exit()
		except:
			print "Error: please specify boundary condition"
			print "-f <boundary condition> s: shrink-wrapping p: periodic boundary"
			sys.exit()
	elif opt == '-v':
		try:
			ve = arg
			if ve not in ['wca','lj']:
				print "Error: -ve <type of pairwise interaction> wca: WCA potential lj: Lenard-Jones potential"
				sys.exit()
		except:
			print "Error: please specify the type of VDW pairwise interaction"
			print "-ve <type of pairwise interaction> wca: WCA potential lj: Lenard-Jones potential"
			sys.exit()
	elif opt == '-a':
		try:
			sf = float(arg)
		except:
			print "Error: angle potential spring constant need to be a real number"
			sys.exit()
	elif opt == '-h':
		print "usage: python polymer_inputfile.py [options] [arg] ... <LAMMPS input file>"
		print "Options and arguments:"
		print "Arguments:"
		print "-i <arg> : LAMMPS data file"
		print "-o <arg> : LAMMPS log file"
		print "-t <arg> : simulation temperature"
		print "-d <arg> : simulation duration(how many timesteps)"
		print "-l <arg> : bond length"
		print "-f <arg> : boundary condition\n           s:shrink-wrapping boundary condition\n           p:periodic boundary condition"
		print "Options:"
		print "-v       : WCA potential is set on(default is no WCA potential)"
		print "-a       : bond angle potential set on and to be harmonic(default is no angle potential)"
		print "<***>    : LAMMPS input file. This script will generate this file"
		sys.exit()

try:
	l0
except NameError:
	print "Error: please specify the bond length"
	sys.exit()

try:
	k
except NameError:
	print "Error: please specify the bond spring constant"
	sys.exit()

try:
	n
except NameError:
	print "Error: please specify the number of monomers"
	sys.exit()

try:
	data_name
except NameError:
	print "Error: please give a LAMMPS data file"
	sys.exit()

try:
	output_name
except NameError:
	print "Error: please give a LAMMPS log file name you want"
	sys.exit()

try:
	pc
except NameError:
	print "Error: please specify the boundary conditon"
	print "-f <boundary condition> s: shrink-wrapping p:periodic boundary"
	sys.exit()


with open(input_filename,"w") as f:
	f.write("##############################################\n")
	f.write("#                                            #\n")
	f.write(("# Filename:"+input_filename+".txt").ljust(45)+"#\n")
	f.write("# Author: Guang Shi, 2014                    #\n")
	f.write("#                                            #\n")
	f.write("# Excute the script using:                   #\n")
	f.write(("# lmp < "+input_filename+".txt").ljust(45)+"#\n")
	f.write("#                                            #\n")
	f.write("##############################################\n")
    
    # define VARIABLES
	f.write("# VARIABLES\n")
	f.write("variable".ljust(15) + "input index "+data_name+"\n")
	f.write("variable".ljust(15) + "output index "+output_name+"\n")
	f.write("variable".ljust(15) + "id_end equal "+str(n)+"\n")
	f.write("variable".ljust(15) + "Rd equal " +"(x[1]-x[${id_end}])^2+(y[1]-y[${id_end}])^2+(z[1]-z[${id_end}])^2\n")
	f.write("\n")

	# define Initialization 
	f.write("# Initialization\n")
	f.write("units".ljust(15)+"lj\n")
	if pc == 's' and n >= 80:
		f.write("boundary".ljust(15)+"s s s\n")
	elif pc == 's' and n < 80:
		f.write("boundary".ljust(15)+"m m m\n")
	elif pc == 'p':
		f.write("boundary".ljust(15)+"p p p\n")
	if sf:
		f.write("atom_style".ljust(15)+"angle\n")
	else:
		f.write("atom_style".ljust(15)+"bond\n")
	f.write("log".ljust(15)+"log.${output}.txt\n")
	f.write("read_data".ljust(15)+"${input}\n")
	f.write("\n")

	# define potential information
	f.write("# Potential information\n")
	if ve == 'wca' or ve == False:
		f.write("neighbor".ljust(15)+str(2.0)+"  bin\n")
	elif ve == 'lj':
		f.write("neighbor".ljust(15)+"2.0 bin\n")
	if ve == False:
		f.write("atom_modify".ljust(15)+"sort 0 0.0\n")                    # if no pairwise interaction, atom sort need to be off
		f.write("comm_modify".ljust(15)+"cutoff "+str(100)+"\n")       # if no pairwise interaction, a ghost cutoff need to be set larger than the bond length
	f.write("bond_style".ljust(15)+"harmonic\n")
	f.write("bond_coeff".ljust(15)+"1 " + str(k) + " " + str(1.13) + "\n")
	f.write("bond_coeff".ljust(15)+"2 " + str(k) + " " + str(1.13) + "\n")
	if sf != False:
		f.write("angle_style".ljust(15)+"harmonic\n")
		f.write("angle_coeff".ljust(15)+"1 " + str(sf) +" 180.0\n")
	if ve == 'wca':
		f.write("pair_style".ljust(15)+"lj/cut 1.12246\n")
		f.write("pair_modify".ljust(15)+"shift yes mix arithmetic\n")
		f.write("pair_coeff".ljust(15)+"1  1  1.0  1.0  1.12246\n")
	elif ve == 'lj':
		f.write("pair_style".ljust(15)+"lj/cut 3.0\n")
		f.write("pair_modify".ljust(15)+"mix arithmetic\n")
		f.write("pair_coeff".ljust(15)+"1  1  1.0  1.0  3.0\n")
	elif ve == False:
		f.write("pair_style".ljust(15)+"none\n")

    
    # define Equilibration parameters
        f.write("\n")
	f.write("# Equilibration (Langevin dynamics at reduced temperature " + str(temp)+")\n")
	f.write("\n")
        f.write("compute".ljust(15)+"Rg all gyration\n")
    	#if ve:
    	#	f.write("compute".ljust(15) + "pepair all pe/atom pair\n")
    	#	f.write("compute".ljust(15)+"pebond all pe/atom bond\n")
    	#if sf:
    	#	f.write("compute".ljust(15)+"peangle all pe/atom angle\n")
	f.write("velocity".ljust(15) + "all create " + str(temp)+ " " + str(random_seed[0])+"\n")
	f.write("fix".ljust(15) + "1 all nve\n")
	f.write("fix".ljust(15) + "2 all langevin " + str(temp) + "  " + str(temp) + "  100.0  " +str(random_seed[1])+"\n")
	if pc == 's':
		f.write("fix".ljust(15)+"3 all recenter INIT INIT INIT\n")
	f.write("thermo_style".ljust(15) + "custom step cpuremain temp c_Rg c_Rg[1] c_Rg[2] c_Rg[3] c_Rg[4] c_Rg[5] c_Rg[6] v_Rd evdwl ebond eangle\n")
	f.write("thermo".ljust(15)+str(100)+"\n")
        f.write("dump".ljust(15)+"1 all custom " + str(500) + " ${output}_traj id mass x y z vx vy vz\n")
	f.write("dump_modify".ljust(15)+"1 append yes\n")

	#f.write("timestep".ljust(15)+str(0.00001)+"\n")
	#f.write("run".ljust(15)+str(100000)+"\n")

	#f.write("timestep".ljust(15)+str(0.00005)+"\n")
	#f.write("run".ljust(15)+str(100000)+"\n")

	#f.write("timestep".ljust(15)+str(0.0001)+"\n")
	#f.write("run".ljust(15)+str(100000)+"\n")

	#f.write("timestep".ljust(15)+str(0.0005)+"\n")
	#f.write("run".ljust(15)+str(100000)+"\n")

	#f.write("timestep".ljust(15)+str(0.001)+"\n")
	#f.write("run".ljust(15)+str(100000)+"\n")

	#f.write("timestep".ljust(15)+str(0.001)+"\n")
	#f.write("run".ljust(15)+str(100000)+"\n")

	#f.write("timestep".ljust(15)+str(0.005)+"\n")
	#f.write("run".ljust(15)+str(500000)+"\n")

	#f.write("timestep".ljust(15)+str(0.008)+"\n")
	#f.write("run".ljust(15)+str(500000)+"\n")

	f.write("timestep".ljust(15)+str(0.01)+"\n")
	f.write("run".ljust(15)+str(10000000)+"\n")
	
	f.write("write_restart".ljust(15)+"restart.${output}.*\n")
	f.write("\n")

	f.write("print 'All done'\n")
