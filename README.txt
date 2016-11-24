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

DESCRIPTION

   This is a collection of scripts for learning to work with shapefiles in python, 
   assumining no previous knowledge (of either shapefiles or the python libraries 
   used in manipulating them). 

   Uses U.S. state boundary shapefile from census.gov as the sample shapefile: 
        https://www.census.gov/geo/maps-data/data/cbf/cbf_state.html
   The 20m shapefile (cb_2015_us_state_20m.zip) is the easiest to start with. 
   Shapefile not included in package.

   shape_testing/src/ includes a number of python scripts, tested with python 2.7:

        basic_read_and_plot.py -- simplest possible script, just reads and plots a 
                                  shapefile in various ways. 

   The documentation for pyshp is very useful: 
       https://pypi.python.org/pypi/pyshp

REQUIRED PYTHON LIBRARIES

   general libraries: numpy, matplotlib
   for reading shapefiles: pyshp
   for scripts with polygons: shapely, descartes

QUICK START
   1. Download and unzip a shapefile from:
      https://www.census.gov/geo/maps-data/data/cbf/cbf_state.html
      other shapefiles will work, but you'll have to change the  plot axes limits 
      appropriately for your shapefile
   2. edit dat_dir and shp_file_base in the scripts to reflect the directory 
      and shapefile name. 
   3. run basic_read_plot.py from a terminal window: 
           $ cd /path/to/learning_shapefiles/src/
           $ python basic_read_plot.py
CONTENTS
   scripts in src/ include: 

   basic_read_plot.py
         reads a shapefile, plots outlines of geometry 
   basic_readshp_plotpoly.py 
         reads a shapefile, plots geometry using polygons
   simple_polygons.py
         plots several simple polygons
