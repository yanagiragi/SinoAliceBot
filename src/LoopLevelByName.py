from enum import Enum
import time
import datetime

from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection

class Routine_LoopLevelByName(Routine):
    def __init__(self, name, control, target, accumulateCount, optimized=True):
        super().__init__(name, control, optimized)

        if target is None:
            raise Exception("target cannot be None")

        self.target = target
        self.difference = 100
        self.ShouldSwipeUp = False
        self.accumulateCount = accumulateCount

    def Reset(self, frame):
        pass

    def Update(self):
        pass
    
    def QueryState(self):
        super().QueryState()

        currentDetected = None

        if self.hasDetected['stage header'].IsExist and self.hasDetected['target stage'].IsExist == False:
            self.state = State.TARGET_STAGE_NOT_FOUND
            self.ShouldSwipeUp = True
            
        elif self.hasDetected['rematch'].IsExist:
            currentDetected = self.hasDetected['rematch']
            self.state = State.REMATCH

        elif self.hasDetected['osoujiText'].IsExist:
            currentDetected = self.hasDetected['osoujiText']
            self.state = State.NO_AP

        elif self.hasDetected['ok'].IsExist:
            currentDetected = self.hasDetected['ok']
            if self.prevState == State.NO_AP:
                self.state = State.OSOUJI_COMFIRM
            elif self.prevState == State.BATTLE:
                self.state = State.BATTLE_RESULT_COMFIRM
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

        # For some certain reason, we accidiently run into other pages we not suppose to be at
        # e.g. Ousouji result comfirm click too early
        # In this case, we try to fall back to story page
        elif self.hasDetected['story'].IsExist:
            self.state = State.HOME
            currentDetected = self.hasDetected['story']

        # Check for Stage Finding
        if not self.hasDetected['start'].IsExist:
            found = self.FindTargetStage()
            if found is not None:
                currentDetected = found

        # update doneCount
        if self.state == State.REMATCH and self.prevState == State.BATTLE_RESULT_COMFIRM:
            self.doneCount += 1
        elif self.state == State.NO_AP and self.state == State.REMATCH:
            self.doneCount -= 1 # minus "additional add" in last frame

        # check if is done right after doneCount is called
        if self.accumulateCount != 0 and self.doneCount >= self.accumulateCount:
            if found is None:
                self.state = State.CLEANUP_BEFORE_DONE
                currentDetected = self.hasDetected['ok']
            else:
                self.state = State.DONE
  
        # update Local Position
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
            State.CLEANUP_BEFORE_DONE
        ]
        
        if self.state == State.TARGET_LEVEL_NOT_FOUND or self.state == State.TARGET_STAGE_NOT_FOUND:
            aboveLocalPosition = [int((top_left[0] + bottom_right[0])/2), int((top_left[1] + bottom_right[1])/2) - self.difference]
            belowLocalPosition = [ aboveLocalPosition[0], aboveLocalPosition[1] + self.difference ]            
            if self.ShouldSwipeUp:
                self.control.SwipeUp(aboveLocalPosition, belowLocalPosition)
            else:
                self.control.SwipeDown(aboveLocalPosition, belowLocalPosition)

        if self.state in statesShouldAction:
            if self.state == State.OSOUJI_RESULT_COMFIRM:
                time.sleep(2)
                self.control.MouseLeftClick(top_left, bottom_right)
            else:
                self.control.MouseLeftClick(top_left, bottom_right)
                time.sleep(2.7)
        elif self.state == State.OSOUJI:
            self.control.OsoujiPathSlides()
            time.sleep(1)

    def FindTargetStage(self):
        currentDetected = None
        prevLevel = 0
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
            self.hasDetected['level EX'],
            self.hasDetected['level CX'],
        ]
        targetLevel = list(x for x in enumerate(checkList) if x[1].Name == self.target)[0][0] + 1 # 0 for id

        for idx, check in enumerate(checkList):
            if check.IsExist:
                currentDetected = check
                prevLevel = (idx + 1)
                if currentDetected.Name == self.target:
                    break
        
        if currentDetected is not None: # Currently on the page that select levels
            self.localPosition = currentDetected.LocalPosition # Update self.localPosition
            if prevLevel != targetLevel: # target does not exists in current frame
                self.ShouldSwipeUp = (prevLevel < targetLevel)
                self.state = State.TARGET_LEVEL_NOT_FOUND
            else:                 
                self.state = State.SELECT_LEVEL
                if self.prevState == State.STAGE_LOOP_END:
                    self.state = State.DONE

        return currentDetected

    def GetMessage(self):
        return super().GetMessage() + f', Accomplished = {self.doneCount}/{self.accumulateCount}, state = {self.state.value}'