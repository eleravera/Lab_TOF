
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

import fit_functions
import plot_functions
import geometry
import analysis_functions


#Opzioni da terminale: input file e fondo scala della tac
description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, required = True, help='Input file')
options_parser.add_argument('-full_scale', '-s', default = 200, type=int, help='TAC s full scale')

options = vars(options_parser.parse_args())  
input_file = options['input_file']
scale = options['full_scale']

#Legge il file dati.
t, ch0,  ch1  = numpy.loadtxt(input_file, unpack = True)
utilities.rate_and_saturation(t, ch0, ch1)
T13, T23 = utilities.TAC_scale(ch0, ch1, s = 200) 

bins = 45 #int(numpy.sqrt(len(T23))) 
range_T23 = (0., 60.)
range_T13 = (0., 60.)

plot_functions.histogram(T23, "T_23 [ns]", "dN/dT_23", bins , range = range_T23, f = False)
plot_functions.histogram(T13, "T_13 [ns]", "dN/dT_13", bins = bins, range = range_T13 , f = False)
plot_functions.hist2d(T23, T13, "T23 [ns]", "T13 [ns]", bins=None, range_x = (10., 40.), range_y = (10., 40.) )

r, p = pearsonr(T23, T13)
print("r, p T23 and T13:", r, p)

costant = 17.
TOF = analysis_functions.TOF(T13, T23, costant) 

m = 0.06421 #ns/cm
plt.figure()
plt.hist(T13-T23, bins = 100)

x = analysis_functions.x(T13, T23, m ) 

h13 = geometry.h_13 * 100 #cm

l = numpy.sqrt((x-(100 * geometry.X1)*0.5)**2 + h13**2)
beta = analysis_functions.beta(l, h13, TOF ) 

"""plot_functions.hist2d(TOF, l,  "TOF [ns]", "l[cm]", bins=20, range_x = (10., 40.), range_y = (120, 250.))
analysis_functions.l_vs_TOF(l, TOF)
"""

plt.ion() 
plt.show()


