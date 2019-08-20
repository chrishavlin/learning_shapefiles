'''
countourf_to_shp.py

an example for converting the results of a matplotlib contourf plot to a
shapefile, preserving contour level data

to run:

python contourf_to_shp

outputs data in data/shaped_contour, plots a figure

Copyright (C) 2019  Chris Havlin, <https://chrishavlin.wordpress.com>
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

'''

from shapely import geometry
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import fiona
import os,json
from descartes.patch import PolygonPatch

# create some test data with multiple peaks
lon = np.linspace(0,45,100)
lat = np.linspace(-20,32,90)
long,latg=np.meshgrid(lon,lat)
C1=np.sqrt((long-5.)**2+(latg-25)**2)/30.
C2=np.sqrt((long-30.)**2+(latg-1)**2)/10.
m = 30*np.exp(-C1**2)+20.*np.exp(-C2**2)

# make the contourf plot, storing the resulting ContourSet in cs
plt.figure(figsize=[10,5])
plt.subplot(1,2,1)
Nlevels=10
cs = plt.contourf(lon,lat,m,Nlevels,cmap='gist_heat')
plt.title('contourf figure with Nlevels='+str(Nlevels))

# create lookup table for levels
lvl_lookup = dict(zip(cs.collections, cs.levels))

# loop over collections (and polygons in each collection), store in list for fiona
PolyList=[]
for col in cs.collections:
    z=lvl_lookup[col] # the value of this level
    for contour_path in col.get_paths():
        # create the polygon for this level
        for ncp,cp in enumerate(contour_path.to_polygons()):
            lons = cp[:,0]
            lats = cp[:,1]
            new_shape = geometry.Polygon([(i[0], i[1]) for i in zip(lons,lats)])            
            if ncp == 0:
                poly = new_shape # first shape
            else:
                poly = poly.difference(new_shape) # Remove the holes
        PolyList.append({'poly':poly,'props':{'z': z}})

## write the fiona collection

# clean up directories
outname=os.path.join('..','data','shaped_contour')
if os.path.isdir(outname):
    for file in os.listdir(outname):
        os.remove(os.path.join(outname,file))
    os.rmdir(outname)
os.mkdir(outname)

# define ESRI schema, write each polygon to the file
outfi=os.path.join(outname,'shaped_contour.shp')
schema = {'geometry': 'Polygon','properties': {'z': 'float'}}
with fiona.collection(outfi, "w", "ESRI Shapefile", schema) as output:
    for p in PolyList:
        output.write({'properties': p['props'],
            'geometry': geometry.mapping(p['poly'])})

# save the levels and global min/max as a separate json for convenience
Lvls={'levels':cs.levels.tolist(),'min':m.min(),'max':m.max()}
with open(os.path.join(outname,'levels.json'), 'w') as fp:
    json.dump(Lvls, fp)

## Plotting the results: reads data back in, plots the polygons with data only
## from shapefile and levels.txt

ax=plt.subplot(1,2,2)

# read in levels, define colormap
with open(os.path.join(outname,'levels.json')) as jfile:
    Lvls=json.load(jfile)
levels=np.array(Lvls['levels'])
cmap=plt.cm.gist_heat
lv_range=[Lvls['min'],Lvls['max']]

# loop over each shape, pull out level value ('z'), plot a polygon with a color
# matching the colormap.
ishp=0
with fiona.open(outfi) as shape:
    for shp in shape:

        # pull this shape's level and set the color from the map
        lv=shp['properties']['z'] # this shape's level
        clr=cmap((lv - lv_range[0])/(lv_range[1]-lv_range[0]))

        # build the polygon and add the patch
        coords=shp['geometry']['coordinates'][0] # coords of this polygon
        poly=geometry.Polygon(coords)
        patch = PolygonPatch(poly, facecolor=clr, edgecolor=clr)
        ax.add_patch(patch)

        # track max/min coordinate values
        bnds=poly.bounds
        rng_C={'lon':{'min':bnds[0],'max':bnds[2]},
               'lat':{'min':bnds[1],'max':bnds[3]}}
        if ishp==0:
            rngs=rng_C
        else:
            for ll in ['lon','lat']:
                rngs[ll]['max']=max([rngs[ll]['max'],rng_C[ll]['max']])
                rngs[ll]['min']=min([rngs[ll]['min'],rng_C[ll]['min']])
        ishp=ishp+1

ax.set_xlim([rngs['lon']['min'],rngs['lon']['max']])
ax.set_ylim([rngs['lat']['min'],rngs['lat']['max']])
plt.title('polygon patches from shapefile')

plt.show()
