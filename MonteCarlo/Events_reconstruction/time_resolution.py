import argparse
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
     
import geometry
import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file', '-f', default='None', type=str, help='Input file')

if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file = options['input_file']
   
    E, P, beta, x1, y1, theta, phi, x3, y3, f= numpy.loadtxt(input_file, unpack = True)


    #Forse meglio convertirli in tempi
    plot_functions.histogram(x1, "x1 [m]", "dN/dx", bins = None, range = None, f = True)




    n, bins, patches = plt.hist(x_t, bins = int(numpy.sqrt(len(x_m))) , range = (0., 1.2))
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    polynomial_f = interp1d(bin_centers, n, kind='cubic')    

    x_new = numpy.linspace(bin_centers.min(), bin_centers.max(), 1000, endpoint = True)    
    plt.plot(x_new, polynomial_f(x_new), '-')
    
 
 
 
 
    """Proviamo a fare la convoluzione"""
    norm = 1/200 #bho, valori a caso
    mean = 1.58 #bho, valori a caso
    sigma = 0.2 #bho, valori a caso
    filtered = numpy.convolve(polynomial_f(x_new), gauss(x_new, norm, mean, sigma), mode='same') 
    print(polynomial_f(x_new)[1:10], gauss(x_new, norm, mean, sigma)[1:10] , filtered[1:10], len(x_new), len(filtered))
  
  
    plt.figure("convoluzione")
    plt.plot(x_new, filtered, '.')
    
    
    plt.ion()
    plt.show()   
    
