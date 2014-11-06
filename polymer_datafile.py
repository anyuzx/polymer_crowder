################################################################
# Generate a polymer chain data file for LAMMPS
################################################################

import numpy as np
from math import *
import getopt, sys
import lattice_SAW    # import the lattice_SAW module

##############################################################################
try:
    optlist, args = getopt.getopt(sys.argv[1:],'n:l:vao:f:h')
except getopt.GetoptError as err:
    print str(err)
    print "Command syntax: -n <number of monomers> -l <bond length> -o <output filename>"
    sys.exit()

ve = False
sf = False
for opt, arg in optlist:
    if opt == '-n':
        try:
            N = int(arg)
        except:
            print "Error: number of monomers need to be integer"
            sys.exit()
    elif opt == '-h':
        print "usage: python polymer_write.py [options] [arg] ..."
        print "Options and arguments:"
        print "Arguments:"
        print "-n <arg> : number of monomers. needs to be an integer"
        print "-l <arg> : length of monomer bond. needs to be a real number"
        print "-f <arg> : boundary condition\n           s:shrink-wrapping boundary condition\n           p:periodic boundary condition"
        print "-o <arg> : name of output file name"
        print "Options:"
        print "-v       : volume exclusion is set to be True(default is False)"
        print "-a       : chain persistence is set to be True(default is False)"
        print ""
        print "DISCREPTION:"
        print "If chain persistence is set to be TRUE, chain will always be generated as a straight chain, \
aligned along x-axes and centered in the center of simulation box regardless of it's volume excluded or not."
        print "If chain persistence is set to be FALSE, chain will be generated based on volume exclusion option. \
volume-excluded chain is a lattice self-avoiding random walk and non-volume-excluded chain is a lattice random walk."
        print "If boundary condition is set to be SHRINK-WRAPPING, the box will be made contain the chain roughly in the center \
with 5*(bond length) margin."
        print "If boundary condition is set to be PERIODIC, the box will be made with side length L >= (N+10)*(bond length). \
Chain will be roughly put in the center."
        sys.exit()
    elif opt == '-l':
        try:
            l0 = float(arg)
        except:
            print "Error: bond length need to be a real number"
            sys.exit()
    elif opt == '-v':
        ve = True                 # volume exclusion is set to be True
    elif opt == '-a':
        sf =  True                # semiflexible chain is set to be True
    elif opt == '-o':
        try:
            output_name = arg
        except:
            print "Error: please specify the name of output file"
            sys.exit()
    elif opt == "-f":
        try:
            pc = arg
            if pc not in ['s','p']:
                print "Error: -f <boundary condition> s: shrink-wrapping p:periodic boundary"
                sys.exit()
        except:
            print "Error: please specify boundary condition"
            print "-f <boundary condition> s: shrink-wrapping p:periodic boundary"
            sys.exit()

try:
    N
except NameError:
    print "error. please specify number of monomers"
    sys.exit()

try:
    l0
except NameError:
    print "error. please specify the bond length"
    sys.exit()

try:
    output_name
except NameError:
    print "Error: please specify the name of output file"
    sys.exit()

try:
    pc
except NameError:
    print "Error: please specify the boundary conditon"
    print "-f <boundary condition> s: shrink-wrapping p:periodic boundary"
    sys.exit()
###################################################################################
if ve:
    vee = 1
else:
    vee = 0

# create a straight chain
def straight_chain(N,l0):
    chain = np.dstack((l0*np.arange(N),np.zeros(N),np.zeros(N)))[0]
    chain = chain - np.int_(np.mean(chain,axis=0))
    return chain
###################################################################################
# Generate the random polymer chain and simulation box dimension
# two cases: excluded-volume and no excluded-volume
def make_chain_box(N,l0,pc,ve,sf):
    if sf:
        chain = straight_chain(N,l0)
    else:
        chain = lattice_SAW.lattice_SAW(N,l0,vee)
        chain = chain.reshape(N,3)

    if pc == 's':
        l = np.amax(np.fabs(chain))
        box_dimension = np.array([[-l-5*l0,l+5*l0],[-l-5*l0,l+5*l0],[-l-5*l0,l+5*l0]])
    elif pc == 'p':
        box_dimension = np.array([[-(N+10)*l0/2,(N+10)*l0/2],[-(N+10)*l0/2,(N+10)*l0/2],[-(N+10)*l0/2,(N+10)*l0/2]])
    return chain, box_dimension
###################################################################################
chain, box_dimension = make_chain_box(N,l0,pc,ve,sf)
mass = 1.0

with open(output_name,'w') as f:
    f.write("Data file for polymer chain   Volume Exclusion:" + str(ve)+"   Chain persistence:"+str(sf)+"\n\n")
    f.write(str(N)+"  atoms    # number of monomers\n")
    f.write(str(N-1)+"  bonds    # number of bonds between monomers\n")
    if sf:
        f.write(str(N-2)+"  angles    # semiflexible chain. Angle harmonic potential\n")
    f.write("\n")
     
    f.write("1  atom types    # number of atom types\n")
    f.write("1  bond types    # number of bond types\n")
    if sf:
        f.write("1  angle types    # number of angle types\n")
    f.write("\n")
    
    f.write(str("%.4f" % box_dimension[0,0]) + " " + str("%.4f" % box_dimension[0,1]) + " xlo" + " xhi\n")
    f.write(str("%.4f" % box_dimension[1,0]) + " " + str("%.4f" % box_dimension[1,1]) + " ylo" + " yhi\n")
    f.write(str("%.4f" % box_dimension[2,0]) + " " + str("%.4f" % box_dimension[2,1]) + " zlo" + " zhi\n")

    f.write("\n")
    f.write("Masses\n\n")
    f.write(str(1).ljust(10)+"%.2f" % mass + "\n")
    f.write("\n")

    f.write("Atoms\n\n")
    for i in range(len(chain)):
        f.write(str(int(i+1)).ljust(10)+str(1).ljust(10)+str(1).ljust(10)+("%.4f" % chain[i,0]).ljust(15)+("%.4f" % chain[i,1]).ljust(15)+("%.4f" % chain[i,2]).ljust(15)+"\n")
    f.write("\n")
    f.write("Bonds\n\n")
    for i in range(1,len(chain)):
        f.write(str(i).ljust(10)+str(1).ljust(10)+str(i).ljust(10)+str(i+1).ljust(10)+"\n")

    if sf:
        f.write("\n")
        f.write("Angles\n\n")
        for i in range(1,len(chain)-1):
            f.write(str(i).ljust(10)+str(1).ljust(10)+str(i).ljust(10)+str(i+1).ljust(10)+str(i+2).ljust(10)+"\n")
