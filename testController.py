'''
    Set up a call to be used in a threaded context. 

    - Call must take into account that when called in a threaded context that 
      it must unpack the first argument as a tuple and verify that it is, in fact
      the right number of incoming arguments.
    - Calls with more than one arg MUST set the follow on args after the first one 
      to None because only the first arg will be present if called from a thread.
'''
import threading
import time
import requests
from datetime import datetime, timedelta
from threadutils.Controller import AsyncController
from threadutils.Log import AsyncLog

'''
    This is the call we are going to use in the thread. Any return value 
    will be accumulated by the controller. 
'''
def networkCall(url):
    '''
        IF it's a tuple then it's a threaded call from the controller 
        and we need to unpack it. 
    '''
    if isinstance(url, tuple):
        if len(url) != 1:
            raise Exception("Incorrect argument count...")
        url = url[0]

    r = requests.get(url)
    r.status_code

    return {'target' : url, 'result' : r.status_code}

'''
    Test the call with params and with a tuple
'''
url = "http://www.boston.com"

print("Call with regular args....")
networkCall(url)
print("Call with tuple arg....")
networkCall((url))
print("Call with invalid tuple arg....")
try:
    networkCall((url,2))
except Exception as ex:
    print("ERROR: ", ex)


'''
    Call it 20 times no threading
'''
print("Call multiple times no thread...")
start = datetime.now()
for i in range(20):
    print(networkCall(url))
stop = datetime.now()
nothread_diff = stop - start
print(nothread_diff)


'''
    Now set up a controller and call it 20 times
'''
print("Thread it")
asyncController = AsyncController(10)

start = datetime.now()

for i in range(20):
    asyncController.queueTask(networkCall, url)

while asyncController.waitExecution(1) == False:
    print("MAIN - Waiting on execution....")

total_latency = 0
for result in asyncController.getExecutionResults():
    current_latency = (result.latency.microseconds/1000)
    total_latency += current_latency
    print("Latency (ms): ", current_latency, "Result: ", result.result)

stop = datetime.now()
thread_diff = stop - start
print(thread_diff)


print("Execution time no thread ", nothread_diff)
print("Execution time with thread ", thread_diff)
print(" Latency in thread (s): ", total_latency)
