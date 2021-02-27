"""Genero un muone che passa nello scintillatore 3 a x fissato, e calcolo le cordinate in cui passerebbe nella barra scintillante. Le cordinate nello scintillatore 3 la chiamo _m (measured), e quelle nella barra scintillante _t (true)"""

"""Al solito devo usare la funzione che genera theta phi. 

Devo scrivere una funzione che associa a x_t un x_r

devo scrivere una funzione che presi questi dati faccia un fit dell'istogramma!

"""

import numpy
import matplotlib.pyplot as plt
import argparse 

import muon_generator
import geometry

description = ''
options_parser = argparse.ArgumentParser(description = description)
options_parser.add_argument('--number_events', '-n', default=100, type=int, help='Numero di muoni da generare')
options_parser.add_argument('--position', '-x', default=1., type=float, help='Posizione dello scintillatore 3 sulla barra [m]')

if __name__ == '__main__' :   
   
    options = vars(options_parser.parse_args())  
    N = options['number_events']
    x = options['position']
    
    
    x_m, y_m = muon_generator.position_on_S3_generator(N, x)
    theta, phi = muon_generator.muon_angle_generator(N)
    x_t, y_t, f = muon_generator.propagation_from_S3_to_S1(x_m, y_m, theta, phi)

    data = numpy.vstack((x_m, y_m*100, theta, phi, x_t, y_t*100, f)).T   
    print("x_m[m], y_m[cm], theta, phi, x_t[m], y_t[cm], flag \n", data)
       
    epsilon = numpy.sum(f)/N   
    print("Number of events hitting S1/Total number of events:", numpy.sum(f), "/", N, "=", epsilon)
    
       
    plt.figure(10)
    plt.subplot(2, 1 , 1)
    plt.hist(x_t, bins = int(numpy.sqrt(N)) , range = (0., geometry.X1))
    plt.xlabel("x_true [m]")
    plt.subplot(2, 1, 2)
    plt.hist(y_t, range = (-geometry.Y1, geometry.Y1))
    

    plt.ion()
    plt.show()   
    
    
