# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
#from scipy import signal
import matplotlib.pyplot as plot

#1 
E = 4 # amplitude
T=6 # période
f = 1/T # fréquence
t= np.linspace(0,20,100) # vecteur de temps
# création de la fonction de signal u(t)
def signal(t):
    return  E * np.cos((2*np.pi*t)/T)

plot.plot(t,signal(t)) # tracer de la fonction u en fonction du temps

#2
plot.plot(t,E*np.sign(signal(t))) # tracer du signal carré

#3

