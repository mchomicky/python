import os, shutil, zipfile, re, PySimpleGUI as sg

zipFile = 'Z:\\Clients\\TND\\FirstEnr\\80936_ETF_2014_ISD\\_Program\\Design\\_Common\\Dsgn_Notes\\Adams Stuff\\_MPLS Configs\\Summaries\\2020-03-17.zip'
targetDir = 'C:\\Users\\mechomicky\\Documents'

# Create a new subfolder within the specified target folder to hold the unzipped text files
# Change working directory to newly created folder
targetDir = os.path.join(targetDir, os.path.basename(zipFile)[:-4])

for i in range(0, 101):
    if i == 0:
        try:
            os.makedirs(targetDir)
            os.chdir(targetDir)
            print(targetDir + ' successfully created.\n')
            break
        except FileExistsError:
            print(targetDir + ' already exists.\n')
            continue
    else:
        try:
            os.makedirs(targetDir + '_' + str(i))
            os.chdir(targetDir + '_' + str(i))
            print(targetDir + '_' + str(i) + ' successfully created.\n')
            break
        except FileExistsError:
            print(targetDir + '_' + str(i) + ' already exists.\n')
            continue

# Extract the contents of the ZIP file to the newly created folder
zipFile = zipfile.ZipFile(zipFile)
zipFile.extractall()
zipFile.close()

# Loop through text files, renaming the file to the name specified in Location
locPattern = re.compile(r'''Location\s*:\s*            # beginning of line and Location: label
                            ([_,'.&:#)(/0-9a-zA-Z\s]+) # first capture group - OpCo or Site Name
                            -*\s*                      # separator between capture groups (optional)
                            ([_,'.:#)(/0-9a-zA-Z\s]*)  # optional second capture group - Site Name or specific location
                            -*\s*                      # separator between capture groups (optional)
                            ([_,/0-9a-zA-Z\s]*)        # optional third capture group
                            \**\n\s+Coordinates        # end of pattern
                            ''', re.VERBOSE)
fepPattern = re.compile(r'(\s+(?:FEP)*\s*[a-z]{0,2}([0-9][a-z][0-9])|[0-9]{4}[A-Z]{2})')
newline = re.compile(r'\n\s*')
voltageZero = re.compile(r'^0{1,2}([0-9]{1,2})')

for txt in os.listdir('.'):
    print('Current file: ' + txt + '\n')
    newName = ''
    hasFep = False
    txtFile = open(os.path.join(targetDir, txt))
    txtContent = txtFile.read()
    location = locPattern.search(txtContent)
    try:
        mo = list(location.groups())
    except AttributeError:
        print('No location name detected - may contain illegal characters\n')
        continue
    # clean out newline characters (with or without trailing whitespace)
    for n in range(0, len(mo)):
        if newline.search(mo[n]) is None:
            continue
        else:
            mo[n] = newline.sub(' ', mo[n])
    # clear out leading and trailing whitespace
    for n in range(0, len(mo)):
        mo[n] = mo[n].strip()
    # search for FEP Channel, remove FEP from the string
    for n in range(0, len(mo)):
        if fepPattern.search(mo[n]) is None:
            continue
        else:
            hasFep = True
            mo[n] = re.sub(r'FEP\s*', '', mo[n])
    # remove leading zeros from the voltage
    for n in range(0, len(mo)):
        if voltageZero.search(mo[n]) is None:
            continue
        else:
            mo[n] = voltageZero.sub(r'\1', mo[n])
    # remove / from groups
    for n in range(0, len(mo)):
        if '/' in mo[n]:
            mo[n] = mo[n].replace('/', '_')
        else:
            continue
    # remove / from groups
    for n in range(0, len(mo)):
        if ':' in mo[n]:
            mo[n] = mo[n].replace(':', '')
        else:
            continue
    # delete groups if they are empty string
    while '' in mo:
        mo.remove('')
    # build the new file name
    if len(mo) == 1:
        newName = mo[0]
    elif len(mo) == 2 and hasFep is True:
        newName = mo[0] + ' ' + mo[1]
    elif len(mo) == 2:
        newName = mo[1]
    else:
        newName = mo[1] + ' ' + mo[2]
    txtFile.close()
    # rename the file
    suffix = 1
    suffixName = ''
    while os.path.isfile('.\\' + newName + '.txt'):
        suffixName = newName + ' ' + str(suffix)
        suffix += 1
        if os.path.isfile('.\\' + suffixName + '.txt'):
            continue
        else:
            newName = suffixName
            break
    print('Renamed to ' + newName + '\n\n')
    shutil.move('.\\' + txt, '.\\' + newName + '.txt')
