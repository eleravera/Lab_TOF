"""Genero un muone che passa nello scintillatore 3 a x fissato, e calcolo le cordinate in cui passerebbe nella barra scintillante. Le cordinate nello scintillatore 3 la chiamo _m (measured), e quelle nella barra scintillante _t (true)"""

import numpy
import argparse 
import datetime
import time
import matplotlib.pyplot as plt

import muon_generator
import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--number_events', '-n', default=100, type=int, help='Numero di muoni da generare')
options_parser.add_argument('--position', '-x', default=1., type=float, help='Posizione dello scintillatore 3 sulla barra [m]')
options_parser.add_argument('--output_File_events', '-f', default='None', type=str, help='File su cui scrivere gli eventi')

if __name__ == '__main__' :   

    start_time = time.time()      
    options = vars(options_parser.parse_args())  
    N = options['number_events']
    x = options['position']
    output_file_events = options['output_File_events']
              
    E, P, beta = muon_generator.muon_energy_generator(N) 
    x3, y3 = muon_generator.position_on_S3_generator(N, x)
    theta, phi = muon_generator.muon_angle_generator(N, muon_generator.dist_theta)
    x1, y1, f = muon_generator.propagation_from_S3_to_S1(x3, y3, theta, phi)

    data = numpy.vstack((x1, y1*100, theta, phi, x3, y3*100, f)).T  
    epsilon = numpy.sum(f)/N        
    print("x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag \n", data)
    print("Number of events hitting S1/Total number of events:", numpy.sum(f), "/", N, "=", epsilon)
    
    if(output_file_events.endswith('.txt')): 
      header ='%s\nx_input = %d \nE[MeV], P[MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag\n' % (datetime.datetime.now() , x)
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.2f', '%.2f', '%.4f', '%.4f', '%d']
      numpy.savetxt(output_file_events, numpy.transpose([E, P, beta, x1, y1*100, theta, phi, x3, y3*100, f]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")


    print("Time of execution: %s seconds " % (time.time() - start_time))


    plot_functions.multiple_histogram(theta, phi, "theta", "phi")  
    plot_functions.multiple_histogram(theta[f], phi[f], "theta[mask]", "phi[mask]")       
    
    plot_functions.multiple_histogram(x3, y3, "x3", "y3")      
    plot_functions.multiple_histogram(x3[f], y3[f], "x3[mask]", "y3[mask]")  
    plot_functions.multiple_histogram(x1, y1, "x1", "y1")      
    plot_functions.multiple_histogram(x1[f], y1[f], "x1[mask]", "y1[mask]")  
  
    plt.ion()
    plt.show()
