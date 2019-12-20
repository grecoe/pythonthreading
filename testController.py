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
    Network requests are most benefitted by this....
'''
def callInAThread(arg1):
    if isinstance(arg1, tuple):
        if len(arg1) != 1:
            raise Exception("Incorrect argument count...")
        arg1 = arg1[0]

    r = requests.get(arg1)
    r.status_code
    AsyncLog.print("Thread: " + str(threading.get_ident()) + " : Called with:" + str(arg1) + " " + str(r.status_code))

'''
    Test the call with params and with a tuple
'''
url = "http://www.boston.com"

print("Call with regular args....")
callInAThread(url)
print("Call with tuple arg....")
callInAThread((url))
print("Call with invalid tuple arg....")
try:
    callInAThread((url,2))
except Exception as ex:
    print("ERROR: ", ex)


'''
    Call it 20 times no threading
'''
print("Call multiple times no thread...")
start = datetime.now()
for i in range(20):
    callInAThread(url)
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
    asyncController.queueTask(callInAThread, url)

while asyncController.waitExecution(1) == False:
    print("MAIN - Waiting on execution....")

stop = datetime.now()
thread_diff = stop - start
print(thread_diff)


print("Execution time no thread ", nothread_diff)
print("Execution time with thread ", thread_diff)
