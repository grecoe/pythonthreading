'''
    Another example of using the AsyncController to thread pulling web data. 

    In this example, it pulls the content from a web page and creates outputs for each
    web site it is pointed at. The data is collected in a directory (locally) in the form:
    
        [NAME]/year/month/day
    output files:
        run_history -> List of date/times (strings) of times run on a given day. 

        data     -> Text pulled from the page in the form of a JSON dictionary
                    { 
                       'data' : [str of date/time seen]
                    }

        images   -> List of images (img tag) in the form of a JSON dictionary
                    {
                        'imglink' : { 'id' : 'uuid', 'occurance' : [str of date/time seen]}
                    }

        links    -> List of url links (a tag) in the form of a JSON dictionary
                    {
                        'link' : { 'id' : 'uuid', 'occurance' : [str of date/time seen]}
                    }


    This could be extended to really crawl a site by downloading all images (tagging with UUID)
    and then crawling all of the links it found and also tagging results with UUID.

    The issue with crawling the sites is that it would take some serious work to ensure it 
    didn't try to collect too much information. A descision about depth of data would need
    to be made.  
'''

import time
import json
import collections

from datetime import datetime, timedelta

from threadutils.Controller import AsyncController
from threadutils.Log import AsyncLog
from pageparser.threadfn import parse_endpoint
from pageparser.persist import createPath
from pageparser.sitepersist import WebSiteDataPersist

'''
    Maximum of 15 worker threads.
'''
asyncController = AsyncController(15)

start = datetime.now()

endpoint_target = collections.namedtuple('endpoint_target', 'name url')
test_endpoints = [
    endpoint_target(name = "BostonGlobe", url = "http://www.boston.com"), 
    endpoint_target(name = "BostonHerald", url = "https://www.bostonherald.com/"), 
    endpoint_target(name = "SeattleTimes", url = "https://www.seattletimes.com/"),
    endpoint_target(name = "AlJazeera", url = "https://www.aljazeera.com/")
    ]
'''
test_endpoints = [
    endpoint_target(name = "BostonGlobe", url = "http://www.boston.com") 
    ]
'''

# Setting the min word count limits the page data returned to entries containing at 
# least that many words. This essentially limits links to things like travel, etc. 
min_word_count_data = 2
for site in test_endpoints:
    asyncController.queueTask(parse_endpoint, site.name, site.url, min_word_count_data)

while asyncController.waitExecution(1) == False:
    print("MAIN - Parsing web data....")

stop = datetime.now()


print("Execution Time: ", stop - start)
execution_results = asyncController.getExecutionResults()

'''
    Now create the outputs for each of the sites searched and persist the 
    data onto the disk. 
'''
job_time = datetime.now()
for result in execution_results:
    # Creates path name/year/month/day
    dump_path = createPath(".\\AAADATA", result.result["name"], job_time)

    # Update runs for day
    WebSiteDataPersist.updateSiteRunHistory(dump_path, job_time)

    # Update lines of data found for the day
    WebSiteDataPersist.updateSiteData(dump_path,job_time, result.result["content"]["data"] )
    # Update image and link data for the day
    WebSiteDataPersist.updateSiteImages(dump_path, job_time,result.result["content"]["images"])
    WebSiteDataPersist.updateSiteLinks(dump_path, job_time,result.result["content"]["links"])

    print("Latency: ", result.latency.microseconds/1000)
    print("Name: ", result.result["name"])
