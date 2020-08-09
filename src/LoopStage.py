from enum import Enum
import time
import datetime

from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection

class Routine_LoopStage(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)
        self.prevLevel = 1

    def Reset(self, frame):
        pass

    def Update(self):
        pass
    
    def QueryState(self):
        super().QueryState()

        if self.state == State.DONE: # already Done
            return

        currentDetected = None

        if self.hasDetected['hard'].IsExist or self.hasDetected['normal'].IsExist:
            hardLocationY = self.hasDetected['hard'].LocalPosition[0][1] # y coordinate of left top corner
            normalLocationY = self.hasDetected['normal'].LocalPosition[0][1]            
            if hardLocationY > normalLocationY: # hard button is below
                currentDetected = self.hasDetected['hard']
                self.state = State.STAGE_NORMAL_IDLE
            else:
                currentDetected = self.hasDetected['normal']
                self.state = State.STAGE_HARD_IDLE
                if self.prevState == State.STAGE_LOOP_END:
                    self.state = State.DONE

        elif self.hasDetected['next'].IsExist:
            currentDetected = self.hasDetected['next']
            self.state = State.NEXT

        elif self.hasDetected['storySkip'].IsExist:
            currentDetected = self.hasDetected['storySkip']
            currentDetected = Detection("", True, (300, 400), (300, 400) )
            self.state = State.STORY_SKIP
        
        elif self.hasDetected['osoujiText'].IsExist:
            currentDetected = self.hasDetected['osoujiText']
            self.state = State.NO_AP

        elif self.hasDetected['ok'].IsExist:
            currentDetected = self.hasDetected['ok']
            if self.hasDetected['rematch'].IsExist:
                self.state = State.STAGE_LOOP_END
            elif self.hasDetected['rematch'].IsExist == False and self.hasDetected['next'].IsExist == False:
                self.state = State.STAGE_LOOP_END
            elif self.prevState == State.IDLE or self.prevState == State.BATTLE:
                self.state = State.SELECT_LEVEL_CONFIRM
            elif self.prevState == State.NO_AP:
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
        elif self.hasDetected['target stage'].IsExist:
            self.state = State.SELECT_STAGE
            currentDetected = self.hasDetected['target stage']
    
        # Stage, next action = level
        elif self.hasDetected['target level'].IsExist:
            self.state = State.SELECT_LEVEL
            currentDetected = self.hasDetected['target level']

        elif self.hasDetected['start'].IsExist:
            self.state = State.SELECT_LEVEL_CONFIRM
            currentDetected = self.hasDetected['start']

        elif self.hasDetected['log'].IsExist:
            self.state = State.BATTLE
            currentDetected = None

        elif self.hasDetected['pause'].IsExist:
            self.state = State.OSOUJI
            currentDetected = None
        
        # Has enter next level, increase prevLevel
        if self.state == State.BATTLE and self.prevState == State.NEXT:
            self.prevLevel += 1

        if currentDetected is not None:
            self.localPosition = currentDetected.LocalPosition

        self.DeterminePrevStage()

    def StateAction(self):
        super().StateAction()

        top_right, bottom_right = self.localPosition
        statesShouldAction = [
            # State.REMATCH, # No Rematch
            State.NO_AP,
            State.OSOUJI_COMFIRM,
            State.OSOUJI_LEVEL_COMFIRM,
            State.OSOUJI_RESULT_COMFIRM,
            State.SELECT_EVENT,
            State.SELECT_STAGE,
            State.SELECT_LEVEL,
            State.SELECT_LEVEL_CONFIRM,
            State.HOME,
            State.STORY_SKIP,
            State.NEXT,
            State.STAGE_LOOP_END,
            State.STAGE_NORMAL_IDLE,
        ]

        if self.state in statesShouldAction:            
            self.control.MouseLeftClick(top_right, bottom_right)
            
            # Special delays for certain states
            if self.prevState == State.STAGE_LOOP_END:
                time.sleep(5)
            elif self.state == State.OSOUJI_RESULT_COMFIRM:
                time.sleep(5)
            elif self.state == State.STAGE_LOOP_END:
                time.sleep(3.5)
            else:
                time.sleep(2.5)

        elif self.state == State.OSOUJI:
            self.control.OsoujiPathSlides()
            time.sleep(1)
    
    def GetMessage(self):
        return super().GetMessage() + ', Now Level = {}, state = {}'.format(self.prevLevel, self.state.value)

    def DeterminePrevStage(self):
        currentDetected = None
        checkList = [
            self.hasDetected['level 1'],
            self.hasDetected['level 2'],
            self.hasDetected['level 3'],
            self.hasDetected['level 4'],
            self.hasDetected['level 5'],
            self.hasDetected['level 6'],
            self.hasDetected['level 7'],
            self.hasDetected['level 8'],
            self.hasDetected['level 9'],
            self.hasDetected['level 10'],
            self.hasDetected['level EX-L'],
            self.hasDetected['level CX'],
        ]

        for idx, check in enumerate(checkList):
            if check.IsExist:
                currentDetected = check
                self.prevLevel = (idx + 1)
        
        if currentDetected is not None:
            self.localPosition = currentDetected.LocalPosition
            self.state = State.SELECT_LEVEL
            if self.prevState == State.STAGE_LOOP_END:
                self.state = State.DONE

        return currentDetected
