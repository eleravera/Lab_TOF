
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
options_parser.add_argument('-input_simulation_file', '-s', type=str, default = None, help='Input simulation file')
options_parser.add_argument('-salve_fig', '-fig', type=bool, default = False, help='save figure')


def Ti_histogram(T13, T23, bins, range_T13, range_T23, salve_fig, figlabel): 
  plot_functions.histogram(T23, "$T_{23} [ns]$", "entries/bin", bins , f = False, legend = '')
  plot_functions.histogram(T13, "$T_{13} [ns]$", "entries/bin", bins = bins , f = False, legend = '')
  plot_functions.hist2d(T23, T13, "$T_{23} [ns]$", "$T_{13} [ns]$", bins=None, range_x = range_T23, range_y = range_T13, save_fig = salve_fig, figlabel = figlabel )
  r, p = pearsonr(T23, T13)
  print("r, p T23 and T13:", r, p)
  return 

def beta_and_tof_analysis(T13, T23, costant, tau_diff, salve_fig, figlabel, h, p3):  
  TOF = analysis_functions.TOF(T13, T23, costant, save_fig = salve_fig, figlabel = figlabel) 
  T12 = analysis_functions.T12(T13, T23, tau_diff)
  x = analysis_functions.x(T12, m , save_fig = salve_fig, figlabel = figlabel)   
  l = analysis_functions.l(x, h, p3)       
  beta = analysis_functions.beta(l, h, TOF, save_fig = salve_fig, figlabel = figlabel )     
  plot_functions.hist2d(TOF, l,  "TOF [ns]", "l[cm]", bins=None, range_x = (-10., 20.), range_y = (170., 270.), norm = LogNorm())
  analysis_functions.l_vs_TOF(l, TOF, 170., 220., 6)
  plot_functions.hist2d((T23+T13)*0.5-costant, T13-T23, "$T_{sum} [ns]$", "$T_{diff} [ns]$", range_x = (0., 11.), range_y = (-20., 20.), bins=None, norm = LogNorm())
  return 

if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_data_file = options['input_data_file']
    input_simulation_file = options['input_simulation_file']
    salve_fig = options['salve_fig']
     
    
    t, ch0,  ch1  = numpy.loadtxt(input_data_file, unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    T13, T23 = utilities.TAC_scale(ch0, ch1) 
    mask = (T23 > 1.) * (T13 > 1.) * (T23 < 65.) * (T13 < 65.)
    T13 = T13[mask]
    T23 = T23[mask]
    figlabel = '_run' 
        

    #Lettura parametri da file
    input_file_T13_T23_vs_x = 'vs_x/T13_T23_vs_x.txt'
    input_file_Tsum_Tdiff_vs_x = 'vs_x/Tsum_Tdiff_vs_x.txt'
    m, q, dm, dq, c, dc  = numpy.loadtxt(input_file_T13_T23_vs_x, unpack = True)
    a, b, da, db = numpy.loadtxt(input_file_Tsum_Tdiff_vs_x, unpack = True)  
  
    weights = 1/dm**2
    m = sum(a * weights) / sum(weights)
    dm = numpy.sqrt(dm[0]**2 + dm[1]**2 )


    x = numpy.linspace(-10., 300., 1000)
    costant = fit_functions.line(x, a[0], b[0])

    costant = 17.2 #da definire in funzione di x 
    tau_diff = q[1] - q[0] #tau23 - tau13    
      

    Ti_histogram(T13, T23, 50, (0., 60.), (0., 60.), salve_fig, figlabel)
    beta_and_tof_analysis(T13, T23, costant, tau_diff, salve_fig, figlabel, geometry.h_13_long * 100, geometry.s3 * 100)


    T23, res23, T13 , res13, T12, TOF  = numpy.loadtxt(input_simulation_file, unpack = True)
    
    figlabel = '_MC' 
    Ti_histogram(T13, T23, 50, (0., 60.), (0., 60.), salve_fig, figlabel)
    beta_and_tof_analysis(T13, T23, costant, tau_diff, salve_fig, figlabel, geometry.h_13_long * 100, geometry.X1 * 50)
    plot_functions.histogram(TOF, "TOF_true", "", bins = None, range = None, f=False, density = False, title = '', legend = '')   
    
    
    plt.ion() 
    plt.show()


