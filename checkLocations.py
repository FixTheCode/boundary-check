# -----------------------------------------------------------
# check if a coordinate in within the United States
#
# requires shape and dbf file from:
# www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
#
# https://github.com/FixTheCode CC0 1.0 Universal
# -----------------------------------------------------------
import argparse
import csv
import shapefile
from shapely.geometry import Point
from shapely.geometry import shape

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="file containint coordinates")
args = parser.parse_args()

# open the shapefile
shp = shapefile.Reader('us.shp') 
all_shapes = shp.shapes() 
all_records = shp.records()

# open the file of coordinates. we expect lat,long,filename
# we are using this to identify files with coordinates that 
# have a location in the United States.
with open(args.file, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        lat = float(row[0])
        lng = float(row[1])
        file = row[2]

        point_to_check = (lng, lat) # an x,y tuple. long,lat
        for i in range(1,len(all_shapes)):
            boundary = all_shapes[i] # get a boundary polygon
            if Point(point_to_check).within(shape(boundary)): # make a point and see if it's within the polygon
                name = all_records[i][8] # get location name associated with the point
                print ("US location: ", name, " ", lat, ",", lng, " File: ", file) 
       


