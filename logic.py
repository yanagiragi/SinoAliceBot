import Pattern
from enum import Enum

from control import *

from State import *

from Routine import Routine
from LoopStage import Routine_LoopStage
from Detection import Detection

class Routines(Enum):
    LOOP_SINGLE_LEVEL = 'LOOP LEVEL'
    LOOP_STAGE = 'LOOP STAGE' # 第一次跑關卡時，跑通整個流程

class Logic(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)
        
        # Set Current Routine
        self.routine = Routine_LoopStage('Routine.Loop_Stage', control, optimized)
    
    def Reset(self, frame):
        super().Reset(frame)
        
        # Call Reset() to current routine
        self.routine.Reset(frame)

    def Update(self):
        super().Update()
        
        for name, template, threshold in Pattern.patterns:
            isExist, top_left, bottom_right = Pattern.Detect(self.frame, template, threshold)

            # Need Refactor
            self.routine.hasDetected[name] = Detection(name, isExist, top_left, bottom_right)

        # Call Update() to current routine
        self.routine.Update()
    
    def QueryState(self):        
        super().QueryState()

        # Call QueryState() to current routine
        self.routine.QueryState()

    def StateAction(self): 
        super().StateAction()

        # Call StateAction() to current routine
        self.routine.StateAction()

    def Process(self, frame):
        try:
            if self.routine.state != State.DONE:
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

    def GetMessage(self):
        return super().GetMessage() + self.routine.GetMessage()

    def Routine_Loop_SingleLevel(self):
        currentDetected = None
            
        if self.hasDetected['rematch']['isExist']:
            currentDetected = self.hasDetected['rematch']
            self.state = State.REMATCH

        elif self.hasDetected['osoujiText']['isExist']:
            currentDetected = self.hasDetected['osoujiText']
            self.state = State.NO_AP

        elif self.hasDetected['ok']['isExist']:
            currentDetected = self.hasDetected['ok']
            if self.prevState == State.NO_AP:
                self.state = State.OSOUJI_COMFIRM
            elif self.prevState == State.OSOUJI:
                self.state = State.OSOUJI_RESULT_COMFIRM
            elif self.prevState == State.SELECT_LEVEL:
                self.state = State.OSOUJI_LEVEL_COMFIRM
        
        # HomePage, next action = story
        elif self.hasDetected['mission']['isExist']:
            self.state = State.HOME
            currentDetected = self.hasDetected['story']

        # Story, next action = event
        elif self.hasDetected['event']['isExist']:
            self.state = State.SELECT_EVENT
            currentDetected = self.hasDetected['event']

        # Event, next action = stage
        elif self.hasDetected['stage']['isExist']:
            self.state = State.SELECT_STAGE
            currentDetected = self.hasDetected['stage']
    
        # Stage, next action = level
        elif self.hasDetected['level']['isExist']:
            self.state = State.SELECT_LEVEL
            currentDetected = self.hasDetected['level']

        elif self.hasDetected['start']['isExist']:
            self.state = State.SELECT_LEVEL_CONFIRM
            currentDetected = self.hasDetected['start']

        elif self.hasDetected['log']['isExist']:
            self.state = State.BATTLE
            currentDetected = None

        elif self.hasDetected['pause']['isExist']:
            self.state = State.OSOUJI
            currentDetected = None
        
        if currentDetected is not None:
            self.localPosition = currentDetected['localPosition']   

    def DealAction_Loop_SingleLevel(self, control):
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
        ]

        if self.state in statesShouldAction:            
            control.MouseLeftClick(top_left, bottom_right)
            if self.state == State.OSOUJI_RESULT_COMFIRM:
                time.sleep(5)
            else:
                time.sleep(2.5)
        elif self.state == State.OSOUJI:
            control.OsoujiPathSlides()
            time.sleep(1)