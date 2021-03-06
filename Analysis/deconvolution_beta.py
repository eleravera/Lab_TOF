
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
options_parser.add_argument('-input_data_fileh2', '-ff', type=str, default='None', help='Input data file')
options_parser.add_argument('-input_simulation_file', '-s', type=str, default = None, help='Input simulation file')
options_parser.add_argument('-save_fig', '-fig', type=bool, default = False, help='save figure')
options_parser.add_argument('-output_file', '-fout', type=str, default='None', help='save output file')

if __name__ == '__main__' :   
    options = vars(options_parser.parse_args())  
    input_data_file = options['input_data_file']
    input_simulation_file = options['input_simulation_file']
    save_fig = options['save_fig']
    output_file = options['output_file']  
    input_data_fileh2 = options['input_data_fileh2']
    bias_tof = 2.342
    
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
    #analysis_functions.Ti_histogram(T13, T23, bins=n_bins, range_T13=(0., 60.), range_T23=(0., 60.), norm = LogNorm(), legend = legend, save_fig = save_fig, title = title)
  
    m, dm , costant, tau_diff = utilities.read_parameter('vs_x/T13_T23_vs_x.txt', 'vs_x/Tsum_Tdiff_vs_x.txt')       
    TOF = analysis_functions.TOF(T13, T23, costant) 
    TOF = TOF + bias_tof
    T12 = analysis_functions.T12(T13, T23, tau_diff)
    x = analysis_functions.x(T12, m ) 
    x = numpy.sqrt(x**2 + 36.)
    l = analysis_functions.l(x, geometry.h_13_long * 100,  geometry.s3 * 100)       
    beta = analysis_functions.beta(l,  geometry.h_13_long * 100, TOF)  
    #analysis_functions.tof_beta_histogram(TOF, T12, x, l, beta, save_fig = save_fig, figlabel = figlabel, title = title, legend = legend)
       
    
    if input_data_fileh2 is not None:    
      t, ch0,  ch1  = numpy.loadtxt(input_data_fileh2, unpack = True)
      utilities.rate_and_saturation(t, ch0, ch1)
      t_run = utilities.acquisition_duration(t)
      T13_h2, T23_h2 = utilities.TAC_scale(ch0, ch1) 
      mask = (T23_h2 > 1.) * (T13_h2 > 1.) * (T23_h2 < 65.) * (T13_h2 < 65.)
      T13_h2 = T13_h2[mask]
      T23_h2 = T23_h2[mask]
       
      n_bins = 100
      legend = ''   
      figlabel = '_run30'      
      date = ''    
      title = '%d eventi, %d secondi, %s' % (len(T13_h2), t_run, date) 
      #analysis_functions.Ti_histogram(T13, T23, bins=n_bins, range_T13=(0., 60.), range_T23=(0., 60.), norm = LogNorm(), legend = legend, save_fig = save_fig, title = title)
    
      TOF_h2 = analysis_functions.TOF(T13_h2, T23_h2, costant) 
      TOF_h2 = TOF_h2 + bias_tof
      T12_h2 = analysis_functions.T12(T13_h2, T23_h2, tau_diff)
      x_h2 = analysis_functions.x(T12_h2, m ) 
      l_h2 = analysis_functions.l(x_h2, geometry.h_13_short * 100,  geometry.s3 * 100)       
      beta_h2 = analysis_functions.beta(l_h2,  geometry.h_13_short * 100, TOF_h2+bias_tof)  
      #analysis_functions.tof_beta_histogram(TOF_h2, T12_h2, x_h2, l_h2, beta_h2, save_fig = save_fig, figlabel = figlabel, title = title, legend = legend)

      
      plot_functions.two_histogram_data_MC(x, x_h2, "x [cm]", "", bins = None, range = (-10., 300.), density = False, title = '', labelx = 'h = 177 cm', labely = 'h = 122 cm')
      plot_functions.two_histogram_data_MC(TOF, TOF_h2, "Tof [ns]", "", bins = None, range = (-10., 30.), density = False, title = '', labelx = 'h = 177 cm', labely = 'h = 122 cm')
      plot_functions.two_histogram_data_MC(beta, beta_h2, "beta", "", bins = None, range = (0., 3.), density = False, title = '', labelx = 'h = 177 cm', labely = 'h = 122 cm')


    if input_simulation_file is not None: 
      T23_sim, ris23_sim, T13_sim, ris13_sim, T12_sim, TOF_true_sim = numpy.loadtxt(input_simulation_file, unpack = True)      

      #analysis_functions.Ti_histogram(T13_sim, T23_sim, bins=n_bins, range_T13=(0., 60.), range_T23=(0., 60.), norm = LogNorm(), legend = legend, save_fig = save_fig, title = 'simulazioni')
      TOF_sim = analysis_functions.TOF(T13_sim, T23_sim, costant) 
      TOF_sim = TOF_sim + bias_tof
      T12_sim = analysis_functions.T12(T13_sim, T23_sim, tau_diff)
      x_sim = analysis_functions.x(T12_sim, m )   
      #x_sim = numpy.sqrt(x_sim**2 - 60.)
      l_sim = analysis_functions.l(x_sim, geometry.h_13_long * 100,  geometry.s3 * 100)       
      beta_sim = analysis_functions.beta(l_sim,  geometry.h_13_long * 100, TOF_sim)  
      #analysis_functions.tof_beta_histogram(TOF_sim, T12_sim, x_sim, l_sim, beta_sim, save_fig = save_fig, figlabel = figlabel, title = '', legend = legend)
      
      plot_functions.two_histogram_data_MC(T13, T13_sim, "$T_{13}$", "", bins = 100, density = False, title = title, labelx = 'dati', labely= 'simulazione', range = (0., 60.))
      
      plot_functions.two_histogram_data_MC(T23, T23_sim, "$T_{23}$", "", bins = 100, density = False, title = title, labelx = 'dati', labely= 'simulazione', range = (0., 60.))
        
      plot_functions.two_histogram_data_MC(TOF, TOF_sim, "$Tof [ns]$", "", bins = 100, density = False, title = title, labelx = 'dati', labely= 'simulazione', range = (-10., 20.))
      
      plot_functions.two_histogram_data_MC(x, x_sim, "x [cm]", "", bins = None, range = (-10., 300.), density = False, title = '', labelx = 'dati', labely = 'simulazione')
 
      plot_functions.two_histogram_data_MC(T12, T12_sim, "$T12$", "", bins = 100, density = False, title = title, labelx = 'dati', labely= 'simulazione')
      
      plot_functions.two_histogram_data_MC(beta, beta_sim, "$beta$", "", bins = 100, density = False, title = title, labelx = 'dati', labely= 'simulazione', range = (0., 3.))
      
               
 
      """
      l = numpy.concatenate((l, l_h2))
      TOF = numpy.concatenate((TOF, TOF_h2))
      plot_functions.hist2d( l, TOF, "l [cm]", "Tof [ns]", bins=None, range_y = (-10., 15.), range_x = (110., 240.), norm = LogNorm(), title = '', legend = '')
      lmin = 120
      lmax = 220
      bin_tof = 10
      l_bins_center, mean_tof, sigma_tof, n_per_bin = analysis_functions.l_vs_TOF(l, TOF, lmin , lmax, bin_tof )
      print(" l_bins_center", l_bins_center)
      print("mean_tof", mean_tof)
      print("sigma_tof", sigma_tof)
      
      dl = numpy.ones(len(l_bins_center)) * 10./numpy.sqrt(12)
      sigma = numpy.sqrt(sigma_tof**2 + (0.0427*dl)**2)
      opt, pcov = plot_functions.line_fit(l_bins_center, mean_tof, "l [cm]", "Tof [ns]", dx = dl, dy = sigma_tof, err_fit = sigma_tof, title = 'Tof vs l')
      muon_speed = 1/opt[0]
      dmuon_speed = numpy.sqrt(numpy.diagonal(pcov)[0]) * muon_speed**2
      print("c, dc = ", muon_speed, dmuon_speed)
      """
      
    if(output_file.endswith('.txt')): 
      header ='l_bins_center[cm], mean_tof[ns], sigma_tof[ns], n_per_bin\n' 
      fmt = ['%.4f', '%.4f', '%.4f', '%d']
      numpy.savetxt(output_file, numpy.transpose([l_bins_center, mean_tof, sigma_tof, n_per_bin]) , fmt=fmt, header=header)
         
          
          
      
      
      
      
      
      """
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
      """
    plt.ion() 
    plt.show()


