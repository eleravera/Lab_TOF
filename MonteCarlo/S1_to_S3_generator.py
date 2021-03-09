import numpy
import matplotlib.pyplot as plt
import argparse 
import datetime
import time

import muon_generator

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
    
    data = numpy.vstack((x1, y1, theta, phi, x3, y3, f)).T    
    epsilon = numpy.sum(f)/N 
    print("x1, y1, theta, phi, x3, y3, flag \n", data) 
            
    print("Number of events hitting S3/Total number of events on S1:", numpy.sum(f), "/", N, "=", epsilon)
            
    if(output_file_events.endswith('.txt')): 
      header ='%s \nE[MeV], P [MeV], beta, x1[m], y1[cm], theta, phi, x3[m], y3[cm], flag\n' % datetime.datetime.now()
      fmt = ['%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.2f', '%.2f', '%.4f', '%.4f', '%d']
      numpy.savetxt(output_file_events, numpy.transpose([E, P, beta, x1, y1*100, theta, phi, x3, y3*100, f]) , fmt=fmt, header=header)
      print("Output file saved!\n\n")
      
    print("Time of execution: %s seconds " % (time.time() - start_time))
      
#theta e phi     
    plt.figure("Theta e phi")
    plt.subplot(2, 2, 1)
    plt.hist(theta, bins = int(numpy.sqrt(N)))
    plt.xlabel("cos(theta)")
      
    plt.subplot(2, 2, 2)
    plt.hist(phi, bins = int(numpy.sqrt(N)))
    plt.xlabel("phi")
    
    plt.subplot(2, 2, 3)
    plt.hist(theta[f], bins = int(numpy.sqrt(N)))
    plt.xlabel("cos(theta)")   

    plt.subplot(2, 2, 4)
    plt.hist(phi[f], bins = int(numpy.sqrt(N)))
    plt.xlabel("phi")
        
#xs3
    plt.figure("Muon position on scintillator 3 ")
    plt.subplot(2, 2, 1)
    plt.hist(x3,  bins = int(numpy.sqrt(len(theta))))
    plt.xlabel("x_s3 [m]")
  
    plt.subplot(2, 2, 2)
    plt.hist(y3* 10**2,  bins = int(numpy.sqrt(len(theta)))  )
    plt.xlabel("y_s3 [cm]")  

    plt.subplot(2, 2, 3)
    plt.hist(x3[mask],  bins = int(numpy.sqrt(len(theta))))
    plt.xlabel("x_s3 [m]")
  
    plt.subplot(2, 2, 4)
    plt.hist(y3[mask]* 10**2,  bins = int(numpy.sqrt(len(theta)))  )
    plt.xlabel("y_s3 [cm]")  

#xs3
    plt.figure("Muon position on scintillator 1 ")
    plt.subplot(2, 2, 1)
    plt.hist(x1,  bins = int(numpy.sqrt(len(theta))))
    plt.xlabel("x_s3 [m]")
  
    plt.subplot(2, 2, 2)
    plt.hist(y1* 10**2,  bins = int(numpy.sqrt(len(theta)))  )
    plt.xlabel("y_s3 [cm]")  

    plt.subplot(2, 2, 3)
    plt.hist(x1[mask],  bins = int(numpy.sqrt(len(theta))))
    plt.xlabel("x_s3 [m]")
  
    plt.subplot(2, 2, 4)
    plt.hist(y1[mask]* 10**2,  bins = int(numpy.sqrt(len(theta)))  )
    plt.xlabel("y_s3 [cm]")  

#zeta

    print("zeta è: ", z)
    
    plt.ion()
    plt.show()
