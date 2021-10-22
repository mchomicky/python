import arcpy
from arcgis import GIS

# establish connection to AGOL
gis = GIS('Pro')

# search for the Feature Layer item
search_result = gis.content.search('FE_LineFeatureClass', 'Feature Layer')
# the item will be the first item in the search_result list
lineFCItem = search_result[0]
# access the FiberStrands table (first item in the tables list for the lineFCItem)
strandTable = lineFCItem.tables[0]

# save script tool parameters as variables
# line (parameter 0) should be set to Data Type = Feature Layer in the Tool Properties, so that a layer from the map can be used as input
line = arcpy.GetParameterAsText(0)
# add strand counts to a list to iterate over and run the function
# strand count parameters are set to Data Type = String in the Tool Properties - integer doesn't seem to be an option, so must convert
strandsList = [{'type':'ndsf', 'count': int(arcpy.GetParameterAsText(2)), 'label': 'NDSF (G.652)', 'mode': 'SMF'},
            {'type': 'dsf', 'count': int(arcpy.GetParameterAsText(3)), 'label': 'DSF (G.653)', 'mode': 'SMF'},
            {'type': 'nzdsf','count': int(arcpy.GetParameterAsText(4)), 'label': 'NZ-DSF (G.655)', 'mode': 'SMF'},
            {'type': 'om1', 'count': int(arcpy.GetParameterAsText(5)), 'label': 'OM1', 'mode': 'MMF'},
            {'type': 'om2', 'count': int(arcpy.GetParameterAsText(6)), 'label': 'OM2', 'mode': 'MMF'},
            {'type': 'om3', 'count': int(arcpy.GetParameterAsText(7)), 'label': 'OM3', 'mode': 'MMF'},
            {'type': 'om4', 'count': int(arcpy.GetParameterAsText(8)), 'label': 'OM4', 'mode': 'MMF'},
            {'type': 'om5', 'count': int(arcpy.GetParameterAsText(9)), 'label': 'OM5', 'mode': 'MMF'},
            {'type': 'unk', 'count': int(arcpy.GetParameterAsText(10)), 'label': None, 'mode': None}]

# raise error if sum of individual strand type counts does not equal total
totStrands = int(arcpy.GetParameterAsText(1))
summedCount = 0
for i in strandsList:
    summedCount += i['count']
if summedCount != totStrands:
    arcpy.AddError('Strand Type counts do not equal Total Strands')

# get GlobalID of the selected line, raise error if more than one line was selected when running this tool
cursor = arcpy.da.SearchCursor(line, field_names='GlobalID')
cursorCnt = 0
for row in cursor:
    key = row[0]
    cursorCnt += 1
if cursorCnt > 1:
    arcpy.AddError('Please select only one fiber line to add strands')

# define a function to create strand objects based on the provided counts
strands = []
strandNum = 1
def createFiberStrands(qty, type, mode):
    global strandNum
    while qty > 0:
        strands.append({'attributes':
            {'LineFeatureClassGUID': key,
             'StrandNumber': strandNum,
             'StrandType': type,
             'Mode': mode
             }
        })
        strandNum += 1
        qty -= 1

# run the function for each type of strand
for i in strandsList:
    if i['count'] != 0:
        createFiberStrands(i['count'], i['label'], i['mode'])

# append the results to the table
strandTable.edit_features(adds=strands)