"""
inspect_shapefile.py

script that builds up list of record values for shapes. Use for inspecting a shapefile
that didn't come with a description of the fields.

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

"""
 IMPORT THE SHAPEFILE 
"""

class field_description(object):
      def __init__(self,name):
          self.fieldname=name
      
      def get_field_type(self,sf):
          """ self -- the object
              sf -- the shapefile object of interest """

          # pull out the fields
          fld = sf.fields[1:]
          field_names = [field[0] for field in fld]
          nshapes=len(sf.shapes())

          # find the data type of the field
          self.field_type=None
          shapeid=0
          while not self.field_type and shapeid < nshapes-1:
                rec=sf.record(shapeid)[field_names.index(self.fieldname)]
                if rec:
                   self.field_type=type(rec) 
                shapeid += 1
   
      def get_unique_rec_values(self,sf):
          """
          finds unique values of records
          """

          # pull out the fields
          fld = sf.fields[1:]
          field_names = [field[0] for field in fld]
          nshapes=len(sf.shapes())

          self.rec_vals=list()

          shape_id = 0

          print 'Finding unique record values for',self.fieldname
          for rec in sf.iterRecords():
              # pull out shape geometry and records
              shape_id += 1
              pct_comp=float(int(float(shape_id)/float(nshapes)*10000))/100.
              print shape_id, 'of', nshapes, '(', pct_comp,'% )'

              if rec[field_names.index(self.fieldname)] not in self.rec_vals:
                 print "  new record value: rec[field_names.index(self.fieldname)]"
                 self.rec_vals.append(rec[field_names.index(self.fieldname)])
 
if __name__ == '__main__':
   shp_file_base='ex_QMDJXT8DzmqNh6eFiNkAuESyDNCX_osm_line'
   dat_dir='../shapefiles/denver_maps/grouped_by_geometry_type/'
   sf = shapefile.Reader(dat_dir+shp_file_base)

   # pull out the fields
   fld = sf.fields[1:]
   field_names = [field[0] for field in fld]

   field_obj=field_description(field_names[1]) 

   field_obj.get_field_type(sf)

   field_obj.get_unique_rec_values(sf)

   print '---------------------------------------'
   print 'Shapefile has the following field names'
   print field_names
   print 'The field name',field_obj.fieldname,field_obj.field_type
   print 'has',len(field_obj.rec_vals),' possible values:'
   print field_obj.rec_vals

