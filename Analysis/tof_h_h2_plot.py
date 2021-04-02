
import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


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


if __name__ == '__main__' :   

    bias_tof = 2.342
    
    input_data_file = 'dati/Run47.dat'
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
       
    input_data_fileh2 = 'dati/Run30.dat'
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
   
    TOF_h2 = analysis_functions.TOF(T13_h2, T23_h2, costant) 
    TOF_h2 = TOF_h2 + bias_tof
    T12_h2 = analysis_functions.T12(T13_h2, T23_h2, tau_diff)
    x_h2 = analysis_functions.x(T12_h2, m ) 
    x_h2 = numpy.sqrt(x_h2**2 + 36.) 
    l_h2 = analysis_functions.l(x_h2, geometry.h_13_short * 100,  geometry.s3 * 100)       
    beta_h2 = analysis_functions.beta(l_h2,  geometry.h_13_short * 100, TOF_h2)  


    input_simulation_file = 'T_drop_300.txt'
    T23_sim, ris23_sim, T13_sim, ris13_sim, T12_sim, TOF_true_sim = numpy.loadtxt(input_simulation_file, unpack = True)      

    TOF_sim = analysis_functions.TOF(T13_sim, T23_sim, costant) 
    TOF_sim = TOF_sim + bias_tof
    T12_sim = analysis_functions.T12(T13_sim, T23_sim, tau_diff)
    x_sim = analysis_functions.x(T12_sim, m )   
    x_sim = numpy.sqrt(x_sim**2 + 36.)
    l_sim = analysis_functions.l(x_sim, geometry.h_13_long * 100,  geometry.s3 * 100)       
    beta_sim = analysis_functions.beta(l_sim,  geometry.h_13_long * 100, TOF_sim)  

    input_simulation_file_h2 = 'T_drop_300_h2.txt'
    T23_sim_h2, ris23_sim_h2, T13_sim_h2, ris13_sim_h2, T12_sim_h2, TOF_true_sim_h2 = numpy.loadtxt(input_simulation_file_h2, unpack = True)      

    TOF_sim_h2 = analysis_functions.TOF(T13_sim_h2, T23_sim_h2, costant) 
    TOF_sim_h2 = TOF_sim_h2 + bias_tof
    T12_sim_h2 = analysis_functions.T12(T13_sim_h2, T23_sim_h2, tau_diff)
    x_sim_h2 = analysis_functions.x(T12_sim_h2, m )   
    x_sim_h2 = numpy.sqrt(x_sim_h2**2 + 36.)
    l_sim_h2 = analysis_functions.l(x_sim_h2, geometry.h_13_short * 100,  geometry.s3 * 100)       
    beta_sim_h2 = analysis_functions.beta(l_sim_h2,  geometry.h_13_short * 100, TOF_sim_h2)  
 
 
      
    plot_functions.four_histogram_data_MC(T13, T13_h2, T13_sim, T13_sim_h2, "$T_{13}$ [ns]", "a.u.", bins = None, range = (0., 60.), density = False, title = '', labelx = 'dati h = 177 cm', labely = 'dati h = 122 cm', labelz = 'sim. h = 177 cm', labelw = 'sim. h = 122 cm') 
    plot_functions.four_histogram_data_MC(T23, T23_h2, T23_sim, T23_sim_h2, "$T_{23}$ [ns]", "a.u.", bins = None, range = (0., 60.), density = False, title = '', labelx = 'dati h = 177 cm', labely = 'dati h = 122 cm', labelz = 'sim. h = 177 cm', labelw = 'sim. h = 122 cm')    
   
      
    plot_functions.four_histogram_data_MC(x, x_h2, x_sim, x_sim_h2, "x [cm]", "a.u.", bins = None, range = (-50., 330.), density = False, title = '', labelx = 'dati h = 177 cm', labely = 'dati h = 122 cm', labelz = 'sim. h = 177 cm', labelw = 'sim. h = 122 cm')
    plot_functions.four_histogram_data_MC(TOF, TOF_h2, TOF_sim, TOF_sim_h2, "Tof [ns]", "a.u.", bins = None, range = (-5., 25.), density = False, title = '',  labelx = 'dati h = 177 cm', labely = 'dati h = 122 cm', labelz = 'sim. h = 177 cm', labelw = 'sim. h = 122 cm')
    plot_functions.four_histogram_data_MC(beta, beta_h2, beta_sim, beta_sim_h2, "beta", "a.u.", bins = None, range = (0., 2.), density = False, title = '',  labelx = 'dati h = 177 cm', labely = 'dati h = 122 cm', labelz = 'sim. h = 177 cm', labelw = 'sim. h = 122 cm')


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
    
    plt.ion()
    plt.show()

