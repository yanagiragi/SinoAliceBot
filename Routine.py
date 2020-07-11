import utils

from enum import Enum
from abc import ABCMeta, abstractmethod
from State import State

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
        return ''

    """
        return isError, errorMessage
    """
    def Process(self, frame):
        try:
            if self.state != State.DONE:
                self.Reset(frame)
                self.Update()
                self.QueryState()
                self.StateAction()
                return False, None
            else:
                return True, None
        except Exception as e:
            # sometime setForegroundWindow may raise error
            utils.printErr(e)
            # pass the iteration instead.
            return False, e