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
    Call it 20 times no threading. Time it so we can 
    see how long it takes regularly. 
'''
print("Call multiple times no thread...")
start = datetime.now()
for i in range(20):
    print(networkCall(url))
stop = datetime.now()
nothread_diff = stop - start
print(nothread_diff)


'''
    Now set up a controller and call it 20 times via threads. We will time 
    this too to see the difference in timing. 

    NOte that the results collected by the controller are a 
    named tuple with 
        latency - datetime.timedelta
        result - Whatever the function returns, if anything
'''
print("Thread it")
asyncController = AsyncController(10)

start = datetime.now()

for i in range(20):
    asyncController.queueTask(networkCall, url, "invalid parameter")

'''
    Threads do not join the main thread, wait until they 
    are all finished.
'''
while asyncController.waitExecution(1) == False:
    print("MAIN - Waiting on execution....")

'''
    Now that they are all done, get the results and you can 
    see the latency of each call as well as any result it might
    have returned. 
'''
total_latency = 0
for result in asyncController.getExecutionResults():
    current_latency = (result.latency.microseconds/1000000)
    total_latency += current_latency

    result_output = result.result
    if isinstance(result_output, Exception):
        result_output = {"ERROR" : result.result}

    print("Latency (ms): ", current_latency, "Result: ", result_output)

stop = datetime.now()
thread_diff = stop - start
print(thread_diff)


print("Execution time no thread ", nothread_diff)
print("Execution time with thread ", thread_diff)
print(" Latency in thread (s): ", total_latency)
