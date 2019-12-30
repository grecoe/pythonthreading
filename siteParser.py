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
'''
test_endpoints = [
    endpoint_target(name = "BostonGlobe", url = "http://www.boston.com"), 
    endpoint_target(name = "NASA", url = "https://www.nasa.gov"), 
    endpoint_target(name = "BostonHerald", url = "https://www.bostonherald.com/"), 
    endpoint_target(name = "AlJazeera", url = "https://www.aljazeera.com/")
    ]
'''
test_endpoints = [
    endpoint_target(name = "BostonGlobe", url = "http://www.boston.com")
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
