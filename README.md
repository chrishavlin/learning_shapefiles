**Copyright (C) 2019 Chris Havlin, <https://chrishavlin.com>**

  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

**DESCRIPTION**

This is a collection of scripts for learning to work with shapefiles in python, assuming no previous knowledge (of either shapefiles or the python libraries used in manipulating them).

`src/` includes a number of python scripts, tested with python

The documentation for pyshp is very useful: https://pypi.python.org/pypi/pyshp

**REQUIREMENTS**

  * python (2.xx or 3.xx should work)
  * general libraries: numpy, matplotlib, pandas
  * for reading shapefiles: pyshp
  * for scripts with polygons: shapely, descartes

`colorado_plateau.py` uses a shapefile from  Fenneman and Johnson (1946): see comments for where to download it.

**CONTENTS**

scripts in `src/` include:
  * **basic_read_plot.py**: reads a shapefile, plots outlines of geometry
  * **basic_readshp_plotpoly.py**: reads a shapefile, plots geometry using polygons
  * **simple_polygons.py**: plots several simple polygons
  * **read_shp_and_rcrd.py**: reads a shapefile, plots geometry using polygons colored by record values. The record indexing is specific to the census.gov State Boundaries shapefile.
  * **colorado_plateau.py**: reads the shapefile from Fenneman and Johnson (1946), pulls out Colorado Plateau shapes and generates a single shape for the full physiographic boundary of the Colorado Plateau.
  * **affine_expansion.py**: reads a CSV of lat/lon coords for a polygon and scales the shape by specified amounts.
