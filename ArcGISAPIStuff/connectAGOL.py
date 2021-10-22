import os, arcpy
from arcgis.gis import GIS

gis = GIS('Pro')    # Use AGOL Portal from Pro - couldn't figure out how to directly authorize connection

# change below to be user input location of the files
os.chdir('\\\\B712137\\Users\\mechomicky\\Documents\\FE RadioCompass KMZ\\tpks\\JCPL\\Tinton Falls')

# change below to use user specified type and folder
for file in os.listdir(os.getcwd()):
    print('Uploading ' + file + '... ', end='')
    tpk_item = gis.content.add({'type':'Tile Package'}, data=file, folder='JCPL TPK')
    print('Done.')
    tpk_item.publish()
    print('Tile Package ' + file[:-5] + ' published.')