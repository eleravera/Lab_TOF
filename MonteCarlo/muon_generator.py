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

def muon_angle_generator( N_events ): 
  cos_theta = numpy.random.uniform(-1., +1., N_events) 
  theta_muon = numpy.arccos(cos_theta)
  phi_muon = numpy.random.uniform(0, 2 * numpy.pi, N_events )   
  
  plt.figure("Theta e phi")
  plt.subplot(2, 1, 1)
  plt.hist(cos_theta)
  plt.xlabel("cos(theta)")
  
  plt.subplot(2, 1, 2)
  plt.hist(phi_muon)
  plt.xlabel("phi")
  
  return theta_muon, phi_muon


"""Posizione sul primo scintillatore: x va da 0 ad L e y va da -l/2 a l/2"""

def position_generator( N_events ): 
  x_s1 = numpy.random.uniform(0., geometry.L1, N_events)
  y_s1 = numpy.random.uniform(-geometry.l1/2, +geometry.l1/2, N_events)
  
  plt.figure("Muon position on scintillator 1 ")
  plt.subplot(2, 1, 1)
  plt.hist(x_s1)
  plt.xlabel("x_s1 [m]")  
    
  plt.subplot(2, 1, 2)
  plt.hist(y_s1 * 10**2)
  plt.xlabel("y_s1 [cm]")  
  
  return x_s1, y_s1

"""Calcola la posizione sul piano dello scintillatore 3"""
def position_on_scint3(x_s1, y_s1, theta_muon, phi_muon):
  z = geometry.h_13 + geometry.l1/2 + geometry.l3/2
  x_s3 = x_s1 + numpy.cos(phi_muon) * numpy.tan(theta_muon) * z
  y_s3 = y_s1 + numpy.sin(phi_muon) * numpy.tan(theta_muon) * z 
  
  mask_x = (x_s3 < (geometry.L1 * 0.5 + geometry.l3 * 0.5)) * (x_s3 > (geometry.L1 * 0.5 - geometry.l3 * 0.5))  
  mask_y = (y_s3 < geometry.l3 * 0.5) * (y_s3 > - geometry.l3 * 0.5)     
  print(len(x_s3[mask_x]), len(x_s3))
  
  plt.figure("Muon position on scintillator 3 ")
  plt.subplot(2, 1, 1)
  plt.hist(x_s3[mask_x])
  plt.xlabel("x_s3 [m]")
  
  plt.subplot(2, 1, 2)
  plt.hist(y_s3[mask_y]* 10**2)
  plt.xlabel("y_s3 [cm]")  
 
  return x_s3, y_s3


"""Propagazione del segnale dentro lo scintillatore """
def DT_12(x_s1): 
  T_r = (geometry.L1 - x_s1) / geometry.v_gamma
  T_l = x_s1 / geometry.v_gamma  
  DT_12 = numpy.abs(T_r - T_l)  
  
  plt.figure("Delta t PM1 and 2")
  plt.hist(DT_12 * 10**9)
  plt.xlabel("DT_12 [ns]")
  
  return DT_12
  
"""def DT_13(x_s1, x_s3): 
  T_1 = x_s1 / geometry.v_gamma  
  T_3 = x_s3 / geometry.v_gamma  

  DT_13 = (T_r - T_l)  + cost
  
  return DT_13"""
    
  
  
  


