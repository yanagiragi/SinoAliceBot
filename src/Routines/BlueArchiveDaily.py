from enum import Enum
import time
import datetime

from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection


class Routine_BlueArchiveDaily(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)

    def Reset(self, frame):
        pass

    def Update(self):
        pass

    def QueryState(self):
        super().QueryState()
        
        self.state = State.IDLE
        currentDetected = None

        if self.hasDetected['blue_archive icon'].IsExist:
            self.state = State.BLUE_ARCHIVE_HOME
            currentDetected = self.hasDetected['blue_archive icon']

        # update Local Position
        if currentDetected is not None:
            self.localPosition = currentDetected.LocalPosition

    def StateAction(self):
        super().StateAction()
        top_left, bottom_right = self.localPosition

        statesShouldAction = [
            State.BLUE_ARCHIVE_HOME,
        ]

        if self.state in statesShouldAction:
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(3)

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'
