import argparse
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
     
import geometry

def gauss(x, norm, mean, sigma): 
  return (norm) * numpy.exp(-0.5 * ((x - mean)/sigma )**2)

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_File_events', '-f', default='None', type=str, help='File dati')

if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file = options['input_File_events']
   
    x_m, y_m, theta, phi, x_t, y_t, f  = numpy.loadtxt(input_file, unpack = True)

    plt.figure("Distribuzione X_t")
    #plt.subplot(2, 1 , 1)
    plt.xlabel("x_true [m]")
    n, bins, patches = plt.hist(x_t, bins = int(numpy.sqrt(len(x_m))) , range = (0., geometry.X1))
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    polynomial_f = interp1d(bin_centers, n, kind='cubic')    
    #opt, pcov = curve_fit(gauss, bin_centers, n)    
    #print(opt, pcov) 
    #plt.plot(numpy.linspace(0, geometry.X1, 1000), gauss(numpy.linspace(0, geometry.X1, 1000) , *opt), '-r')  
     
    x_new = numpy.linspace(bin_centers.min(), bin_centers.max(), 1000, endpoint = True)    
    plt.plot(x_new, polynomial_f(x_new), '-')
    
    #plt.subplot(2, 1, 2)   
    #plt.hist(y_t*100, int(numpy.sqrt(len(x_m))), range = (-geometry.Y1*100, geometry.Y1*100))
    #plt.xlabel("y_true [cm]")
 
 
 
 
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
    