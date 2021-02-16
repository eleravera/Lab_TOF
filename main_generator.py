import numpy
import matplotlib.pyplot as plt
import argparse 

from funzioni import muon_generator


description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--number_events', '-n', default=1, type=int, help='Numero di muoni da generare')
options_parser.add_argument('--output_File_events', '-f', default='None', type=str, help='File su cui scrivere gli eventi')


if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    N = options['number_events']
    output_file_events = options['output_File_events']
     
    "Genero un muone con le funzioni di muon_generator" 
    E = muon_generator.muon_energy_generator(N) 
    theta = muon_generator.muon_theta_generator(N)
    phi = muon_generator.muon_phi_generator(N) 
    x, y = muon_generator.position_generator(N) 
    
    
    #plt.show lo mettiamo per adesso qui per poter
    plt.show()

