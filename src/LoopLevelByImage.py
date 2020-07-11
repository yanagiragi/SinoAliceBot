from enum import Enum
import time
import datetime

from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection

class Routine_LoopLevelByImage(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)
        self.waitTimeString = None
        self.battleCount = 0
        self.osoujiCount = 0

    def Reset(self, frame):
        pass

    def Update(self):
        pass
    
    def QueryState(self):
        super().QueryState()

        currentDetected = None
            
        if self.hasDetected['rematch'].IsExist:
            currentDetected = self.hasDetected['rematch']
            self.state = State.REMATCH

        elif self.hasDetected['osoujiText'].IsExist:
            currentDetected = self.hasDetected['osoujiText']
            self.state = State.NO_AP

        elif self.hasDetected['ok'].IsExist:
            currentDetected = self.hasDetected['ok']
            if self.prevState == State.NO_AP:
                self.state = State.OSOUJI_COMFIRM
            elif self.prevState == State.OSOUJI:
                self.state = State.OSOUJI_RESULT_COMFIRM
            elif self.prevState == State.SELECT_LEVEL:
                self.state = State.OSOUJI_LEVEL_COMFIRM
        
        # HomePage, next action = story
        elif self.hasDetected['mission'].IsExist:
            self.state = State.HOME
            currentDetected = self.hasDetected['story']

        # Story, next action = event
        elif self.hasDetected['event'].IsExist:
            self.state = State.SELECT_EVENT
            currentDetected = self.hasDetected['event']

        # Event, next action = stage
        elif self.hasDetected['stage'].IsExist:
            self.state = State.SELECT_STAGE
            currentDetected = self.hasDetected['stage']
    
        # Stage, next action = level
        elif self.hasDetected['level'].IsExist:
            self.state = State.SELECT_LEVEL
            currentDetected = self.hasDetected['level']

        elif self.hasDetected['start'].IsExist:
            self.state = State.SELECT_LEVEL_CONFIRM
            currentDetected = self.hasDetected['start']

        elif self.hasDetected['log'].IsExist:
            self.state = State.BATTLE
            currentDetected = None

        elif self.hasDetected['pause'].IsExist:
            self.state = State.OSOUJI
            currentDetected = None
        
        if currentDetected is not None:
            self.localPosition = currentDetected.LocalPosition
        
    def StateAction(self):
        super().StateAction()

        top_left, bottom_right = self.localPosition

        statesShouldAction = [
            State.REMATCH,
            State.NO_AP,
            State.OSOUJI_COMFIRM,
            State.OSOUJI_LEVEL_COMFIRM,
            State.OSOUJI_RESULT_COMFIRM,
            State.SELECT_EVENT,
            State.SELECT_STAGE,
            State.SELECT_LEVEL,
            State.HOME,
            State.SELECT_LEVEL_CONFIRM
        ]

        if self.state in statesShouldAction:            
            self.control.MouseLeftClick(top_left, bottom_right)
            if self.state == State.OSOUJI_RESULT_COMFIRM:
                time.sleep(5)
            else:
                time.sleep(2.5)
        elif self.state == State.OSOUJI:
            self.control.OsoujiPathSlides()
            time.sleep(1)
    
    def UpdateState(self):           

        if self.prevState != self.state and self.state == State.REMATCH:
            self.battleCount += 1
        
        elif self.prevState != self.state and self.state == State.OSOUJI_RESULT_COMFIRM:
            self.osoujiCount += 1

    def GetMessage(self):
        if self.battleCount == 0:
            self.waitTimeString = '00:00:00'
        else:
            self.waitTimeString = str(datetime.timedelta(seconds=int(float(self.accumulatedTime)/float(self.battleCount))))

        # note we don't call super().GetMessage()
        return f', Accomplished = {self.battleCount}, Avg Time = {self.waitTimeString}, state = {self.state.value}'