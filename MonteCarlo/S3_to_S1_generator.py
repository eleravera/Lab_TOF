"""Genero un muone che passa nello scintillatore 3 a x fissato, e calcolo le cordinate in cui passerebbe nella barra scintillante. Le cordinate nello scintillatore 3 la chiamo _m (measured), e quelle nella barra scintillante _t (true)"""

import numpy
import argparse 
import datetime
import time

import muon_generator

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
    x_m, y_m = muon_generator.position_on_S3_generator(N, x)
    theta, phi = muon_generator.muon_angle_generator(N, muon_generator.dist_theta)
    x_t, y_t, f = muon_generator.propagation_from_S3_to_S1(x_m, y_m, theta, phi)

    data = numpy.vstack((x_m, y_m*100, theta, phi, x_t, y_t*100, f)).T  
    epsilon = numpy.sum(f)/N        
    print("x_m[m], y_m[cm], theta, phi, x_t[m], y_t[cm], flag \n", data)
    print("Number of events hitting S1/Total number of events:", numpy.sum(f), "/", N, "=", epsilon)
    
    if(output_file_events.endswith('.txt')): 
      header ='%s\nx_input = %d \nE[MeV], P[MeV], beta, x_m[m], y_m[cm], theta, phi, x_t[m], y_t[cm], flag\n' % (datetime.datetime.now() , x)
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.2f', '%.2f', '%.4f', '%.4f', '%d']
      numpy.savetxt(output_file_events, numpy.transpose([E, P, beta, x_m, y_m*100, theta, phi, x_t, y_t*100, f]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")


    print("Time of execution: %s seconds " % (time.time() - start_time))
 

