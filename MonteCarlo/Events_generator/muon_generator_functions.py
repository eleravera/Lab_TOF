import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import numpy
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.integrate import quad
from scipy.interpolate import interp1d

import geometry

MUON_MASS = 105. #MeV

"Distribuzione in theta dei muoni: va come cos^2"
def dist_theta(theta):
    return (1/numpy.pi) * (numpy.cos(theta))**2

""" Genero muoni nell'angolo solido"""
def muon_angle_generator(N_events, pdf): 
  
  #theta_muon_1= numpy.random.uniform(-numpy.pi/2, -0.5*numpy.pi+0.1, int(N_events/2) ) 
  #theta_muon_2= numpy.random.uniform(numpy.pi*0.5-0.1, numpy.pi*0.5, int(N_events/2) )
  #theta_muon = numpy.concatenate((theta_muon_1, theta_muon_2))
      
  theta = numpy.linspace(-numpy.pi, +numpy.pi, 200) 
  cdf_y  = []
  for i in range(len(theta)):
    y, rest = quad(pdf, theta[0], theta[i])  
    cdf_y.append(y)       
  cdf_y, unique_indices = numpy.unique(cdf_y, return_index=True) 
  theta = theta[unique_indices] 
  funzione = interp1d(cdf_y, theta)       

  x = numpy.random.uniform(0., 1., N_events)
  theta_muon = funzione(x)
  
  phi_muon = numpy.random.uniform(0, 2 * numpy.pi, N_events )   
   
  return theta_muon, phi_muon


""" Spettro piatto; energie tra 106 e 1000 MeV. Poi bisognerà cambiare e mettere lo spettro vero e proprio"""
def muon_energy_generator( N_events ): 
  E_muon = numpy.random.uniform(305., 10000, N_events) 
  P_muon = numpy.sqrt( E_muon**2 - MUON_MASS **2)
  beta_muon = P_muon / E_muon    
  return E_muon, P_muon, beta_muon

  
"""Posizione sullo scintillatore 3: distribuzione uniforme"""  
def position_on_S3_generator( N_events, x): 
  x_s3 = numpy.random.uniform( (x -geometry.X3/2), (x + geometry.X3/2), N_events)
  y_s3 = numpy.random.uniform(-geometry.Y3+geometry.Y1/2, +geometry.Y1/2, N_events)
  return x_s3, y_s3  
  

"""Calcola la posizione sul piano dello scintillatore 1 partendo dallo scintillatore 3 quando questo sta sopra l'1"""
def propagation_from_S3_to_S1(x_s3, y_s3, theta_muon, phi_muon):
  z = (geometry.Z1/2 + geometry.Z3/2 )
  x_s1 = x_s3 + numpy.cos(phi_muon) * numpy.tan(theta_muon) * z
  y_s1 = y_s3 + numpy.sin(phi_muon) * numpy.tan(theta_muon) * z     
  mask = ((x_s1 > 0.) * (x_s1 < geometry.X1) * (y_s1 < geometry.Y1/2) * (y_s1 > -geometry.X1/2))
  return x_s1, y_s1, mask 



"""Posizione sullo scintillatore 1: x va da 0 ad L e y va da -l/2 a l/2"""
def position_on_S1_generator( N_events ): 
  x_s1 = numpy.random.uniform(0., geometry.X1, N_events)
  y_s1 = numpy.random.uniform(-geometry.Y1/2, +geometry.Y1/2, N_events)
  return x_s1, y_s1
  


"""Calcola la posizione sul piano dello scintillatore 3 partendo dallo scintillatore 1 quando il 3 sta sotto"""  
#ATTENZIONE: NON È BEN FISSATA LA POSIZIONE DELLO SCINTILLATORE 3 QUANDO STA SOTTO
def propagation_from_S1_to_S3(x_s1, y_s1, theta_muon, phi_muon):
  z = geometry.Z1/2 + geometry.Z3/2 + geometry.h_13 
  x_s3 = x_s1 + numpy.cos(phi_muon) * numpy.tan(theta_muon) * z 
  y_s3 = y_s1 + numpy.sin(phi_muon) * numpy.tan(theta_muon) * z 
  mask = ((x_s3 > (geometry.X1-geometry.X3)*0.5) * (x_s3 < (geometry.X1+geometry.X3)*0.5) * (y_s3<geometry.Y3/2) * (y_s3>-geometry.Y3/2))  
  return x_s3, y_s3, mask, z
  




  

