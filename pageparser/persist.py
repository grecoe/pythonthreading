from datetime import datetime
import os
import json

def createPath(base):
    if not base:
        base = './'
    
    now = datetime.now()
    path = [str(now.year), str(now.month), str(now.day)]
    path.append( str(now.hour) + '_' + str(now.minute))

    for part in path:
        base += part + '/'
        if not os.path.isdir(base):
            os.mkdir(base)

    return base

def writeContent(directory, name, content):
    localFileName = os.path.join(directory, name)
    with open(localFileName, 'w') as outputFile:
        outputFile.write(json.dumps(content, indent=4)) 
