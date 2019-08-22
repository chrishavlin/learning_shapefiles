'''
class for loading dem topo files from https://www.ngdc.noaa.gov/mgg/global/global.html
'''
import numpy as np

class etopo(object):

    def __init__(self,filename,loadFile=True):
        self.filename=filename
        self.filetype=filename.split('.')[-1]

        if loadFile:
            if self.filetype=='asc':
                self.loadGriddedAscii()
            else:
                print("filetype "+self.filetype+" not supported")

        return

    def loadGriddedAscii(self):
        ''' loads the gridded etopo file '''

        # load the gridded data
        self.topo=np.loadtxt(self.filename,skiprows=5)

        # load the header
        headervals =[]
        header=['ncols','nrows','lon1','lat1','d_deg']
        with open(self.filename, "r") as f:
            for i in xrange(5):
                line = f.next()
                headervals.append(float(line.split(' ')[-1]))
        header_dict=dict(zip(header,headervals))
        header_dict['lat2']=header_dict['lat1']+header_dict['nrows']*header_dict['d_deg']
        header_dict['lon2']=header_dict['lon1']+header_dict['ncols']*header_dict['d_deg']

        # calculate lat, lon arrays
        self.lats=np.linspace(header_dict['lat2'],header_dict['lat1'],header_dict['nrows'])
        self.lons=np.linspace(header_dict['lon1'],header_dict['lon2'],header_dict['ncols'])
        self.topo_range=header_dict
        return
