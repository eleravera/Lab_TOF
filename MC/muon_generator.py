
from const import costants
import numpy
import matplotlib.pyplot as plt


" Spettro piatto; energie tra 10 e 1000 MeV. Poi bisognerà cambiare e mettere lo spettro vero e proprio"

def muon_energy_generator( N_events ): 
  E_muon = numpy.random.uniform(10., 1000, N_events) 
  return E_muon


" Spettro piatto in cos(theta) e in phi"

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

"Posizione sul primo scintillatore: x va da 0 ad L e y va da -l/2 a l/2"

def position_generator( N_events ): 
  x = numpy.random.uniform(0., costants.L, N_events)
  y = numpy.random.uniform(-costants.l/2, +costants.l/2, N_events)
  
  plt.figure(3)
  plt.hist(x)
  plt.figure(4)
  plt.hist(y)
  return x, y

