from enum import Enum
import time
import datetime

from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection
import requests

class Routine_Guild(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)

    def Reset(self, frame):
        pass

    def Update(self):
        pass
    
    def QueryState(self):
        super().QueryState()

        currentDetected = None

        if self.hasDetected['support'].IsExist:
            currentDetected = None
            self.state = State.APPSTART
            self.localPosition = [(180, 360), (180, 360)] # about center
        
        elif self.hasDetected['close'].IsExist:
            self.state = State.INFO
            currentDetected = self.hasDetected['close']

        elif self.hasDetected['skip'].IsExist:
            currentDetected = self.hasDetected['skip']
            self.state = State.STORY_SKIP

        # HomePage, next action = coop
        elif self.hasDetected['mission'].IsExist:
            self.state = State.HOME
            currentDetected = None
            self.localPosition = [(297, 52), (297, 52)]

        elif self.hasDetected['log'].IsExist:
            self.state = State.DONE
            currentDetected = None
            r = requests.post('http://pref.csie.io:3007/bot', data={})

        elif self.hasDetected['ok'].IsExist:
            currentDetected = self.hasDetected['ok']                

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
            State.SELECT_LEVEL_CONFIRM,
            State.BATTLE_RESULT_COMFIRM,
            State.CLEANUP_BEFORE_DONE,

            State.STORY_SKIP,
            State.APPSTART,
            State.INFO,
            State.COOP_NOT_PICK_GUILD_MEMBER_PANEL,
            State.COOP_PICK_GUILD_MEMBER_PANEL,
            State.COOP_SELECT_STAGE
        ]

        if self.state in statesShouldAction:
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(5)

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'