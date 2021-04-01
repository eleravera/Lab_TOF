import sys
sys.path.insert(1, '/home/testaovo/Scrivania/LABORATORIO/TOF/Lab_TOF')


import numpy
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.integrate import quad
from scipy.interpolate import interp1d

import geometry

MUON_MASS = 105. #MeV

#Distribuzione dei muoni in theta
def dist_theta(theta):
  return (numpy.cos(theta))**2

#Spettro in energia dei raggi cosmici
def distr_energy(E): 
  return 1. / (E)**2.7   


""" Genero muoni nell'angolo solido"""
def muon_angle_generator(N_events, pdf):      
  theta = numpy.linspace(-numpy.pi/2, numpy.pi/2, 200) 
  cdf_y  = []
  for i in range(len(theta)):
    y, rest = quad(pdf, theta[0], theta[i])  
    cdf_y.append(y)
  cdf_y, unique_indices = numpy.unique(cdf_y, return_index=True)
  cdf_y /= cdf_y[-1]
  theta = theta[unique_indices] 
  funzione = interp1d(cdf_y, theta)       

  x = numpy.random.uniform(0., 1., N_events)
  theta_muon = funzione(x)
  
  phi_muon = numpy.random.uniform(0, 2 * numpy.pi, N_events )   
  return theta_muon, phi_muon


""" Spettro piatto; energie tra 106 e 1000 MeV. Poi bisognerà cambiare e mettere lo spettro vero e proprio"""
def muon_energy_generator(N_events, pdf, xmin, xmax): 
  e = numpy.linspace(xmin, xmax, 1000)  
  cdf_y  = numpy.full(len(e), 0.)
  for i in range(len(e)):
    y, rest = quad(pdf, e[0], e[i])
    cdf_y[i] = y       
  cdf_y, unique_indices = numpy.unique(cdf_y, return_index=True)
  cdf_y = cdf_y/cdf_y[-1]
  e = e[unique_indices]  
  ppf_spline = interp1d(cdf_y, e)         
  x = numpy.random.uniform(0., 1., N_events)
  E_kin = ppf_spline(x)  
  E_muon = E_kin + MUON_MASS
  P_muon = numpy.sqrt( E_muon**2 - MUON_MASS **2)
  beta_muon = P_muon / E_muon
  return E_muon, P_muon, beta_muon

  
"""Posizione sullo scintillatore 3: distribuzione uniforme"""  
def position_on_S3_generator( N_events, x): 
  x_s3 = numpy.random.uniform( (x -geometry.X3/2), (x + geometry.X3/2), N_events)
  y_s3 = numpy.random.uniform(-geometry.Y1/2, geometry.Y3-geometry.Y1/2, N_events)
  return x_s3, y_s3  
  

"""Calcola la posizione sul piano dello scintillatore 1 partendo dallo scintillatore 3 quando questo sta sopra l'1"""
def propagation_from_S3_to_S1(x_s3, y_s3, theta_muon, phi_muon):
  z = (geometry.Z1 + geometry.Z3 ) * 0.5
  x_s1 = x_s3 + numpy.cos(phi_muon) * numpy.tan(theta_muon) * z
  y_s1 = y_s3 + numpy.sin(phi_muon) * numpy.tan(theta_muon) * z     
  mask = ((x_s1 > 0.) * (x_s1 < geometry.X1) * (y_s1 < geometry.Y1/2) * (y_s1 > -geometry.Y1/2))
  return x_s1, y_s1, mask 



"""Posizione sullo scintillatore 1: x va da 0 ad L e y va da -l/2 a l/2"""
def position_on_S1_generator( N_events ): 
  x_s1 = numpy.random.uniform(0., geometry.X1, N_events)
  y_s1 = numpy.random.uniform(-geometry.Y1/2, +geometry.Y1/2, N_events)
  return x_s1, y_s1
  


"""Calcola la posizione sul piano dello scintillatore 3 partendo dallo scintillatore 1 quando il 3 sta sotto"""  
def propagation_from_S1_to_S3(x_s1, y_s1, theta_muon, phi_muon):
  z = geometry.Z1/2 + geometry.Z3/2 + geometry.h_13 
  x_s3 = x_s1 + numpy.cos(phi_muon) * numpy.tan(theta_muon) * z 
  y_s3 = y_s1 + numpy.sin(phi_muon) * numpy.tan(theta_muon) * z 

  mask_x = (x_s3 > (geometry.s3 - 0.5 * geometry.X3)) * (x_s3 < (geometry.s3 + geometry.X3 * 0.5 )) 
  mask_y =  (y_s3 < (geometry.s3_y + geometry.Y3 )) * (y_s3 > geometry.s3_y ) 
  mask = mask_x * mask_y
  return x_s3, y_s3, mask, z
  
  
  
def resolution(N, pdf, *args ):
  dt = numpy.linspace(-5., 5., 1000)
  cdf_y  = numpy.zeros(N)
  for i in range(len(dt)):
    y, rest = quad(pdf, dt[0], dt[i], args = args)  
    cdf_y[i] = y 
  cdf_y, unique_indices = numpy.unique(cdf_y, return_index=True)
  cdf_y /= cdf_y[-1]
  dt = dt[unique_indices] 
  funzione = interp1d(cdf_y, dt)
  x = numpy.random.uniform(0., 1., N)
  res = funzione(x)
  return res   
  
