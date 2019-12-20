from threading import *
from threadutils.Tracking import ThreadTracking
from threadutils.Log import AsyncLog

class ExecuteCommandAsync(Thread):
    '''
        Thread class used when processing items - parseObject() because in VM's it can create a secondary call
        that is incredibly slow. 
    '''
    def __init__(self, callback, expansion_tracking, operation, *args):
        Thread.__init__(self)
        self.tracking = expansion_tracking
        self.executionFunction = operation
        self.executionArguments = args
        self.callback = callback

    def run(self):
        self.tracking.modifyThreadCount(1)

        new_obj = self.executionFunction(self.executionArguments)

        self.tracking.addThreadResult(new_obj)
        self.tracking.modifyThreadCount(-1)

        #AsyncLog.print("WORKER COMPLETE")

        if self.callback:
            self.callback()
