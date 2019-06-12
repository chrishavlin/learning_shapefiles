"""
colorado_plateau.py

reads the shapefile from Fenneman and Johnson (1946), pulls out Colorado Plateau
boundaries and generates a single shape for the full physiographic boundary
of the Colorado Plateau.

To use,

1. download the shapefile from https://water.usgs.gov/GIS/dsdl/physio_shp.zip
unpack the .zip and rename the folder from physio_shp to physio

2. run from the command line

python colorado_plateau.py /path/to/physio/physio.shp /folder/for/output/

first argument is the path to the downloaded shapefile
second argument is an optional argument for the folder to write the processed
data to (will not write if argument not given)
Output:

Creates some matplotlib plots, saves processed data to /folder/for/output/

Full Data Reference: Fenneman, N. M., & Johnson, D. W. (1946). Physiographic
divisions of the conterminous U.S. Reston, VA: US Geological Survey,
Physiographic Committee Special Map.

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

"""

import shapefile, os,sys
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.ops import cascaded_union

# read the arguments
fname=sys.argv[1] # path to physio.shp
outfolder=None
if len(sys.argv)>2:
    outfolder=sys.argv[2] # folder to store output

# read the shapefile
sf = shapefile.Reader(fname)

# find the record indeces for colorado plateau (province ID = 21)
i_rec=0
recs_to_plot=[]
for rec in sf.records():
     if rec[-1]==21:
        print(rec)
        print(i_rec)
        recs_to_plot.append(i_rec)
     i_rec=i_rec+1


# plot the individual records
plt.subplot(1,2,1)
for rec in recs_to_plot:
    pts=sf.shapes()[rec].points
    for lon,lat in pts:
        plt.plot(lon,lat,'.k')

# create a single shape for Colorado Plateau from union of sub-shapes
polies=[]
for rec in recs_to_plot:
    polies.append(Polygon(sf.shapes()[rec].points))
CP_bound=cascaded_union(polies)

# plot the exterior shape
lon,lat = CP_bound.exterior.xy
plt.subplot(1,2,2)
plt.plot(lon,lat,'.k')

# export the final shape as a CSV of boundary points
if outfolder is not None:
    f=open(os.path.join(outfolder,'ColoradoPlateauBoundary.csv'),'w')
    f.write("lon,lat\n")
    for i,j in zip(lon,lat):
        f.write(str(i)+","+str(j)+"\n")
    f.close()

plt.show()
