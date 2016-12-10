"""
denver_stack.py

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
from shapely.geometry import LineString
from descartes.patch import PolygonPatch

"""
 IMPORT THE SHAPEFILE 
"""
#shp_file_base='denver_tree_canopy_2013'
#dat_dir='../shapefiles/'+shp_file_base +'/'
#sf = shapefile.Reader(dat_dir+shp_file_base)

shp_file_base='ex_QMDJXT8DzmqNh6eFiNkAuESyDNCX_osm_line'
dat_dir='../shapefiles/denver_maps/grouped_by_geometry_type/'
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
fld_name='TREE_PCT'
map_geoms=['highway']#,'highway','bridge','tunnel']

plot_these_rec_vals=list()
#plot_these_rec_vals.append('motorway')
plot_these_rec_vals.append('motorway_link')
#plot_these_rec_vals.append('primary')
#plot_these_rec_vals.append('secondary')

# loop over records, track global min/max

# exclude shapes outside bounds:

# for downtown zoom:
ymin=39.65
ymax=39.79
xmin=-105.05
xmax=-104.9

# wider view:
ymin=39.
ymax=40.2
xmin=-105.45
xmax=-104.4

""" PLOTS ALL SHAPES AND PARTS """
plt.figure()
ax = plt.axes() # add the axes
ax.set_aspect('equal')

shape_id = 0
nshapes=len(sf.shapes())
rec_vals=list()
for shapeRec in sf.iterShapeRecords():
    # pull out shape geometry and records
    shape_id = shape_id+1
    print shape_id, 'of', nshapes, '(', int(float(shape_id)/float(nshapes)*1000)/10,'%)'
    shape=shapeRec.shape 
    rec = shapeRec.record 

    # select polygon facecolor RGB vals based on record value
    R = 0.1
    G = 0.1
    B = 0.1

    nparts = 0
    for mapg in map_geoms:
        if rec[field_names.index(mapg)] not in rec_vals:
           print rec[field_names.index(mapg)]
           rec_vals.append(rec[field_names.index(mapg)])

        if rec[field_names.index(mapg)] in plot_these_rec_vals:
            nparts = len(shape.parts) # total parts

    if nparts == 1:
        Line = LineString(shape.points)
        x,y = Line.xy
        ax.plot(x, y, color=[R,G,B], zorder=1)

    elif nparts > 0 : # loop over parts of each shape, plot separately
        for ip in range(nparts): # loop over parts, plot separately
            i0=shape.parts[ip]
            if ip < nparts-1:
               i1 = shape.parts[ip+1]-1
            else:
               i1 = len(shape.points)

            # build the polygon and add it to plot   
            Line = LineString(shape.points[i0:i1+1])
            x,y = Line.xy
            ax.plot(x, y, color=[R,G,B],zorder=1)

print 'record field names:',field_names
print 'possible record values for ',map_geoms,':',rec_vals

"""
 IMPORT THE SHAPEFILE 
"""
shp_file_base='denver_tree_canopy_2013'
dat_dir='../shapefiles/'+shp_file_base +'/'
sf = shapefile.Reader(dat_dir+shp_file_base)

"""    Find max/min of record of interest (for scaling the facecolor)"""

# get list of field names, pull out appropriate index
fld = sf.fields[1:]
field_names = [field[0] for field in fld]
print 'record field names:',field_names
fld_name='TREE_PCT'
ndx1=field_names.index(fld_name)

# loop over records, track global min/max
# exclude shapes outside bounds:
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

print 'min:',minrec,'max:',maxrec

""" PLOTS ALL SHAPES AND PARTS """
for shapeRec in sf.iterShapeRecords():
    # pull out shape geometry and records
    shape=shapeRec.shape 
    rec = shapeRec.record 

    # select polygon facecolor RGB vals based on record value
    R = 0.
    G = 0.1+0.9*(rec[ndx1]-minrec)/(maxrec-minrec)
    G = G * (G < 1.0) * (G > 0) + 1.0 * (G>1.0)
    G = G * (G >= 0.1) + 0.1 * (G < 0.1)
    B = 0.

    alf = 0.9

    # check number of parts (could use MultiPolygon class of shapely?)
    nparts = len(shape.parts) # total parts
    if nparts == 1:
        polygon = Polygon(shape.points)
        patch = PolygonPatch(polygon, facecolor=[R,G,B], edgecolor=[R,G,B], alpha=alf, zorder=2)
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
            patch = PolygonPatch(polygon, facecolor=[R,G,B], edgecolor=[R,G,B],alpha=alf, zorder=2) 
            ax.add_patch(patch)
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
plt.show()

