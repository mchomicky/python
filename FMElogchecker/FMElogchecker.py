#! python3

import PySimpleGUI as sg
import os, time

FMEdir = 'C:\\Users\\mechomicky\\Documents\\FME\\Workspaces'
FMElogs = []
logStatus = {}

# Search Workspaces folder for .log files (modified current day?)
for file in os.listdir(FMEdir):
    if file.endswith('.log') and (time.time() - os.path.getmtime(os.path.join(FMEdir, file))) <= 86400:
        FMElogs.append(file)

# Open .logs, check for "Translation was SUCCESSFUL"
for log in FMElogs:
    logText = open(os.path.join(FMEdir, log))
    logText = logText.read()
    if "Translation was SUCCESSFUL" in logText:
        logStatus[log] = 'succeeded'
# If not successful, add to list of failed translations
    else:
        logStatus[log] = 'failed'

# create popup with any failed translations - if all were successful, then popup with all succeeded
popupText = ''
for translation, status in logStatus.items():
    popupText += translation + ': ' + status + '\n'
sg.PopupScrolled(popupText)