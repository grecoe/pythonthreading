from datetime import datetime
import os
import json

def normalizeBase(base):
    if not base:
        base = '.\\'
    elif not os.path.isdir(base):
        os.mkdir(base)

    if not base.endswith('\\'):
        base += '\\'

    return base

def createPath(base, name, time_stamp = datetime.now()):
    '''
        Builds up a directory structure based on

        NAME/Year/Month/Day
    '''
    base = normalizeBase(base)
    
    path = [name, str(time_stamp.year), str(time_stamp.month), str(time_stamp.day)]

    for part in path:
        base += part + '\\'
        if not os.path.isdir(base):
            os.mkdir(base)

    return base

def writeContent(directory, name, content):
    '''
        Dump out ALL content of a sequence as JSON. 
    '''
    localFileName = os.path.join(directory, name)
    with open(localFileName, 'w') as outputFile:
        outputFile.write(json.dumps(content, indent=4)) 

def loadContent(directory, name = None):
    file_data = None

    # Might have the file on it already
    file_path = directory 
    if name :
        file_path = os.path.join(directory,name)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file_read:
            file_content = file_read.readlines()
            file_data = '\n'.join(file_content)
    return file_data