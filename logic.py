import pattern
from enum import Enum

from control import *

class state(Enum):
    IDLE = 'idle'
    LOBBY = 'lobby'
    SELECT_MISSION = 'select mission'
    MISSION_BRIEF = 'mission brief selected'
    MISSION_BRIEF_SELECTED = 'mission brief pending'
    COMFIRM = 'confirm'
    LEAVE = 'leave'
    LOADING = 'loading'
    NPC_DIALOG = 'npc dialog'
    END_BATTLE = 'battle end'
    BATTLE = 'battle'

class Logic:
    def __init__(self, optimized=True):
        self.state = state.IDLE
        self.optimized = optimized
    
    def Reset(self, frame):     
        self.frame = frame   

    def Update(self):
        frame = self.frame

    def QueryState(self):
        self.state = state.IDLE
    
    def StateAction(self, control):

        return

        def LeftClick(top_left, bottom_right):
            # click center
            localPosition = [int((top_left[0] + bottom_right[0])/2), int((top_left[1] + bottom_right[1])/2)]
            control.MouseLeftClick(localPosition)            
            control.MouseMove([0,0])
        
        self.hasDetectNext, top_left, bottom_right = pattern.Detect(self.frame, pattern.nextPattern, 0.8)
        canEarlyBreak = self.hasDetectNext
        if self.optimized and canEarlyBreak: # Early Break
            LeftClick(top_left, bottom_right)
            return

        self.hasDetectOk, top_left, bottom_right = pattern.Detect(self.frame, pattern.okPattern, 0.4)
        canEarlyBreak = self.hasDetectOk
        if self.optimized and canEarlyBreak: # Early Break
            LeftClick(top_left, bottom_right)
            return

        self.hasDetectStorySkip, top_left, bottom_right = pattern.Detect(self.frame, pattern.storySkipPattern, 0.8)
        canEarlyBreak = self.hasDetectStorySkip
        if self.optimized and canEarlyBreak: # Early Break
            LeftClick(top_left, bottom_right)
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
