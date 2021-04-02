
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
options_parser.add_argument('-input_data_file_pb', '-ff', type=str, required = True, help='Input data file')
options_parser.add_argument('-input_data_file_pb2', '-fff', type=str, required = True, help='Input data file')
options_parser.add_argument('-salve_fig', '-fig', type=bool, default = False, help='save figure')


if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    input_data_file_pb = options['input_data_file_pb']
    input_data_file_pb2 = options['input_data_file_pb2']
    salve_fig = options['salve_fig']

    m, dm , costant, tau_diff = utilities.read_parameter('vs_x/T13_T23_vs_x.txt', 'vs_x/Tsum_Tdiff_vs_x.txt')
    
    t, ch0,  ch1  = numpy.loadtxt(input_file, unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    t_run = utilities.acquisition_duration(t)
    T13, T23 = utilities.TAC_scale(ch0, ch1) 
    mask = (T23 > 1.) * (T13 > 1.) * (T23 < 65.) * (T13 < 65.)
    T13 = T13[mask]
    T23 = T23[mask]
    figlabel = '_run' 
    
    t, ch0,  ch1  = numpy.loadtxt(input_data_file_pb, unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    T13_pb, T23_pb = utilities.TAC_scale(ch0, ch1) 
    t_run_pb = utilities.acquisition_duration(t)
    mask = (T23_pb > 1.) * (T13_pb > 1.) * (T23_pb < 65.) * (T13_pb < 65.)
    T13_pb = T13_pb[mask]
    T23_pb = T23_pb[mask]
    figlabel = '_run_pb' 

    t, ch0,  ch1  = numpy.loadtxt(input_data_file_pb2, unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    T13_pb2, T23_pb2 = utilities.TAC_scale(ch0, ch1) 
    t_run_pb2 = utilities.acquisition_duration(t)
    mask = (T23_pb2 > 1.) * (T13_pb2 > 1.) * (T23_pb2 < 65.) * (T13_pb2 < 65.)
    T13_pb2 = T13_pb2[mask]
    T23_pb2 = T23_pb2[mask]
    figlabel = '_run_pb2' 

    TOF = analysis_functions.TOF(T13, T23, costant) 
    T12 = analysis_functions.T12(T13, T23, tau_diff)
    x = analysis_functions.x(T12, m)   
    l = analysis_functions.l(x, geometry.h_13_long * 100,  geometry.s3 * 100)       
    beta = analysis_functions.beta(l,  geometry.h_13_long * 100, TOF)     
    plot_functions.hist2d(TOF, l,  "TOF [ns]", "l[cm]", bins=None, range_x = (-10., 20.), range_y = (170., 270.), norm = LogNorm())


    TOF_pb = analysis_functions.TOF(T13_pb, T23_pb, costant) 
    T12_pb = analysis_functions.T12(T13_pb, T23_pb, tau_diff)
    x_pb = analysis_functions.x(T12_pb, m )   
    l_pb = analysis_functions.l(x_pb,  geometry.h_13_long * 100,  geometry.s3 * 100)       
    beta_pb = analysis_functions.beta(l_pb,  geometry.h_13_long * 100, TOF_pb )     
    
    TOF_pb2 = analysis_functions.TOF(T13_pb2, T23_pb2, costant) 
    T12_pb2 = analysis_functions.T12(T13_pb2, T23_pb2, tau_diff)
    x_pb2 = analysis_functions.x(T12_pb2, m )   
    l_pb2 = analysis_functions.l(x_pb2,  geometry.h_13_long * 100,  geometry.s3 * 100)       
    beta_pb2 = analysis_functions.beta(l_pb2,  geometry.h_13_long * 100, TOF_pb2 )     
    
    
    plot_functions.two_histogram_data_MC(beta, beta_pb, "beta", "", bins = None, range = (0., 5.), density = False, title = '', labelx = 'con veto', labely = 'senza veto')
    plot_functions.three_histogram_data_MC(beta, beta_pb, beta_pb2, "beta", "", bins = None, range = (0., 5.), density = False, title = '', labelx = 'senza piombo', labely = '7 spessori', labelz='4 spessori')

    plt.ion()
    plt.show()
