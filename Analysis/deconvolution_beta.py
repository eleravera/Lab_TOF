
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')

import argparse 
import numpy
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from matplotlib.colors import LogNorm
from scipy import signal


import fit_functions
import plot_functions
import geometry
import analysis_functions
import utilities

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('-input_data_file', '-f', type=str, required = True, help='Input data file')
options_parser.add_argument('-input_simulation_file', '-s', type=str, default = None, help='Input simulation file')
options_parser.add_argument('-save_fig', '-fig', type=bool, default = False, help='save figure')
options_parser.add_argument('-save_file', '-fout', type=bool, default = False, help='save output file')

if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_data_file = options['input_data_file']
    input_simulation_file = options['input_simulation_file']
    save_fig = options['save_fig']
    save_file = options['save_file']  
 
    t, ch0,  ch1  = numpy.loadtxt(input_data_file, unpack = True)
    utilities.rate_and_saturation(t, ch0, ch1)
    t_run = utilities.acquisition_duration(t)
    T13, T23 = utilities.TAC_scale(ch0, ch1) 
    mask = (T23 > 1.) * (T13 > 1.) * (T23 < 65.) * (T13 < 65.)
    T13 = T13[mask]
    T23 = T23[mask]

    n_bins = 100
    legend = ''   
    figlabel = '_run'      
    date = ''    
    title = '%d eventi, %d secondi, %s' % (len(T13), t_run, date) 
    analysis_functions.Ti_histogram(T13, T23, bins=n_bins, range_T13=(0., 60.), range_T23=(0., 60.), norm = LogNorm(), legend = legend, save_fig = save_fig, title = title)
  
    m, dm , costant, tau_diff = utilities.read_parameter('vs_x/T13_T23_vs_x.txt', 'vs_x/Tsum_Tdiff_vs_x.txt')       
    TOF = analysis_functions.TOF(T13, T23, costant) 
    T12 = analysis_functions.T12(T13, T23, tau_diff)
    x = analysis_functions.x(T12, m )   
    l = analysis_functions.l(x, geometry.h_13_long * 100,  geometry.s3 * 100)       
    beta = analysis_functions.beta(l,  geometry.h_13_long * 100, TOF)  
    analysis_functions.tof_beta_histogram(TOF, T12, x, beta, save_fig = save_fig, figlabel = figlabel, title = title, legend = legend)
       
    lmin = 170
    lmax = 220
    bin_tof = 6
    l_bins_center, mean_tof, sigma_tof = analysis_functions.l_vs_TOF(l, TOF, lmin , lmax, bin_tof )
    
    # = utilities.make_opt_string(opt_true, pcov_true, s = string_x_n)      
    if save_file is True:    
      with open("TOF_vs_l%s.txt", "a") as output_file:
        output_file.write("l_bins_center, mean_tof, sigma_tof")
    
           
    if input_simulation_file is not None: 
      T23_sim, ris23_sim, T13_sim, ris13_sim, T12_sim, TOF_true_sim = numpy.loadtxt(input_simulation_file, unpack = True)      
      TOF_sim = analysis_functions.TOF(T13_sim, T23_sim, costant) 
      T12_sim = analysis_functions.T12(T13_sim, T23_sim, tau_diff)
      x_sim = analysis_functions.x(T12_sim, m )   
      l_sim = analysis_functions.l(x_sim, geometry.h_13_long * 100,  geometry.s3 * 100)       
      beta_sim = analysis_functions.beta(l_sim,  geometry.h_13_long * 100, TOF_sim)  
      analysis_functions.tof_beta_histogram(TOF_sim, T12_sim, x_sim, beta_sim, save_fig = save_fig, figlabel = figlabel, title = '', legend = legend)

      #deconvoluzione 

      plt.figure("beta_misurato")
      n, bins, patches = plt.hist(beta,  bins = 301, range = (0., 3.), density = False, label = '')    
      
      plt.figure("beta_simulazione")
      n_sim, bins_sim, patches = plt.hist(beta_sim,  bins = 201, range = range, density = False, label = '')    
      print("n simulazione:", n_sim)
      print(mask)
      mask = (n_sim > 0.)
      n_sim = n_sim[36:185]
      #n_sim = n_sim /n_sim.sum()

      plt.figure()
      plt.title("filter")
      plt.plot(n_sim)    
       
      #plt.figure()
      #plt.title("convoluzione")
      #input_signal = numpy.repeat([0., 1., 0.], 50)
      #conv = numpy.convolve(input_signal, n_sim, mode='same')
      #conv = conv / conv.sum()
      #plt.plot(conv)
      
      
      #n = n/n.sum()
      plt.figure()
      plt.title("deconvoluzione")
      recovered, remainder = signal.deconvolve(n, n_sim)    

       
      plt.plot(recovered)
      print(recovered)
      plt.figure()
      plt.plot(remainder)
      print(remainder)

    plt.ion() 
    plt.show()


