import arcgis, re
from arcgis import GIS

gis = GIS('Pro')

items = gis.content.search('tags:RadioCompass AND owner:mechomicky@burnsmcd.com_bmcd_gis', max_items=3000)

for i in items:
    if re.match(r'('
                r'.*?(?!(?:pO|uW))[a-z])([A-Z0-9].*)', i.title) is not None:
        print(f'renaming {i.title}')
        i.update(item_properties={'title': re.sub(r'(.*?(?!(?:pO|uW))[a-z])([A-Z0-9].*)', r'\1 \2', i.title)})
