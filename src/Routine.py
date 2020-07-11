import time
from enum import Enum
from abc import ABCMeta, abstractmethod

from src.State import State
import src.utils as utils

class Routine(metaclass=ABCMeta):
    def __init__(self, name, control, optimized=True):
        self.name = name
        self.control = control
        self.optimized = optimized
        
        self.frame = None
        
        self.state = State.IDLE
        self.prevState = State.IDLE        
        self.localPosition = [[0, 0], [0, 0]]
        self.hasDetected = {}

        self.doneCount = 0
        self.lastDoneTime = None
        self.accumulatedTime = None
        self.averageTimeString = None

    @abstractmethod
    def Reset(self, frame):
        self.frame = frame

    @abstractmethod
    def Update(self):
        pass

    @abstractmethod
    def QueryState(self):        
        if self.state != self.prevState: # Update prevState        
            self.prevState = self.state

        self.state = State.IDLE # Default state

    @abstractmethod
    def StateAction(self):
        pass

    @abstractmethod
    def GetMessage(self):
        return f', Avg time = {self.averageTimeString}'

    """
        return isError, errorMessage
    """
    def Process(self, frame):
        try:
            if self.state != State.DONE:
                tStart = time.time()
                self.Reset(frame)
                self.Update()
                self.QueryState()
                self.StateAction()
                tEnd = time.time()

                if self.accumulatedTime == None:
                    self.accumulatedTime = (tEnd - tStart)
                    self.averageTimeString = '00:00:00'
                else:
                    self.accumulatedTime += (tEnd - tStart)
                    self.averageTimeString = str(datetime.timedelta(seconds=int(float(self.accumulatedTime)/float(self.doneCount))))

                self.lastDoneTime = tEnd
                self.doneCount += 1

                return False, None
            else:
                return True, None
        except Exception as e:
            # sometime setForegroundWindow may raise error
            utils.printErr(e)
            # pass the iteration instead.
            return False, e