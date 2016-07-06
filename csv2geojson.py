#!/usr/bin/env python

import pandas as pd
import geopandas as gpd
import sys
import fiona.crs
from shapely.geometry import Point

if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    print 'error. usage: python csv2json.py <file>'
    sys.exit()

df = pd.read_csv(sys.argv[1], sep=';', encoding = "ISO-8859-1")

# correct error on Y files
df = df[pd.notnull(df['Y'])]

# # Convert to shapely Points and to a GeoDataFrame with epsg 2950
geoms = df.apply(lambda row: Point(row['X'], row['Y']), axis=1)

# remove fields X and Y, now useless
df = df.drop(['X','Y'], 1)
gdf = gpd.GeoDataFrame(df, geometry=geoms, crs=fiona.crs.from_epsg(2950))

# # Convert to lon/lat
gdf.to_crs(epsg=4326, inplace=True)

# # output GeoJSON
print gdf.to_json(indent=2, separators=(',', ': '), encoding = "utf-8")
