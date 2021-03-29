
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from matplotlib.colors import LogNorm


import fit_functions
import plot_functions
import geometry
import analysis_functions
import utilities

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_file', '-f', type=str, required = True, help='Input file')
#options_parser.add_argument('-input_file_half_height', '-ff', type=str, required = False, help='Input file')

if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']

    #Legge il file dati.
    t, ch0,  ch1  = numpy.loadtxt(input_file, unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    T13, T23 = utilities.TAC_scale(ch0, ch1) 

    mask = (T23 > 1.) * (T13 > 1.)
    T13 = T13[mask]
    T23 = T23[mask]

    bins = 45 
    range_T23 = (0., 60.)
    range_T13 = (0., 60.)

    plot_functions.histogram(T23, "$T_{23} [ns]$", "entries/bin", bins , range = range_T23, f = False, legend = '')
    plot_functions.histogram(T13, "$T_{13} [ns]$", "entries/bin", bins = bins, range = range_T13 , f = False, legend = '')
    plot_functions.hist2d(T23, T13, "$T_{23} [ns]$", "$T_{13} [ns]$", bins=None, range_x = range_T23, range_y = range_T13, norm =LogNorm() )

    r, p = pearsonr(T23, T13)
    print("r, p T23 and T13:", r, p)

    input_file_T13_T23_vs_x = 'vs_x/T13_T23_vs_x.txt'
    input_file_Tsum_Tdiff_vs_x = 'vs_x/Tsum_Tdiff_vs_x.txt'
    m, q, dm, dq, c, dc  = numpy.loadtxt(input_file_T13_T23_vs_x, unpack = True)
    a, b, da, db = numpy.loadtxt(input_file_Tsum_Tdiff_vs_x, unpack = True)  
   
    weights = 1/dm**2
    m = sum(a * weights) / sum(weights)
    dm = numpy.sqrt(dm[0]**2 + dm[1]**2 )

    costant = 17.2 #da definire in funzione di x 
    TOF = analysis_functions.TOF(T13, T23, costant) 

    tau_diff = q[1] - q[0] #tau23 - tau13
    T12 = analysis_functions.T12(T13, T23, tau_diff)
    x = analysis_functions.x(T12, m ) 

    h13 = geometry.h_13_long * 100 #cm

    l = numpy.sqrt(( x - geometry.s3 * 100 )**2 + h13**2 )
    beta = analysis_functions.beta(l, h13, TOF ) 
    
    plot_functions.hist2d(TOF, l,  "TOF [ns]", "l[cm]", bins=20, range_x = (-10., 20.), range_y = (170., 270.), norm = LogNorm() )
    analysis_functions.l_vs_TOF(l, TOF, 170., 220., 6)


    plt.ion() 
    plt.show()


