'''
affine_expansion.py

expansion/scaling of a shape using shapely

python affine_expansion.py -f ../data/expansion_test_data.csv -exp 0.25,.5,.75,1
.25,1.5,1.75,2

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
from shapely import geometry as geo
from shapely import affinity as aff
import numpy as np
import pandas as pd
import sys,os,argparse
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch

def expandShape(geom_in,scalefactor,frac_or_dist='frac'):

    if frac_or_dist=='dist_km':
        km_per_deg=110. # rough translation from km to degrees
        scalefactor=scalefactor / km_per_deg
    if frac_or_dist in ['dist_km','dist_deg']:
        # calculate the scaling factor as a fractional change from centroid
        dist=scalefactor
        bnds=geom_in.bounds
        dX=bnds[2]-bnds[0]
        dXnew=dX+2.*dist
        fac=dXnew / dX
    else:
        # factor is already a fractional change
        fac=scalefactor

    geom_scaled=aff.scale(geom_in, xfact=fac, yfact=fac)

    return geom_scaled

def loadCSVcoords(filename,latcol='lat',loncol='lon'):
    '''
    loads coordinates from filename, pulls lat/lon from file, returns shape
    '''
    df=pd.read_csv(filename)
    poly = geo.Polygon([[p[0], p[1]] for p in zip(df[loncol],df[latcol])])
    return poly


def plotExpansion(geom_list):
    fig=plt.figure()
    ax=plt.gca()
    scales=geom_list.keys()
    scales.sort()

    lat_rng={'max':-180,'min':180}
    lon_rng={'max':-360,'min':360}
    for sc in scales:
        geom=geom_list[sc]
        patch = PolygonPatch(geom, alpha=0.2)
        ax.add_patch(patch)
        outer=geom.exterior.coords[:]
        for pt in outer:
            lon_rng['max']=np.max([lon_rng['max'],pt[0]])
            lon_rng['min']=np.min([lon_rng['min'],pt[0]])
            lat_rng['max']=np.max([lat_rng['max'],pt[1]])
            lat_rng['min']=np.min([lat_rng['min'],pt[1]])

    ax.set_xlim(lon_rng['min'],lon_rng['max'])
    ax.set_ylim(lat_rng['min'],lat_rng['max'])
    plt.show()

    return

def loadExpandPlot(fname,factors,expansion_units,latlon):
    geom=loadCSVcoords(fname,latlon['lat'],latlon['lon']) # loads into shape

    # expand by each factor
    scaled_geoms={}
    for fac in factors:
        scaled_geoms[fac]=expandShape(geom,fac,expansion_units)

    unscaled=1
    if expansion_units in ['dist_km','dist_deg']:
        unscaled=0
    if unscaled not in factors:
        scaled_geoms[unscaled]=geom

    plotExpansion(scaled_geoms)

    return

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-f','--coord_file', help='CSV file of coordinates',
                        required=True)
    required.add_argument('-exp','--exp_factors', help=('comma separated list '
                        'of exapansion scaling factors to run'),required=True)
    hlpstr=("expansion factor units: 'frac' or 'dist_km' or 'dist_deg'. If 'frac', will expand "
        "bounding box by the given fraction. If 'dist' km or deg, will calculate 'frac' "
        "such that each point moves by given distance (roughly)")
    optional.add_argument('--exp_units', help=hlpstr,default='percent')
    optional.add_argument('--latcol', help=("latitude (or y) column in csv "
                        "(default 'lat')"),default='lat')
    optional.add_argument('--loncol',help=("longitude (or x) column in csv "
                        "(default 'lon')"),default='lon')
    args = vars(parser.parse_args())
    args['exp_factors']=args['exp_factors'].split(',')
    args['exp_factors']=[float(fac) for fac in args['exp_factors']]
    latlon={'lat':args['latcol'],'lon':args['loncol']}
    loadExpandPlot(args['coord_file'],args['exp_factors'],args['exp_units'],latlon)
