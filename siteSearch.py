'''
    After running the siteParser.py you will have directories with the data contained
    from each of the parsing events.

    Use the following code to search for things: 
'''
import collections
from pageparser.sitepersist import WebSiteDataPersist, SiteDataPath

'''
    Set up a search criteria to find data you are interested in
'''
search_target = collections.namedtuple('search_target', 'name year month day')
search_criteria = {
    search_target(name = "BostonGlobe", year = '2020', month = '1', day = '2'),
    search_target(name = "BostonHerald", year = '2020', month = '1', day = '2'),
    search_target(name = "SeattleTimes", year = '2020', month = '1', day = '2'),
    search_target(name = "AlJazeera", year = '2020', month = '1', day = '2')
}

'''
    Load the data from the criteria
'''
site_data = {}
for criteria in search_criteria:
     data = WebSiteDataPersist.loadSiteData('.\\AAADATA',criteria.name, criteria.year, criteria.month, criteria.day)
     if data:
        # Data is dictionary 'text' : [date/time], so grab only the data. 
        site_data[criteria.name] = list(data.keys()) 

'''
    Now allow the user to search it.....
'''
while True:
    search_term = input("Enter a term to search (q to quit) > ")
    
    if search_term == 'q':
        break

    # Go through all the data and see if we have anything that matches
    sorted_keys = list(site_data.keys())
    sorted_keys.sort()
    for key in sorted_keys:
        # Case sensitive search
        #mentions = [entry for entry in site_data[key] if search_term in entry]
        # Case in-sesitive search
        mentions = [entry for entry in site_data[key] if search_term.lower() in entry.lower()]

        print(key, "(", len(mentions) ,"contains '", search_term, "') :")
        for mention in mentions:
            print("   ", mention)
        print("")

