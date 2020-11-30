#!/usr/bin/python3

#------------- imports ---------------#
#import packages
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants

#import animation package
from matplotlib.animation import FuncAnimation

#import slider package
from matplotlib.widgets import Slider
#------------ end imports ------------#

pi = constants.pi
Ns = 4
Nb = 4
freq = (5.8)*(10**9)
c = constants.c
wavelength = c/freq
ds = wavelength/2
db = ds*Ns
k = (2*pi)/wavelength

#Finds larger beam generate from butler matrix
def sub_beam(phase_diff, angle):
    beta_subarray = phase_diff
    psi_subarray = k*ds*(np.cos(angle)) + beta_subarray*(pi/180)
    AF_subarray = ((np.sin((Ns/2)*psi_subarray))/(np.sin(psi_subarray/2)))/Ns
    return abs(AF_subarray)**2

def array_beam(phase_diff, angle):
    beta_array = phase_diff
    psi_array = k*db*(np.cos(angle)) + beta_array*(pi/180)
    AF_array = ((np.sin((Nb/2)*psi_array))/(np.sin(psi_array/2)))/Nb
    return abs(AF_array)**2

#Update values
def update(val):
    beta_subarray = s_beta_subarray.val
    beta_array = s_beta_array.val
    f_d.set_data(theta, sub_beam(beta_subarray, theta_rad))     #Updates the plot of the large beam from AF_subarray
    f_d2.set_data(theta, array_beam(beta_array, theta_360_rad)) #Updates the plot of the small beam from AF_array
    #Updates the plot of the total sum beam formation from AF_total
    f_d3.set_data(theta, sub_beam(beta_subarray, theta_rad) * array_beam(beta_array, theta_360_rad))
    fig.canvas.draw_idle()

#Create figure and add axes
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(311)
ax.set_ylim([0,1])
ax2 = fig.add_subplot(312)
ax2.set_ylim([0,1])
ax3 = fig.add_subplot(313)
ax3.set_ylim([0,1])
fig.subplots_adjust(bottom=0.2, top=0.75)

#Create axes for beta_subarray slider
ax_beta_subarray = fig.add_axes([0.3, 0.9, 0.4, 0.05])
ax_beta_subarray.spines['top'].set_visible(True)
ax_beta_subarray.spines['right'].set_visible(True)

#Create axes for beta_array slider
ax2_beta_array = fig.add_axes([0.3, 0.8, 0.4, 0.05])
ax2_beta_array.spines['top'].set_visible(True)
ax2_beta_array.spines['right'].set_visible(True)

#theta values
theta = np.arange(0,180,0.1)
theta_rad = [val*(pi/180) for val in theta]
theta_360 = np.arange(0,360,0.1)
theta_360_rad = [val*(pi/180) for val in theta]

#Create slider
s_beta_subarray = Slider(ax=ax_beta_subarray, label='Beta Subarray', valmin=-135, valmax=135, valinit=-135, valfmt='%i deg', valstep=90, facecolor='#cc7000')
s_beta_array = Slider(ax=ax2_beta_array, label='Beta Array', valmin=0, valmax=360, valinit=0, valfmt='%i deg', valstep=10, facecolor='#cc7000')

#Plot default data
beta_subarray0 = -135
beta_array0 = 0
f_d, = ax.plot(theta, sub_beam(beta_subarray0, theta_rad), linewidth=2.5)   #Plots large beam from AF_subarray
f_d2, = ax2.plot(theta, array_beam(beta_array0, theta_360_rad), linewidth=2.5)  #Plots smaller beam from AF_array
#Plots total beam summation from AF_total
f_d3, = ax3.plot(theta, sub_beam(beta_subarray0, theta_rad) * array_beam(beta_array0, theta_360_rad), linewidth=2.5)

#Call the function to update values
s_beta_subarray.on_changed(update)
s_beta_array.on_changed(update)

#Display the plot
plt.show()
