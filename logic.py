import pattern as Pattern
from enum import Enum

from control import *

class state(Enum):
    IDLE = 'idle'
    END_BATTLE = 'END_BATTLE'
    
    BATTLE = 'BATTLE'
    REMATCH = 'rematch'
    NO_AP = 'no ap'
    OSOUJI = 'osouji 中'
    OSOUJI_COMFIRM = 'osouji comfirm'
    OSOUJI_RESULT_COMFIRM = 'OSOUJI_RESULT_COMFIRM'
    HOME = 'HOME'
    SELECT_EVENT = 'SELECT_EVENT'
    SELECT_STAGE = 'SELECT_STAGE'
    SELECT_LEVEL = 'SELECT_LEVEL'
    OSOUJI_LEVEL_COMFIRM = 'OSOUJI_LEVEL_COMFIRM'
    SELECT_LEVEL_CONFIRM = 'SELECT_LEVEL_CONFIRM'

class Routine(Enum):
    LOOP_LEVEL = 'LOOP LEVEL'

class Logic:
    def __init__(self, optimized=True):
        self.prevState = state.IDLE
        self.state = state.IDLE

        # For Debug mode
        self.state = state.OSOUJI

        self.optimized = optimized
        self.routine = Routine.LOOP_LEVEL
        self.localPosition = [[0, 0], [0, 0]]
    
    def Reset(self, frame):     
        self.frame = frame   

    def Update(self):
        frame = self.frame
        self.hasDetected = {}
        for name, _pattern, threshold in Pattern.patterns:
            isExist, top_left, bottom_right = Pattern.Detect(frame, _pattern, threshold)
            self.hasDetected[name] = { "isExist": isExist, "localPosition": [top_left, bottom_right] }

    def QueryState(self):
        
        if self.state != self.prevState:
            self.prevState = self.state

        if self.routine == Routine.LOOP_LEVEL:
            currentDetected = None
            
            if self.hasDetected['rematch']['isExist']:
                currentDetected = self.hasDetected['rematch']
                self.state = state.REMATCH

            elif self.hasDetected['osoujiText']['isExist']:
                currentDetected = self.hasDetected['osoujiText']
                self.state = state.NO_AP

            elif self.hasDetected['ok']['isExist']:
                currentDetected = self.hasDetected['ok']
                if self.prevState == state.NO_AP:
                    self.state = state.OSOUJI_COMFIRM
                elif self.prevState == state.OSOUJI:
                    self.state = state.OSOUJI_RESULT_COMFIRM
                elif self.prevState == state.SELECT_LEVEL:
                    self.state = state.OSOUJI_LEVEL_COMFIRM
            
            # HomePage, next action = story
            elif self.hasDetected['mission']['isExist']:
                self.state = state.HOME
                currentDetected = self.hasDetected['story']

            # Story, next action = event
            elif self.hasDetected['event']['isExist']:
                self.state = state.SELECT_EVENT
                print('SELECT_EVENT')
                currentDetected = self.hasDetected['event']

            # Event, next action = stage
            elif self.hasDetected['stage']['isExist']:
                self.state = state.SELECT_STAGE
                currentDetected = self.hasDetected['stage']
        
            # Stage, next action = level
            elif self.hasDetected['level']['isExist']:
                self.state = state.SELECT_LEVEL
                currentDetected = self.hasDetected['level']

            elif self.hasDetected['start']['isExist']:
                self.state = state.SELECT_LEVEL_CONFIRM
                currentDetected = self.hasDetected['start']

            elif self.hasDetected['log']['isExist']:
                self.state = state.BATTLE
                currentDetected = None

            elif self.hasDetected['pause']['isExist']:
                self.state = state.OSOUJI
                currentDetected = None
            
            if currentDetected is not None:
                self.localPosition = currentDetected['localPosition']

    def StateAction(self, control):
        
        top_left, bottom_right = self.localPosition                

        if self.routine == Routine.LOOP_LEVEL:

            statesShouldAction = [
                state.REMATCH,
                state.NO_AP,
                state.OSOUJI_COMFIRM,
                state.OSOUJI_LEVEL_COMFIRM,
                state.OSOUJI_RESULT_COMFIRM,
                state.SELECT_EVENT,
                state.SELECT_STAGE,
                state.SELECT_LEVEL,
                state.HOME,
                state.SELECT_LEVEL_CONFIRM
            ]

            if self.state in statesShouldAction:
                control.MouseLeftClick(top_left, bottom_right)
                time.sleep(2.5)
            elif self.state == state.OSOUJI:
                control.OsoujiPathSlides()
                time.sleep(1)        
            
        return
            
    def Process(self, frame, control):
        self.Reset(frame)
        self.Update()
        self.QueryState()
        try:
            self.StateAction(control)
            return None
        except Exception as e:
            # sometime setForegroundWindow may raise error
            # pass the iteration instead.
            return e
