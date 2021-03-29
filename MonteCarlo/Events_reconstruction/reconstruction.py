import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.stats import pearsonr
import sys

sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import plot_functions
import geometry
import signal_propagation_functions


description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file', '-f', default='None', type=str, help='File of the events')
options_parser.add_argument('--z_scintillator', '-z', default='1.8', type=float, help='Position of the scintillator 3')
options_parser.add_argument('--plot_flag', '-p', default= False, type=bool, help='Flag to plot some distributions to test')
options_parser.add_argument('--output_File', '-fo', default='None', type=str, help='File su cui scrivere ')

if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    z_13 = options['z_scintillator']
    plot_flag = options['plot_flag']
    output_file = options['output_File']

    #E[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag     
    E, P, beta, x1, y1, theta, phi, x3, y3, f  = numpy.loadtxt(input_file, unpack = True)
    mask = f > 0.5
    print("efficienza/tot:", numpy.sum(f), len(f)) 
       
    delay_T13 = numpy.ones(int(numpy.sum(f))) * 26.1
    delay_T23 = numpy.ones(int(numpy.sum(f))) * 26.2 
    delay_T12 = delay_T13
    
   
    if(plot_flag == True): 
      plot_functions.multiple_histogram(theta, phi, '$\Theta[rad]$', "$\Phi[rad]$", bins = 45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2), density = True)  
      plot_functions.multiple_histogram(theta[mask], phi[mask], "$\Theta_{S3}[rad]$", "$\Phi_{S3}[rad]$", bins=45, range_var1 = (-1, 1),  range_var2 = (0., numpy.pi*2), density = True)       
      plot_functions.multiple_histogram(x3, y3, "x3", "y3", bins=45)      
      print(y3, y3[mask])
      plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]", bins=45)  
      plot_functions.multiple_histogram(x1, y1, "$x [cm]$", "$y [cm]$", bins=45, density = True)      
      plot_functions.multiple_histogram(x1[mask], y1[mask], "$x_{S3} [cm]$",  "$y_{S3} [cm]$", bins=45, density = True)  
 

    res = None
    T12 = signal_propagation_functions.DT_12(x1[mask], delay_T12, res) 
    TOF = signal_propagation_functions.Time_Of_Flight(x1[mask], x3[mask], y1[mask], y3[mask], z_13, beta[mask])   
    T13 = signal_propagation_functions.DT_13(x1[mask], x3[mask], delay_T13, TOF, res) 
    T23 = signal_propagation_functions.DT_23(x1[mask], x3[mask], delay_T23, TOF, res) 

    plot_functions.multiple_histogram(x1[mask], x3[mask], "x1[mask]", "x3[mask]", bins=45)
    plot_functions.multiple_histogram(T13, T23, "T13", "T23", bins=45)       
    plot_functions.scatter_plot(T12, T13, "T12 [ns]", "T13 [ns]")
    plot_functions.scatter_plot(T23, T13, "T23 [ns]", "T13 [ns]")  
    plot_functions.histogram(TOF, "TOF [ns]", "dN/dTOF", bins=100, range = (6., 9.), f = False)   
    plot_functions.hist2d(T23, T13, "T23", "T13", range_x = (15., 40.), range_y = (15., 40.)) 
    res = signal_propagation_functions.gauss_resolution(len(T13))
    plot_functions.histogram(res, "gauss_resolution [ns]", "dN/dres", bins = 100, range = (-5., +5))     
    
    
    r1_23, p1_23 = pearsonr(T12, T13)
    print("\n\nr, p T12 and T13:", r1_23, p1_23)
    r12_3, p12_3 = pearsonr(T23, T13)
    print("\nr, p T23 and T13:", r12_3, p12_3)
    

    if(output_file.endswith('.txt')): 
      t = numpy.ones(len(T13))
      header ='%s \nt[] T23[ns] T13[ns]\n'
      fmt = ['%.4f', '%.4f', '%.4f']
      numpy.savetxt(output_file, numpy.transpose([t, T23, T13]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")
      
    
    plt.ion()
    plt.show()
    
    
     
    
    
