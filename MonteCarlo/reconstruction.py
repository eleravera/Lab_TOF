import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.stats import pearsonr


import geometry
import signal_propagation
import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file', '-f', default='None', type=str, help='File of the events')
options_parser.add_argument('--delay', '-d', default='32', type=int, help='Delay')

if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    delay_ns = options['delay']
     
    #E[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag     
    E, P, beta, x1, y1, theta, phi, x3, y3, f  = numpy.loadtxt(input_file, unpack = True)
    y1 = y1*100
    y3 = y3*100
   
    mask = (f == 1) 
    print("efficienza/tot:", numpy.sum(mask), len(mask))
    
    delay = numpy.ones(len(E[mask])) * delay_ns
    Z13 = 0. #geometry.h_13
    
    T1, T2, T12 = signal_propagation.DT_12(x1[mask], delay)
    TOF = signal_propagation.Time_Of_Flight(x1[mask], x3[mask], Z13, beta[mask]) 
    T13 = signal_propagation.DT_13(x1[mask], x3[mask], delay, TOF) 
    T23 = signal_propagation.DT_23(x1[mask], x3[mask], delay, TOF) 
    n_bins = 50
    
    
    #correlazione
    r1_23, p1_23 = pearsonr(T12, T13)
    print("r, p T12 and T13:", r1_23, p1_23)
    r12_3, p12_3 = pearsonr(T23, T13)
    print("r, p T23 and T13:", r12_3, p12_3)
    

    plot_functions.multiple_histogram(x1[mask], x3[mask], "x1[mask]", "x3[mask]")
    plot_functions.multiple_histogram(T13, T23, "T13", "T23")       
    plot_functions.multiple_histogram(T13, T23, "T13", "T23")       
    plot_functions.scatter_plot(T12, T13, "T12 [ns]", "T13 [ns]")
    plot_functions.scatter_plot(T23, T13, "T23 [ns]", "T13 [ns]")  
    plot_functions.histogram(TOF, "TOF [ns]")   
    

    plt.ion()
    plt.show()
    
    
     
    
    
