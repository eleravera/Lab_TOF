
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
options_parser.add_argument('-input_data_file', '-f', type=str, required = True, help='Input data file')
options_parser.add_argument('-input_data_file_1', '-ff', type=str, required = False, help='Input data file')
options_parser.add_argument('-input_simulation_file', '-s', type=str, default = None, help='Input simulation file')
options_parser.add_argument('-salve_fig', '-fig', type=bool, default = False, help='save figure')


def Ti_histogram(T13, T23, bins, range_T13, range_T23, salve_fig, figlabel): 
  plot_functions.histogram(T23, "$T_{23} [ns]$", "entries/bin", bins , f = False, legend = '')
  plot_functions.histogram(T13, "$T_{13} [ns]$", "entries/bin", bins = bins , f = False, legend = '')
  plot_functions.hist2d(T23, T13, "$T_{23} [ns]$", "$T_{13} [ns]$", bins=None, range_x = range_T23, range_y = range_T13, save_fig = salve_fig, figlabel = figlabel )
  r, p = pearsonr(T23, T13)
  print("r, p T23 and T13:", r, p)
  return 

if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_data_file = options['input_data_file']
    salve_fig = options['salve_fig']

    m, dm , costant, tau_diff = utilities.read_parameter('vs_x/T13_T23_vs_x.txt', 'vs_x/Tsum_Tdiff_vs_x.txt')
    
    t, ch0,  ch1  = numpy.loadtxt(input_data_file, unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    T13, T23 = utilities.TAC_scale(ch0, ch1) 
    mask = (T23 > 1.) * (T13 > 1.) * (T23 < 65.) * (T13 < 65.)
    T13 = T13[mask]
    T23 = T23[mask]
    figlabel = '_run' 
             
    Ti_histogram(T13, T23, 50, (0., 60.), (0., 60.), salve_fig, figlabel)
    
    TOF = analysis_functions.TOF(T13, T23, costant, save_fig = salve_fig, figlabel = figlabel) 
    T12 = analysis_functions.T12(T13, T23, tau_diff)
    x = analysis_functions.x(T12, m , save_fig = salve_fig, figlabel = figlabel)   
    l = analysis_functions.l(x, geometry., p3)       
    beta = analysis_functions.beta(l, h, TOF, save_fig = salve_fig, figlabel = figlabel )     
    plot_functions.hist2d(TOF, l,  "TOF [ns]", "l[cm]", bins=None, range_x = (-10., 20.), range_y = (170., 270.), norm = LogNorm())
    analysis_functions.l_vs_TOF(l, TOF, 170., 220., 6)
    plot_functions.hist2d((T23+T13)*0.5-costant, T13-T23, "$T_{sum} [ns]$", "$T_{diff} [ns]$", range_x = (0., 11.), range_y = (-20., 20.), bins=None, norm = LogNorm())
      
    plt.ion() 
    plt.show()


