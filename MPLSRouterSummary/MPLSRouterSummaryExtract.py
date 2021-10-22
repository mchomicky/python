import os, shutil, zipfile, re, PySimpleGUI as sg

# Create function to extract text files from the ZIP folder to the target folder, while renaming
# def summaryExtract(zipFile, targetDir):
    # Create a new subfolder within the specified target folder to hold the unzipped text files

# Define layout and success message to append to layout after function completes
layout = [[sg.T('Select target ZIP file:'),
           sg.FileBrowse(initial_folder='Z:\\Clients\\TND\\FirstEnr\\80936_ETF_2014_ISD\\_Program\\Design\\_Common'
                                        '\\Dsgn_Notes\\Adams Stuff\\_MPLS Configs\\Summaries', key='-zip-',
                         target='-inputZip-')],
          [sg.T('Selected ZIP file:'), sg.InputText('', key='-inputZip-')],
          [sg.T('Select destination for extract:'), sg.FolderBrowse(key='-dest-', target='-inputDest-')],
          [sg.T('Selected destination:'), sg.InputText('', key='-inputDest-')],
          [sg.T('Console:')],
          [sg.Multiline('', key='-console-')],
          [sg.Submit(), sg.Cancel()]]

successMsg = 'Files extracted successfully.'
errorMsg = 'Please specify a ZIP file and destination folder.'

window = sg.Window('Router Summary Extract', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Cancel'):
        break
    if event == 'Submit':
        consoleStat = ''
        print(os.path.exists(values['-zip-']))
        print(os.path.exists(values['-dest-']))
        '''for v in values.values():
            if v == '':
                sg.PopupOK(errorMsg)
                break
            else:
                summaryExtract(values['-zip-'], values['-dest-'])'''
