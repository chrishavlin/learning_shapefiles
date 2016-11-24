"""
Uses shapely and descartes to plot some simple polygons
"""
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

# initialize figure and axes
fig = plt.figure()
ax = fig.add_axes((0.1,0.1,0.8,0.8))

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
   ext = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)] # exterior points

elif shape == 'unit_circle':
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


if len(inter) == 0: 
    # build the polygon from exterior points
    polygon = Polygon(ext)
else:
    # include interior points?
    polygon = Polygon(ext,[inter])

# put the patch on the plot
patch = PolygonPatch(polygon, facecolor=[0,0,0.5], edgecolor=[1,1,1], alpha=1.0, zorder=2)
ax.add_patch(patch)

# new axes
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5,1.5])
ax.set_aspect(1)

plt.show()

