"""
simple_polygons.py 

Uses shapely and descartes to plot some simple polygons

Copyright (C) 2016  Chris Havlin, <https://chrishavlin.wordpress.com>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

# choose which shape to plot
shape = 'pacman_rough_eye'
# available shapes:
#       'square'
#       'unit_circle'
#       'pacman'
#       'pacman_rough'
#       'pacman_rough_eye'


# define points of shape
if shape == 'square':
   # square
   ext = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)] # exterior points

elif shape == 'unit_circle':
   # unit circle
   theta = np.linspace(0,2*3.14,50)
   x = np.cos(theta)
   y = np.sin(theta)
   
   # build the list of points
   ext = list()
   
   # loop over x,y, add each point to list
   for itheta in range(len(theta)):
       ext.append((x[itheta],y[itheta]))
   
   ext.append((x[0],y[0]))    
   inter = list()

elif shape == 'pacman':
   # pacman shape!
   theta = np.linspace(0.25*3.14,1.75*3.14,50)
   x = np.cos(theta)
   y = np.sin(theta)
   
   # build the list of points
   ext = list()
   
   # loop over x,y, add each point to list
   for itheta in range(len(theta)):
       ext.append((x[itheta],y[itheta]))
   
   ext.append((0,0))    
   inter = list()

elif shape == 'pacman_rough':
   # pacman shape with random roughness added to bounding points
   theta = np.linspace(0.25*3.14,1.75*3.14,80)

   # add random perturbation
   max_rough=0.05
   pert=max_rough * np.random.rand(len(theta))

   x = np.cos(theta)+pert
   y = np.sin(theta)+pert
   
   # build the list of points
   ext = list()
   
   # loop over x,y, add each point to list
   for itheta in range(len(theta)):
       ext.append((x[itheta],y[itheta]))
   
   ext.append((0,0))    
   inter = list()

elif shape == 'pacman_rough_eye':
   theta = np.linspace(0.25*3.14,1.75*3.14,80)

   # add random perturbation
   max_rough=0.05
   pert=max_rough * np.random.rand(len(theta))

   x = np.cos(theta)+pert
   y = np.sin(theta)+pert
   
   # build the list of points
   ext = list()
   
   # loop over x,y, add each point to list
   for itheta in range(len(theta)):
       ext.append((x[itheta],y[itheta]))
   
   ext.append((0,0))    

   # build eyeball interior points
   theta=np.linspace(0,2*3.14,30)
   x = 0.1*np.cos(theta)+0.2
   y = 0.1*np.sin(theta)+0.7

   inter = list()
   for itheta in range(len(theta)):
       inter.append((x[itheta],y[itheta]))
   inter.append((x[0],y[0]))


if len(inter) == 0: 
   # build the polygon from exterior points
   polygon = Polygon(ext)
else:
   # include interior points
   polygon = Polygon(ext,[inter[::-1]])

# initialize figure and axes
fig = plt.figure()
ax = fig.add_axes((0.1,0.1,0.8,0.8))

# put the patch on the plot
patch = PolygonPatch(polygon, facecolor=[0,0,0.5], edgecolor=[1,1,1], alpha=1.0, zorder=2)
ax.add_patch(patch)

# new axes
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5,1.5])
ax.set_aspect(1)

plt.show()

