"""
denver_household_income.py

reads a shapefile using the shapefile library, loops over imported shapes 
and plots polygons for each shape, colored by record entry

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
import shapefile
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

"""
 IMPORT THE SHAPEFILE 
"""
shp_file_base='american_community_survey_blk_grp_2010_2014'
dat_dir='../shapefiles/'+shp_file_base +'/'
sf = shapefile.Reader(dat_dir+shp_file_base)

print 'number of shapes imported:',len(sf.shapes())


"""
       PLOTTING
"""

"""    Find max/min of record of interest (for scaling the facecolor)"""

# get list of field names, pull out appropriate index
fld = sf.fields[1:]
field_names = [field[0] for field in fld]
print 'record field names:',field_names
fld_name='MED_HH_INC'
ndx1=field_names.index(fld_name)

# loop over records, track global min/max
ymin=39.65
ymax=39.79
xmin=-105.05
xmax=-104.9

maxrec=-9999
minrec=1e21
for shapeRec in sf.iterShapeRecords():
       shape=shapeRec.shape
          
       if shape.bbox[0]>xmin or shape.bbox[2]>xmin:    
          if shape.bbox[0]<xmax:
             if shape.bbox[1]>ymin or shape.bbox[3]>ymin:
                if shape.bbox[1]<ymax:
                   rec=shapeRec.record
                   maxrec=np.max((maxrec,rec[ndx1]))
                   minrec=np.min((minrec,rec[ndx1]))


print fld_name,'min:',minrec,'max:',maxrec

""" PLOTS ALL SHAPES AND PARTS """
plt.figure()
ax = plt.axes() # add the axes
ax.set_aspect('equal')

for shapeRec in sf.iterShapeRecords():
    # pull out shape geometry and records
    shape=shapeRec.shape 
    rec = shapeRec.record 

    # select polygon facecolor RGB vals based on record value
    R = 1.
    G = (rec[ndx1]-minrec)/(maxrec-minrec)
    G = G * (G < 1.0) * (G > 0) + 1.0 * (G>1.0)
    B = 0.

    # check number of parts (could use MultiPolygon class of shapely?)
    nparts = len(shape.parts) # total parts
    if nparts == 1:
        polygon = Polygon(shape.points)
        patch = PolygonPatch(polygon, facecolor=[R,G,B], edgecolor=[0,0,0], alpha=1.0, zorder=2)
        ax.add_patch(patch)

    else: # loop over parts of each shape, plot separately
        for ip in range(nparts): # loop over parts, plot separately
            i0=shape.parts[ip]
            if ip < nparts-1:
               i1 = shape.parts[ip+1]-1
            else:
               i1 = len(shape.points)

            # build the polygon and add it to plot   
            polygon = Polygon(shape.points[i0:i1+1])
            patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)           
            ax.add_patch(patch)
    
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.show()

