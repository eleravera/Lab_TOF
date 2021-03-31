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
options_parser.add_argument('-input_file', '-f', type=str, required = True, help='Input data file')
options_parser.add_argument('-save_fig', '-fig', type=bool, default = False, help='save figure')
options_parser.add_argument('-input_file_pb', '-pb', type=str, required = False, help='Input data file piombo') 
 
if __name__ == '__main__' :       
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    input_file_pb = options['input_file_pb']
    save_fig = options['save_fig']

    l_bins_center, mean_tof, sigma_tof  = numpy.loadtxt(input_file, unpack = True)
    
    print("\n----------Fit con retta vincolata a zero-------------")  
    opt, pcov = plot_functions.proportional_fit( l_bins_center, mean_tof,  sigma_tof, "l [cm]", "Tof [ns]")
    v = 1/ opt[0]
    dv = numpy.sqrt(pcov.diagonal())[0]/(opt[0])**2
    print("v+- dv", v, dv)
 
    
    print("\n\n----------Fit con retta------------------------") 
    opt, pcov = plot_functions.line_fit( l_bins_center, mean_tof,  sigma_tof, "l [cm]", "Tof [ns]")
    v = 1/ opt[0]
    dv = numpy.sqrt(pcov.diagonal())[0]/(opt[0])**2
    print("v+- dv", v, dv)
    
    #-----------------------------------------------------------------------------------------------------------------------
    
    print("\n\n\n----------Fit con retta vincolata a zero con pb-------------")
    
    if input_file_pb is not '':
      l_bins_center, mean_tof, sigma_tof  = numpy.loadtxt(input_file_pb, unpack = True)      
    opt, pcov = plot_functions.proportional_fit( l_bins_center, mean_tof,  sigma_tof, "l [cm]", "Tof [ns]")
    v = 1/ opt[0]
    dv = numpy.sqrt(pcov.diagonal())[0]/(opt[0])**2
    print("v+- dv", v, dv)
 
    
    print("\n\n----------Fit con retta con pb------------------------") 
    opt, pcov = plot_functions.line_fit( l_bins_center, mean_tof,  sigma_tof, "l [cm]", "Tof [ns]")
    v = 1/ opt[0]
    dv = numpy.sqrt(pcov.diagonal())[0]/(opt[0])**2
    print("v+- dv", v, dv)
    

    plt.ion()
    plt.show()
     
