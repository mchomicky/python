import requests, bs4, re

# Create a function with ASR as the input to search the database and download the html
def searchASR(ASR):
    # Create the URL send the request and save the response to a variable
    url = 'https://www.fccinfo.com/CMDProASRLookup.php?sASR=' + str(ASR) + '&tabSearchType=ASR+Search'
    res = requests.get(url)
    res.raise_for_status()

    # Create a BeautifulSoup object to parse the html
    soup = bs4.BeautifulSoup(res.text)

    # Get all the table data elements
    tableData = soup.select('tr td')

    # Create a regex pattern object to search table data for NAD83 coordinates
    coordsNAD83 = re.compile(r'Structure Coordinates:\s+([0-9]{1,2})-([0-9]{1,2})-([0-9.]{3,4})\s+([NS])\s+([0-9]{1,2})-([0-9]{1,2})-([0-9.]{3,4})\s+([EW])\s+\(NAD 83\)')

    # Search for the pattern in the table data
    for td in tableData:
        coords = coordsNAD83.search(td.getText())
        if coords:
            lat = float(coords[1]) + float(coords[2])/60 + float(coords[3])/3600
            if coords[4] == 'S':
                lat *= -1
            long = float(coords[5]) + float(coords[6])/60 + float(coords[7])/3600
            if coords[8] == 'W':
                long *= -1
            print(str(lat) + ', ' + str(long))

searchASR(1299712)
