from enum import Enum
import time
import datetime

from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection


class Routine_OpenBlueArchive(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)

        self.difference = 200
        self.ShouldSwipeUp = False
        self.accumulateCount = 0

    def Reset(self, frame):
        pass

    def Update(self):
        pass

    def QueryState(self):
        super().QueryState()

        currentDetected = None

        # update Local Position
        if currentDetected is not None:
            self.localPosition = currentDetected.LocalPosition

    def StateAction(self):
        super().StateAction()
        top_left, bottom_right = self.localPosition

    def GetMessage(self):
        return super().GetMessage() + f', Accomplished = {self.doneCount}/{self.accumulateCount}, state = {self.state.value}'
