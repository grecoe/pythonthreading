import os
import collections
from tkinter import * 
from pageparser.sitepersist import WebSiteDataPersist, SiteDataPath
from tkinterui.searchUi import SearchWindow


'''
    This is the directory that siteParser.py is dumping data into. 
'''
base_directory = '.\\NEWSDATA'
'''
    These are the sub directory names that siteParser.py creates. 
'''
names = ["BostonGlobe", "BostonHerald", "SeattleTimes", "AlJazeera"]


'''
    Collect the data from the disk
'''
'''
    Set up a search criteria to find data you are interested in. This can be 
    done two ways.

    1. Identify the site you want and a specific day
    2. Using the site name, get all data paths and load them all. 
        HINT: You could filter days with this as well. 
'''
search_target = collections.namedtuple('search_target', 'name year month day')
search_criteria = []

for name in names:
    data_paths = WebSiteDataPersist.getAllDataPaths(base_directory, name)
    for path in data_paths:
        target = search_target(name = path.name, year = path.year, month = path.month, day = path.day)
        search_criteria.append(target)

'''
    Load the data using the search criteria. Result will be a dictionary or 
    dictionaries:

    {
        "SiteName": {"date", [data]}
    }
'''
site_data = {}
for criteria in search_criteria:
     data = WebSiteDataPersist.loadSiteData(base_directory,criteria.name, criteria.year, criteria.month, criteria.day)
     if data:
        # Data is dictionary 'text' : [date/time], so grab only the data. 
        if criteria.name not in site_data.keys():
            site_data[criteria.name] = {}
        date_key = "{}-{}-{}".format(criteria.month, criteria.day, criteria.year)    
        site_data[criteria.name][date_key] = list(data.keys()) 



'''
    Now with data, create the UI
'''
window = Tk()
window.title("News Search")
window.resizable(width=TRUE, height=TRUE)
app = SearchWindow(site_data, window)


app.mainloop()