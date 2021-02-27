import numpy
import matplotlib.pyplot as plt
import argparse 

import muon_generator

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--number_events', '-n', default=100, type=int, help='Numero di muoni da generare')
options_parser.add_argument('--output_File_events', '-f', default='None', type=str, help='File su cui scrivere gli eventi')


if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    N = options['number_events']
    output_file_events = options['output_File_events']
     
    """Genero un muone con le funzioni di muon_generator"""
    E, P, beta = muon_generator.muon_energy_generator(N) 
    theta, phi = muon_generator.muon_angle_generator(N)
    x1, y1 = muon_generator.position_on_S1_generator(N) 
    x3, y3 = muon_generator.propagation_from_S1_to_S3(x1, y1, theta, phi)
    
    t12 = muon_generator.DT_12(x1) 
    
    
    data = numpy.vstack((x1, y1, x3, y3)).T
    print(data)
    print(numpy.vstack((x3, y3)).T)
    
    plt.ion()
    plt.show()
    

