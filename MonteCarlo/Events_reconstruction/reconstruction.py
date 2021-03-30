import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.stats import pearsonr
import sys

sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import plot_functions
import fit_functions
import geometry
import signal_propagation_functions


description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file', '-fi', default='None', type=str, help='File of the events')
options_parser.add_argument('--plot_flag', '-p', default= False, type=bool, help='Flag to plot some distributions to test')
options_parser.add_argument('--output_File', '-fo', default='None', type=str, help='File su cui scrivere ')


if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    plot_flag = options['plot_flag']
    output_File = options['output_File']

    #E[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag     
    E, P, beta, x1, y1, theta, phi, x3, y3, f  = numpy.loadtxt(input_file, unpack = True)
    mask = f > 0.5
    print("efficienza/tot:", numpy.sum(f), len(f)) 
       
    delay_T13 = numpy.ones(int(numpy.sum(f))) * 26.1 #ns
    delay_T23 = numpy.ones(int(numpy.sum(f))) * 26.2 #ns
    delay_T12 = delay_T13
    z_13 = 1.77
   
    if(plot_flag == True): 
      plot_functions.multiple_histogram(theta, phi, '$\Theta[rad]$', "$\Phi[rad]$", bins = 45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2), density = True)  
      plot_functions.multiple_histogram(theta[mask], phi[mask], "$\Theta_{S3}[rad]$", "$\Phi_{S3}[rad]$", bins=45, range_var1 = (-1, 1),  range_var2 = (0., numpy.pi*2), density = True)       
      plot_functions.multiple_histogram(x3, y3, "x3", "y3", bins=45)      
      plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]", bins=45)  
      plot_functions.multiple_histogram(x1, y1, "$x [cm]$", "$y [cm]$", bins=45, density = True)      
      plot_functions.multiple_histogram(x1[mask], y1[mask], "$x_{S3} [cm]$",  "$y_{S3} [cm]$", bins=45, density = True)  
 
    
    
    ris23 = signal_propagation_functions.resolution( int(numpy.sum(f)), fit_functions.two_gauss, 1.98e-01, 1.068e+02, 0. , 1.74483e+00, 0.3856, 4.95658e-01 )
    ris13 = signal_propagation_functions.resolution( int(numpy.sum(f)), fit_functions.two_gauss, 1.98e-01, 1.068e+02, 0. , 1.74483e+00, 0.3856, 4.95658e-01 )
    T12 = signal_propagation_functions.DT_12(x1[mask], delay_T12, res = None) 
    TOF_true = signal_propagation_functions.Time_Of_Flight(x1[mask], x3[mask], y1[mask], y3[mask], z_13, beta[mask])   
    T13 = signal_propagation_functions.DT_13(x1[mask], x3[mask], delay_T13, TOF_true, ris13) 
    T23 = signal_propagation_functions.DT_23(x1[mask], x3[mask], delay_T23, TOF_true, ris23) 



    plot_functions.multiple_histogram(x1[mask], x3[mask], "x1[mask]", "x3[mask]", bins=45)
    plot_functions.multiple_histogram(T13, T23, "T13", "T23", bins=45)       
    plot_functions.scatter_plot(T12, T13, "T12 [ns]", "T13 [ns]")
    plot_functions.scatter_plot(T23, T13, "T23 [ns]", "T13 [ns]")  

    plot_functions.histogram(TOF_true, "TOF_true [ns]", "dN/dTOF", bins=100, range = (6., 9.), f = False)   
    plot_functions.hist2d(T23, T13, "T23", "T13", range_x = (15., 40.), range_y = (15., 40.)) 
    
    res = signal_propagation_functions.resolution( int(numpy.sum(f)), fit_functions.two_gauss, 1.98e-01, 1.068e+02, 0. , 1.74483e+00, 0.3856, 4.95658e-01 )
    plot_functions.histogram(res, "gauss_resolution [ns]", "dN/dres", bins = 100, range = (-5., +5), f=False)            

        
    r1_23, p1_23 = pearsonr(T12, T13)
    print("\n\nr, p T12 and T13:", r1_23, p1_23)
    r12_3, p12_3 = pearsonr(T23, T13)
    print("\nr, p T23 and T13:", r12_3, p12_3)
    

    if(output_File.endswith('.txt')): 
      header ='%s \n T23[ns] ris23[ns] T13[ns] ris13[ns] T12[ns] TOF_true[ns] \n'
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f']
      numpy.savetxt(output_File, numpy.transpose([T23, ris23, T13, ris13, T12, TOF_true]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")

    plt.ion()
    plt.show()
    
    
     
    
    
