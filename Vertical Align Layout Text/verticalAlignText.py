import arcpy, re
# Create an aprx object
aprx = arcpy.mp.ArcGISProject("CURRENT")

# Create a layout object for your layout. Assumes only one layout in project
# If project has more than one layout, need to list all layouts and find index of the desired layout and replace [0]
layout = aprx.listLayouts()[0]

# Create a map series object so the update can be run page by page
ms = layout.mapSeries
# Access the text element of the layout object. Assumes the element name is "Text". Replace below if name is different
text = layout.listElements("TEXT_ELEMENT", "Text")[0]

# Count the original number of newlines at the end of the label
newLines = len(re.findall('\n(?=(\n|$))(?!\n*\w)', text.text))

# Define a function to run on each page
def updateText():
    # Create regular expression to check for newlines at the start and end of the label text
    startLineRegex = '\n(?=(\n|\w))(?!\n+$|$)'
    endLineRegex = '\n(?=(\n|$))(?!\n*\w)'
    # Check whether there are more newlines at the end or the start of the label, start should have one more
    if len(re.findall(startLineRegex, text.text)) < len(re.findall(endLineRegex, text.text)):
        # More newlines at end, add to start and remove from end
        while len(re.findall(startLineRegex, text.text)) < len(re.findall(endLineRegex, text.text)):
            text.text = '\n' + text.text[:-1]
    elif len(re.findall(startLineRegex, text.text)) > len(re.findall(endLineRegex, text.text)):
        # More newlines at start, add to end
        while len(re.findall(startLineRegex, text.text)) > len(re.findall(endLineRegex, text.text)):
            text.text = text.text + '\n'

# Iterate over map series pages, running the update function and exporting the page
# Change the name and directory in ms.exportToPDF to the desired location and filename
for pageNum in range(1, ms.pageCount + 1):
    ms.currentPageNumber = pageNum
    updateText()
    ms.exportToPDF(r'C:\Users\mechomicky\Documents\Tests\TextTest_{}.pdf'.format(ms.pageRow.Name), 'CURRENT', image_quality="FASTEST")

# Reset text so that script will work properly next time
# First, strip all newlines from start and end of label
text.text = text.text.strip('\n')
# Next, add back in the original number of newlines
text.text += newLines * '\n'
