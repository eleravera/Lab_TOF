import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import argparse
import numpy
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
     
import geometry
import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file', '-f', default='None', type=str, help='Input file')
options_parser.add_argument('--plot_flag', '-p', default= False, type=bool, help='Flag to plot some distributions to test')

if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
    plot_flag = options['plot_flag']
   
    E, P, beta, x1, y1, theta, phi, x3, y3, f= numpy.loadtxt(input_file, unpack = True)
    mask = f > 0.5

    #Plot sulle distribuzioni dei dati generati: da usare come test
    if(plot_flag == True): 
      plot_functions.multiple_histogram(theta, phi, "theta", "phi", bins = 45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))  
      plot_functions.multiple_histogram(theta[mask], phi[mask], "theta[mask]", "phi[mask]", bins=45, range_var1 = (-numpy.pi, numpy.pi),  range_var2 = (0., numpy.pi*2))       
      plot_functions.multiple_histogram(x3, y3, "x3", "y3", bins=45)      
      plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]", bins=45)  
      plot_functions.multiple_histogram(x1, y1, "x1", "y1", bins=45)      
      plot_functions.multiple_histogram(x1[mask], y1[mask], "x1[mask]", "y1[mask]", bins=45)  
 


    #Forse meglio convertirli in tempi
    plot_functions.histogram(x1, "x1 [m]", "dN/dx", bins = None, range = None, f = True)
    
    plt.figure()
    n, bins, patches = plt.hist(x1, bins = int(numpy.sqrt(len(x1))) , range = (0., 2.9))
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    polynomial_f = interp1d(bin_centers, n, kind='cubic')    

    x_new = numpy.linspace(bin_centers.min(), bin_centers.max(), 1000, endpoint = True)    
    plt.plot(x_new, polynomial_f(x_new), '-')
    
 
 
 
 
    """Proviamo a fare la convoluzione"""
    """norm = 1/200 #bho, valori a caso
    mean = 1.58 #bho, valori a caso
    sigma = 0.2 #bho, valori a caso
    filtered = numpy.convolve(polynomial_f(x_new), gauss(x_new, norm, mean, sigma), mode='same') 
    print(polynomial_f(x_new)[1:10], gauss(x_new, norm, mean, sigma)[1:10] , filtered[1:10], len(x_new), len(filtered))
  
  
    plt.figure("convoluzione")
    plt.plot(x_new, filtered, '.')
    """
    
    plt.ion()
    plt.show()   
    
