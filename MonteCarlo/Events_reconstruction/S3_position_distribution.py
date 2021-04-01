
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse
import numpy
from scipy.integrate import quad
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

import geometry
import fit_functions
import plot_functions
import utilities
import signal_propagation_functions

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--input_file_simulation', '-f', default='None', type=str, help='Input file sim')
options_parser.add_argument('--save_fig', '-p', default=False, type=bool, help='')
options_parser.add_argument('--s3_position', '-x', type=int, help='position of s3')


if __name__ == '__main__' :   

    options = vars(options_parser.parse_args())  
    input_file_sim = options['input_file_simulation']
    save_fig = options['save_fig']
    position = options['s3_position']

    E, P, beta, x1, y1, theta, phi, x3, y3, f = numpy.loadtxt(input_file_sim, unpack = True)
    mask = (f == 1)
    
    title = 'Simulazione Monte Carlo per x = %d cm ' % position
    range = (position - 20.,  position + 20.)
    plot_functions.histogram(x1[mask]*100, "$x_{t}$[cm]", "entries/bin", bins = 150, range = range, f=False, density = False, title = title, legend = '')
    
   
 
    delay_T13 = 26.1 
    delay_T23 = 26.2
    res = 0.   
    TOF_sim = signal_propagation_functions.Time_Of_Flight(x1[mask], x3[mask], y1[mask], y3[mask], 0., beta[mask])
    T13_sim, _ = signal_propagation_functions.DT_13(x1[mask], x3[mask], y3[mask], delay_T13, TOF_sim, res = res) 


    title = 'Simulazione Monte Carlo per x = %d cm ' % position
    #range = (position - 20.,  position + 20.)
    plot_functions.histogram(T13_sim, "$T_{13,t }$[ns]", "entries/bin", bins = 150, range = (21., 25.), f=False, density = False, title = title, legend = '')
    
    
    if save_fig ==True:
      plt.savefig('../spline_%d.pdf' % position, format = 'pdf')     
    
    st_dev = numpy.std(x1[mask]*100)
    print(position, st_dev)
    
    plt.ion()
    plt.show()
    
    
    
    
