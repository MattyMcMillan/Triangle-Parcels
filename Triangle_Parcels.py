import geopandas as gpd
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np


CRS = 'PROJCS["NAD_1983_Albers",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG","4269"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["latitude_of_center",23],PARAMETER["longitude_of_center",-96],PARAMETER["standard_parallel_1",29.5],PARAMETER["standard_parallel_2",45.5],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
CRS2 = 'EPSG:2264'

wake_shapes = gpd.read_file(r'filelocation').to_crs(CRS)
orange_shapes = gpd.read_file(r'filelocation').to_crs(CRS)
johnston_shapes = gpd.read_file(r'filelocation').to_crs(CRS)
chatham_shapes = gpd.read_file(r'filelocation').to_crs(CRS)
franklin_shapes = gpd.read_file(r'filelocation').to_crs(CRS)
vance_shapes = gpd.read_file(r'filelocation').to_crs(CRS)


vance_shapes['RECAREANO'] = vance_shapes['GISACRES']

wake_shapes['County'] = 'Wake'
orange_shapes['County'] = 'Orange'
johnston_shapes['County'] = 'Johnston'
chatham_shapes['County'] = 'Chatham'
franklin_shapes['County'] = 'Franklin'
vance_shapes['County'] = 'Vance' 


triangle_shapes = pd.concat([wake_shapes,orange_shapes,johnston_shapes,chatham_shapes,franklin_shapes,vance_shapes])


#ADD COLUMNS
triangle_shapes['Parcel_Area'] = triangle_shapes.geometry.area

#DROP COLUMNS
triangle_shapes = triangle_shapes.drop(['GISACRES','SZIP','STRUCT','SOURCEREF','PARVAL','PARUSEDESC','OWNTYPE','LANDVAL','TRANSFDATE', 'STNAME' , 'PARUSEDSC2' , 'NPARNO' , 'MSTATE' , 
								 'GNISID', 'ALTPARNO', 'CNTYFIPS', 'LEGDECFULL',
								 'MADDPREF', 'MADDRNO', 'MADDSTNAME', 'MADDSTR', 'MADDSTSUF', 'MADDSTTYP', 'MAILADD', 'MAPREF', 'MULTISTRUC', 'MUNIT', 'MCITY', 'MZIP', 'OWNFRST', 
								 'OWNLAST', 'PARUSECD2', 'PARUSECODE', 'PARVALTYPE', 'PRESENTVAL', 'RECAREATX', 'REVDATETX', 'REVISEDATE', 'REVISEYEAR', 'SADDNO', 'SADDPREF', 
								 'SADDSTNAME', 'SADDSTR', 'SADDSTTYP', 'SALEDATETX', 'SCITY', 'SOURCEAGNT', 'SOURCEDATE', 'SOURCEDATX', 'STCNTYFIPS', 'STFIPS', 'STRUCTNO', 'SUBDIVISIO', 
								 'SUBOWNTYPE', 'SUBSURFOWN', 'SUNIT', 'SSTATE', 'STRUCTYEAR', 'SADDSTSUF', 'SALEDATETX', 'SCITY', 'SITEADD', 'SOURCEAGNT',
							     'SOURCEDATE', 'SOURCEDATX', 'SOURCEREF', 'SSTATE', 'STCNTYFIPS',
  								 'SADDNO', 'SADDPREF', 'SADDSTNAME', 'SADDSTR', 'SADDSTSUF', 'SADDSTTYP','PARUSECD2', 'PARUSECODE',
       							 'PARUSEDESC', 'PARUSEDSC2', 'PARVAL', 'PARVALTYPE', 'PRESENTVAL','OWNTYPE','GNISID',
       							 'LANDVAL', 'LEGDECFULL', 'MADDPREF', 'MADDRNO', 'MADDSTNAME', 'MADDSTR',
                                 'MADDSTSUF', 'MADDSTTYP', 'MAILADD', 'MAPREF', 'MCITY', 'MSTATE',
       							 'MULTISTRUC', 'MUNIT', 'MZIP','CNTYNAME','SALEDATE'], axis=1)


#RENAME COLUMN
triangle_shapes = triangle_shapes.rename(columns={'IMPROVVAL':'Building', 'RECAREANO':'Acreage'})

#WETLANDS
merged = gpd.overlay(triangle_shapes, wetlands, how='intersection')
merged['Wetland_Area'] = merged.geometry.area

sum2 = merged.groupby(['PARNO'])['Wetland_Area'].sum().reset_index(name="Wetlands")


triangle_shapes = triangle_shapes.merge(sum2, on='PARNO')
triangle_shapes['Wetlands'] = triangle_shapes['Wetlands'].fillna(0)

triangle_shapes['Wetlands_%'] = ((triangle_shapes['Wetlands'] / triangle_shapes['Parcel_Area']) * 100)

#FILTER
triangle_shapes = triangle_shapes[(triangle_shapes['Acreage'] >= 5) & (triangle_shapes['Acreage'] <= 10)]

#triangle_shapes = triangle_shapes[(triangle_shapes['Building'] <= 300000)]

#triangle_shapes = triangle_shapes[(triangle_shapes['Wetlands'] < (0.4) * (triangle_shapes['Parcel_Area']))]

pd.set_option('precision',0)

triangle_shapes.to_file(r'filelocation')

