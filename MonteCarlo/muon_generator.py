import numpy
import matplotlib.pyplot as plt

import geometry

MUON_MASS = 105. #MeV

""" Spettro piatto; energie tra 106 e 1000 MeV. Poi bisognerà cambiare e mettere lo spettro vero e proprio"""

def muon_energy_generator( N_events ): 
  E_muon = numpy.random.uniform(106., 1000, N_events) 
  P_muon = numpy.sqrt( E_muon**2 - MUON_MASS **2)
  beta_muon = P_muon / E_muon  
  return E_muon, P_muon, beta_muon



""" Spettro piatto in cos(theta) e in phi"""

def muon_theta_generator( N_events ): 
  cos_theta = numpy.random.uniform(-1., +1., N_events) 
  theta_muon = numpy.arccos(cos_theta)
  
  plt.figure(1)
  plt.hist(cos_theta)
  return theta_muon

def muon_phi_generator( N_events ): 
  phi_muon = numpy.random.uniform(0, 2 * numpy.pi, N_events ) 
  
  plt.figure(2)
  plt.hist(phi_muon)
  return phi_muon

"""Posizione sul primo scintillatore: x va da 0 ad L e y va da -l/2 a l/2"""

def position_generator( N_events ): 
  x_s1 = numpy.random.uniform(0., geometry.L1, N_events)
  y_s1 = numpy.random.uniform(-geometry.l1/2, +geometry.l1/2, N_events)
  
  plt.figure(3)
  plt.hist(x_s1)
  plt.figure(4)
  plt.hist(y_s1)
  return x_s1, y_s1


def position_on_scint3(x_s1, y_s1, theta_muon, phi_muon):
  z = geometry.h_12 + geometry.l1/2 + geometry.l2/2
  x_s2 = x_s1 + numpy.cos(phi_muon) * numpy.tan(theta_muon) * z
  y_s2 = y_s1 + numpy.sin(phi_muon) * numpy.tan(theta_muon) * z 
  
  plt.figure(4)
  plt.hist(x_s2)
  plt.figure(5)
  plt.hist(y_s2)
    
  return x_s2, y_s2




