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
options_parser.add_argument('--z_scintillator', '-z', default='2.', type=float, help='Position of the scintillator 3')
options_parser.add_argument('--plot_flag', '-p', default='False', type=int, help='Flag to plot some distributions to test')


if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    delay_ns = options['delay']
    z_13 = options['z_scintillator']
    plot_flag = options['plot_flag']

    #E[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag     
    E, P, beta, x1, y1, theta, phi, x3, y3, f  = numpy.loadtxt(input_file, unpack = True)
    y1 = y1*100
    y3 = y3*100
    mask = f > 0.5
       
    print("efficienza/tot:", numpy.sum(f), len(f))    
    delay = numpy.ones(int(numpy.sum(f))) * delay_ns
    
    
    #Plot sulle distribuzioni dei dati generati: da usare come test
    if(p == True): 
      plot_functions.multiple_histogram(theta, phi, "theta", "phi")  
      plot_functions.multiple_histogram(theta[mask], phi[mask], "theta[mask]", "phi[mask]")       
      plot_functions.multiple_histogram(x3, y3, "x3", "y3")      
      plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]")  
      plot_functions.multiple_histogram(x1, y1, "x1", "y1")      
      plot_functions.multiple_histogram(x1[mask], y1[mask], "x1[mask]", "y1[mask]")  
 

    #Calcola i tempi di propagazione dei fotoni dentro la barra scintillante
    T12 = signal_propagation.DT_12(x1[mask], delay)
    TOF = signal_propagation.Time_Of_Flight(x1[mask], x3[mask], y1[mask], y3[mask], z_13, beta[mask]) 
    T13 = signal_propagation.DT_13(x1[mask], x3[mask], delay, TOF) 
    T23 = signal_propagation.DT_23(x1[mask], x3[mask], delay, TOF) 

    #Plot sui Delta T misurati 
    plot_functions.multiple_histogram(x1[mask], x3[mask], "x1[mask]", "x3[mask]")
    plot_functions.multiple_histogram(T13, T23, "T13", "T23")       
    plot_functions.multiple_histogram(T13, T23, "T13", "T23")       
    plot_functions.scatter_plot(T12, T13, "T12 [ns]", "T13 [ns]")
    plot_functions.scatter_plot(T23, T13, "T23 [ns]", "T13 [ns]")  
    plot_functions.histogram(TOF, "TOF [ns]", range_var = (5., 14.))   
    plot_functions.hist2d(T23, T13, "T23", "T13") 
    
    #Correlazione:
    r1_23, p1_23 = pearsonr(T12, T13)
    print("\n\nr, p T12 and T13:", r1_23, p1_23)
    r12_3, p12_3 = pearsonr(T23, T13)
    print("\nr, p T23 and T13:", r12_3, p12_3)
    

    
    plt.ion()
    plt.show()
    
    
     
    
    
