import numpy
import matplotlib.pyplot as plt
import argparse 
import datetime
import time

import muon_generator
import plot_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--number_events', '-n', default=100, type=int, help='Numero di muoni da generare')
options_parser.add_argument('--output_File_events', '-f', default='None', type=str, help='File su cui scrivere gli eventi')


if __name__ == '__main__' :   
    
    start_time = time.time()   
    options = vars(options_parser.parse_args())  
    N = options['number_events']
    output_file_events = options['output_File_events']
     
    """Genero un muone con le funzioni di muon_generator"""
    E, P, beta = muon_generator.muon_energy_generator(N) 
    theta, phi = muon_generator.muon_angle_generator(N, muon_generator.dist_theta)
    
    x1, y1 = muon_generator.position_on_S1_generator(N) 
    x3, y3, mask, z = muon_generator.propagation_from_S1_to_S3(x1, y1, theta, phi)
    
    f = mask>0
    epsilon = numpy.sum(f)/N    
    data = numpy.vstack((x1, y1, theta, phi, x3, y3, f)).T    

    print("x1, y1, theta, phi, x3, y3, flag \n", data)         
    print("Number of events hitting S3/Total number of events on S1:", numpy.sum(f), "/", N, "=", epsilon)
            
    if(output_file_events.endswith('.txt')): 
      header ='%s \nE[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag\n' % datetime.datetime.now()
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.2f', '%.2f', '%.4f', '%.4f', '%d']
      numpy.savetxt(output_file_events, numpy.transpose([E, P, beta, x1, y1*100, theta, phi, x3, y3*100, f]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")
      
    print("Time of execution: %s seconds " % (time.time() - start_time))
      
      
    plot_functions.multiple_histogram(theta, phi, "theta", "phi")  
    plot_functions.multiple_histogram(theta[mask], phi[mask], "theta[mask]", "phi[mask]")       
    plot_functions.multiple_histogram(x3, y3, "x3", "y3")      
    plot_functions.multiple_histogram(x3[mask], y3[mask], "x3[mask]", "y3[mask]")  
    plot_functions.multiple_histogram(x1, y1, "x1", "y1")      
    plot_functions.multiple_histogram(x1[mask], y1[mask], "x1[mask]", "y1[mask]")  
 
    plt.ion()
    plt.show()
