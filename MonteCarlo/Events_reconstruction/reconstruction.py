import numpy
import matplotlib.pyplot as plt
import argparse 
from scipy.stats import pearsonr


import geometry
import signal_propagation_functions
import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file', '-f', default='None', type=str, help='File of the events')
options_parser.add_argument('--delay', '-d', default='32', type=int, help='Delay')
options_parser.add_argument('--z_scintillator', '-z', default='2.', type=float, help='Position of the scintillator 3')
options_parser.add_argument('--plot_flag', '-p', default= False, type=bool, help='Flag to plot some distributions to test')


if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    delay_ns = options['delay']
    z_13 = options['z_scintillator']
    plot_flag = options['plot_flag']

    #E[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag     
    E, P, beta, x1, y1, theta, phi, x3, y3, f  = numpy.loadtxt(input_file, unpack = True)
    y1 = y1
    y3 = y3
    mask = f > 0.5
       
    print("efficienza/tot:", numpy.sum(f), len(f))    
    delay = numpy.ones(int(numpy.sum(f))) * delay_ns
    
    
    #Plot sulle distribuzioni dei dati generati: da usare come test
    if(plot_flag == True): 
      plot_functions.multiple_histogram(theta, phi, "theta", "phi", bins = 45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))  
      plot_functions.multiple_histogram(theta[mask], phi[mask], "theta[mask]", "phi[mask]", bins=45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))       
      plot_functions.multiple_histogram(x3, y3, "x3", "y3", bins=45)      
      plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]", bins=45)  
      plot_functions.multiple_histogram(x1, y1, "x1", "y1", bins=45)      
      plot_functions.multiple_histogram(x1[mask], y1[mask], "x1[mask]", "y1[mask]", bins=45)  
 

    #Calcola i tempi di propagazione dei fotoni dentro la barra scintillante
    T12 = signal_propagation_functions.DT_12(x1[mask], delay)
    print("z13:", z_13)
    
    TOF = signal_propagation_functions.Time_Of_Flight(x1[mask], x3[mask], y1[mask], y3[mask], z_13, beta[mask])   
    T13 = signal_propagation_functions.DT_13(x1[mask], x3[mask], delay, TOF) 
    T23 = signal_propagation_functions.DT_23(x1[mask], x3[mask], delay, TOF) 

    #Plot sui Delta T misurati 
    plot_functions.multiple_histogram(x1[mask], x3[mask], "x1[mask]", "x3[mask]", bins=45)
    plot_functions.multiple_histogram(T13, T23, "T13", "T23", bins=45)       
    plot_functions.multiple_histogram(T13, T23, "T13", "T23", bins=45)       
    plot_functions.scatter_plot(T12, T13, "T12 [ns]", "T13 [ns]")
    plot_functions.scatter_plot(T23, T13, "T23 [ns]", "T13 [ns]")  
    plot_functions.histogram(TOF, "TOF [ns]", "dN/dTOF", bins=45, range = (5., 14.))   
    plot_functions.hist2d(T23, T13, "T23", "T13") 
    
    #Correlazione:
    r1_23, p1_23 = pearsonr(T12, T13)
    print("\n\nr, p T12 and T13:", r1_23, p1_23)
    r12_3, p12_3 = pearsonr(T23, T13)
    print("\nr, p T23 and T13:", r12_3, p12_3)
    

    
    plt.ion()
    plt.show()
    
    
     
    
    
