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

        """self.hasDetectGameplay, top_left, bottom_right = pattern.DetectGameplay(frame)
        canEarlyBreak = self.hasDetectGameplay
        if self.optimized and canEarlyBreak: # Early Break
            return"""

    def QueryState(self):

        # abstract state of flags
        isBattle = None

        self.state = state.IDLE
    
    def StateAction(self, control):
        [x for x in []]
            
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
