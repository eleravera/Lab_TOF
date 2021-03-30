
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
options_parser.add_argument('-input_file_h', '-ff', type=str, required = False, help='Input file')
options_parser.add_argument('-simulation', '-s', type=bool, default = False, help='Input file')
options_parser.add_argument('-salve_fig', '-fig', type=bool, default = False, help='save figure')


if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    input_file_h = options['input_file_h']
    simulation = options['simulation']
    salve_fig = options['salve_fig']
     
    
    if simulation is False: 
      t, ch0,  ch1  = numpy.loadtxt(input_file, unpack = True)
      utilities.rate_and_saturation(t, ch0, ch1)
      T13, T23 = utilities.TAC_scale(ch0, ch1) 
      mask = (T23 > 1.) * (T13 > 1.) * (T23 < 65.) * (T13 < 65.)
      T13 = T13[mask]
      T23 = T23[mask]
      figlabel = '_run47' 

      t, ch0,  ch1  = numpy.loadtxt(input_file_h, unpack = True)
      utilities.rate_and_saturation(t, ch0, ch1)
      T13_h2, T23_h2 = utilities.TAC_scale(ch0, ch1) 
      mask = (T23_h2 > 1.) * (T13_h2 > 1.) * (T23_h2 < 65.) * (T13_h2 < 65.)
      T13_h2 = T13_h2[mask]
      T23_h2 = T23_h2[mask]
      figlabel = '_run30' 

    
    if simulation is True: 
      T23, res23, T13 , res13, T12, TOF  = numpy.loadtxt(input_file, unpack = True)
      figlabel = '_MC' 
    
    bins = 45 
    range_T23 = (0., 60.)
    range_T13 = (0., 60.)

    plot_functions.histogram(T23, "$T_{23} [ns]$", "entries/bin", bins , f = False, legend = '')
    plot_functions.histogram(T13, "$T_{13} [ns]$", "entries/bin", bins = bins , f = False, legend = '')
    plot_functions.hist2d(T23, T13, "$T_{23} [ns]$", "$T_{13} [ns]$", bins=None, range_x = range_T23, range_y = range_T13, save_fig = salve_fig, figlabel = figlabel )

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
    tau_diff = q[1] - q[0] #tau23 - tau13    
    
    
    TOF = analysis_functions.TOF(T13, T23, costant, save_fig = salve_fig, figlabel = figlabel) 
    T12 = analysis_functions.T12(T13, T23, tau_diff)
    x = analysis_functions.x(T12, m , save_fig = salve_fig, figlabel = figlabel)   
    l = analysis_functions.l(x, geometry.h_13_long * 100, geometry.s3 * 100)       
    beta = analysis_functions.beta(l, geometry.h_13_long * 100, TOF, save_fig = salve_fig, figlabel = figlabel )     
    plot_functions.hist2d(TOF, l,  "TOF [ns]", "l[cm]", bins=50, range_x = (-10., 20.), range_y = (170., 270.), norm = LogNorm())


    TOF_h2 = analysis_functions.TOF(T13_h2, T23_h2, costant, save_fig = salve_fig, figlabel = figlabel) 
    T12_h2 = analysis_functions.T12(T13_h2, T13_h2, tau_diff)
    x_h2 = analysis_functions.x(T12_h2, m , save_fig = salve_fig, figlabel = figlabel)   
    l_h2 = analysis_functions.l(x_h2, geometry.h_13_short * 100, geometry.s3 * 100)       
    beta = analysis_functions.beta(l_h2, geometry.h_13_short * 100, TOF_h2, save_fig = salve_fig, figlabel = figlabel )     
    plot_functions.hist2d(TOF_h2, l_h2,  "TOF [ns]", "l[cm]", bins=50, norm = LogNorm())

    
    analysis_functions.l_vs_TOF(l, TOF, 170., 220., 6)
    #analysis_functions.l_vs_TOF(l_h2, TOF_h2, 80., 110.,  6)


    plot_functions.hist2d((T23+T13)*0.5-17.2, T13-T23, "$T_{sum} [ns]$", "$T_{diff} [ns]$", range_x = (0., 11.), range_y = (-20., 20.), bins=None, norm = LogNorm())

    a = numpy.array([5.9, 3.7, 0.])
    b = numpy.array([geometry.h_13_long * 100, geometry.h_13_short * 100, 0.])
    db = numpy.ones(len(a)) * 3.
    plot_functions.line_fit(a, b, db, 'tof', 'h', title = '')
    
    
    plt.ion() 
    plt.show()


