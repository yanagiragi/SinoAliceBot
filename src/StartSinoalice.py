from enum import Enum
import time
import datetime

from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection
from src.Screen import WindowScreen

class Routine_StartSinoalice(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)
        self.hasClicked = False
        self.isDone = False

    def Reset(self, frame):
        pass

    def Update(self):
        pass
    
    def QueryState(self):
        super().QueryState()

        if self.hasDetected['maintence'].IsExist and self.hasDetected['cross'].IsExist:
            currentDetected = self.hasDetected['cross']
            self.localPosition = currentDetected.LocalPosition
            self.state = State.ONSTART
            self.hasClicked = False
            return

        elif self.hasDetected['Downloading'].IsExist:
            currentDetected = None
            self.localPosition = None
            self.state = State.DOWNLOADING
            if self.hasClicked == False:
                self.hasClicked = True

        if self.hasClicked == False:
            if self.hasDetected['Sinoalice Text'].IsExist:
                currentDetected = None
                sinoliceTextLocalPosition_topLeft, sinoliceTextLocalPosition_bottomRight = self.hasDetected['Sinoalice Text'].LocalPosition
                sinoliceTextLocalPositionYOffset = -100
                self.localPosition = [(sinoliceTextLocalPosition_topLeft[0], sinoliceTextLocalPosition_topLeft[1] + sinoliceTextLocalPositionYOffset), (sinoliceTextLocalPosition_bottomRight[0], sinoliceTextLocalPosition_bottomRight[1] + sinoliceTextLocalPositionYOffset)]
                self.state = State.ONSTART
        else:
            allWindows = WindowScreen.GetAllWindows()
            if allWindows != None and 'SINoALICE' in allWindows:
                self.isDone = True
            elif self.hasDetected['Update App'].IsExist:
                currentDetected = self.hasDetected['Update App']
                self.localPosition = currentDetected.LocalPosition
                self.state = State.DOWNLOADPOPOUT
        
    def StateAction(self):
        super().StateAction()

        if self.localPosition is None:
            return

        top_left, bottom_right = self.localPosition

        if self.state == State.ONSTART or self.state == State.DOWNLOADPOPOUT:
            time.sleep(1)
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(3)
            

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}, isClicked = {self.hasClicked}'