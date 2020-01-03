'''
    After running the siteParser.py you will have directories with the data contained
    from each of the parsing events.

    Use the following code to search for things: 
'''
import collections
import os
from pageparser.sitepersist import WebSiteDataPersist, SiteDataPath

use_specific_day = False
base_directory = '.\\AAADATA'


'''
    Set up a search criteria to find data you are interested in. This can be 
    done two ways.

    1. Identify the site you want and a specific day
    2. Using the site name, get all data paths and load them all. 
        HINT: You could filter days with this as well. 
'''
search_target = collections.namedtuple('search_target', 'name year month day')
search_criteria = []

if use_specific_day:
    search_criteria = [
        search_target(name = "BostonGlobe", year = '2020', month = '1', day = '2'),
        search_target(name = "BostonHerald", year = '2020', month = '1', day = '2'),
        search_target(name = "SeattleTimes", year = '2020', month = '1', day = '2'),
        search_target(name = "AlJazeera", year = '2020', month = '1', day = '2')
    ]
else:
    names = ["BostonGlobe", "BostonHerald", "SeattleTimes", "AlJazeera"]
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
    Now allow the user to search it.....
'''
while True:
    search_term = input("Enter a term to search (q to quit) > ")
    
    if search_term == 'q':
        break

    # Go through each site and see if we have anything that matches. 
    # Key in the outer dictionary is the name
    sorted_keys = list(site_data.keys())
    sorted_keys.sort()
    for site_key in sorted_keys:
        # We have the key to the site, but we need to get keys to the data
        dated_mentions = {}
        for date_key in site_data[site_key]:
            # Case in-sesitive search of all data using list comprehension
            dated_mentions[date_key] = [entry for entry in site_data[site_key][date_key] if search_term.lower() in entry.lower()]

        # Print out the results
        print(site_key, "('" + search_term, "') :")
        for date_key in dated_mentions:
            print("   " , date_key)
            for mention in dated_mentions[date_key]:
                print("    ", mention)
        print("")

    input("Press a key to search again...")
    os.system('cls')

