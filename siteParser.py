'''
    Another example of using the AsyncController to thread pulling web data. 

    In this example, it pulls the content from a web page and creates three unique 
    outputs:
        [NAME]_data     -> Text pulled from the page in the form of a JSON list
        [NAME]_images   -> List of images found in img tags, this data is in the form
                           of a JSON dictionary with uuid:url
        [NAME]_links    -> List of url links found in a tags, this data is in the form
                           of a JSON dictionary with uuid:url

    This could be extended to really crawl a site by downloading all images (tagging with UUID)
    and then crawling all of the links it found and also tagging results with UUID.

    The issue with crawling the sites is that it would take some serious work to ensure it 
    didn't try to collect too much information. A descision about depth of data would need
    to be made.  
'''

import time
import collections

from datetime import datetime, timedelta

from threadutils.Controller import AsyncController
from threadutils.Log import AsyncLog
from pageparser.threadfn import parse_endpoint
from pageparser.persist import createPath, writeContent

asyncController = AsyncController(15)

start = datetime.now()

endpoint_target = collections.namedtuple('endpoint_target', 'name url')

test_endpoints = [
    endpoint_target(name = "BostonGlobe", url = "http://www.boston.com"), 
    endpoint_target(name = "NASA", url = "https://www.nasa.gov"), 
    endpoint_target(name = "BostonHerald", url = "https://www.bostonherald.com/"), 
    endpoint_target(name = "AlJazeera", url = "https://www.aljazeera.com/")
    ]

for site in test_endpoints:
    asyncController.queueTask(parse_endpoint, site.name, site.url)

while asyncController.waitExecution(1) == False:
    print("MAIN - Waiting on execution....")

stop = datetime.now()


print("Execution Time: ", stop - start)
execution_results = asyncController.getExecutionResults()
dump_path = createPath(None)

for result in execution_results:
    name = result.result["name"] + '_'

    writeContent(dump_path, name + 'images', result.result["content"]["images"])
    writeContent(dump_path, name + 'data', result.result["content"]["data"])
    writeContent(dump_path, name + 'links', result.result["content"]["links"])

    print("Latency: ", result.latency.microseconds/1000)
    print("Name: ", result.result["name"])
