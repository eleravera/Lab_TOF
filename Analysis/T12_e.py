import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import numpy
import matplotlib.pyplot as plt

import fit_functions
import plot_functions
import geometry
import analysis_functions
import utilities

if __name__ == '__main__' :   
    m, dm , costant, tau_diff = utilities.read_parameter('vs_x/T13_T23_vs_x.txt', 'vs_x/Tsum_Tdiff_vs_x.txt')

    t, ch0,  ch1  = numpy.loadtxt('Run65.dat', unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    t_run = utilities.acquisition_duration(t)      
    t12, tau = utilities.TAC_scale(ch0, ch1) 
    
    #t12 = t12[:3000]
    
    t, ch0,  ch1  = numpy.loadtxt('Run64.dat', unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    t_run = utilities.acquisition_duration(t)      
    T12, tau = utilities.TAC_scale(ch0, ch1) 
    
    #T12 = T12[:3000] 
      
    T12 = numpy.concatenate((t12, T12))  
      
    bins = 101
    range = (0., 70.)
    


    title = '%d eventi %d secondi, %s' % (len(T12), t_run, '31/03/21')
    plot_functions.histogram(T12, "$T_{12} [ns]$", "", f = False, bins = bins, title = title, legend = '')
    #x = 0.5 * (2. + 280. - T12*15)
    T12 = T12 - 42.
    x = 140. - 7.7 * T12 
    #x = analysis_functions.x(T12, m ) 
    
    plot_functions.histogram(x, "x [cm]", "", f = False, bins = bins) 
    
    
    
    plt.ion()
    plt.show()
    
