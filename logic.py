import pattern as Pattern
from enum import Enum

from control import *

class state(Enum):
    IDLE = 'idle'    
    BATTLE = 'BATTLE'
    REMATCH = 'rematch'
    NEXT = '次へ'
    NO_AP = 'AP 回復 確認'
    OSOUJI = 'お掃除'
    OSOUJI_COMFIRM = 'お掃除 確認'
    OSOUJI_RESULT_COMFIRM = 'お掃除 結果確認'
    HOME = 'ホームページ'
    SELECT_EVENT = '物語 選択'
    SELECT_STAGE = 'イベント 選択'
    SELECT_LEVEL = '章 選択'
    OSOUJI_LEVEL_COMFIRM = 'お掃除 確認 (体力不足)'
    SELECT_LEVEL_CONFIRM = '章 確認'
    STORY_SKIP = 'STORY SKIP'
    STAGE_LOOP_END = 'Stage loop end'
    STAGE_NORMAL_IDLE = 'STAGE_NORMAL_IDLE'
    STAGE_HARD_IDLE = 'STAGE_HARD_IDLE'
    DONE = '完了'

class Routine(Enum):
    LOOP_SINGLE_LEVEL = 'LOOP LEVEL'
    LOOP_STAGE = 'LOOP STAGE' # 第一次跑關卡時，跑通整個流程

class Logic:
    def __init__(self, optimized=True):
        
        # For Debug mode
        self.state = state.OSOUJI

        self.routine = Routine.LOOP_STAGE

        self.prevLevel = 1

        self.prevState = state.IDLE
        self.state = state.IDLE
        self.optimized = optimized        
        self.localPosition = [[0, 0], [0, 0]]
    
    def Reset(self, frame):     
        self.frame = frame   

    def Update(self):
        frame = self.frame
        self.hasDetected = {}
        for name, _pattern, threshold in Pattern.patterns:
            isExist, top_left, bottom_right = Pattern.Detect(frame, _pattern, threshold)
            self.hasDetected[name] = { "isExist": isExist, "localPosition": [top_left, bottom_right] }

    def DeterminPrevStage(self):
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
            if check['isExist']:
                currentDetected = check
                self.prevLevel = (idx + 1)
        
        if currentDetected is not None:
            self.localPosition = currentDetected['localPosition']
            self.state = state.SELECT_LEVEL
            if self.prevState == state.STAGE_LOOP_END:
                self.state = state.DONE

        return currentDetected

    def Routine_Loop_Stage(self):
        currentDetected = None

        if self.hasDetected['hard']['isExist'] or self.hasDetected['normal']['isExist']:
            hardLocationY = self.hasDetected['hard']['localPosition'][0][1] # y coordinate of left top corner
            normalLocationY = self.hasDetected['normal']['localPosition'][0][1]            
            if hardLocationY > normalLocationY: # hard button is below
                currentDetected = self.hasDetected['hard']
                self.state = state.STAGE_NORMAL_IDLE
            else:
                currentDetected = self.hasDetected['normal']
                self.state = state.STAGE_HARD_IDLE
                if self.prevState == state.STAGE_LOOP_END:
                    self.state = state.DONE

        elif self.hasDetected['next']['isExist']:
            currentDetected = self.hasDetected['next']
            self.state = state.NEXT

        elif self.hasDetected['storySkip']['isExist']:
            currentDetected = self.hasDetected['storySkip']
            self.state = state.STORY_SKIP
        
        elif self.hasDetected['osoujiText']['isExist']:
            currentDetected = self.hasDetected['osoujiText']
            self.state = state.NO_AP

        elif self.hasDetected['ok']['isExist']:
            currentDetected = self.hasDetected['ok']
            if self.hasDetected['rematch']['isExist']:
                self.state = state.STAGE_LOOP_END
            elif self.hasDetected['rematch']['isExist'] == False and self.hasDetected['next']['isExist'] == False:
                self.state = state.STAGE_LOOP_END
            elif self.prevState == state.IDLE or self.prevState == state.BATTLE:
                self.state = state.SELECT_LEVEL_CONFIRM
            elif self.prevState == state.NO_AP:
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
        
        # Has enter next level, increase prevLevel
        if self.state == state.BATTLE and self.prevState == state.NEXT:
            self.prevLevel += 1

        if currentDetected is not None:
            self.localPosition = currentDetected['localPosition']

        self.DeterminPrevStage()

    def Routine_Loop_SingleLevel(self):
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

    def QueryState(self):        
        if self.state != self.prevState:
            self.prevState = self.state

        if self.routine == Routine.LOOP_STAGE:
            self.Routine_Loop_Stage()
           
        elif self.routine == Routine.LOOP_SINGLE_LEVEL:
            self.Routine_Loop_SingleLevel()

        else:
            self.state = state.IDLE

    def DealAction_Loop_Stage(self, control):
        top_left, bottom_right = self.localPosition

        statesShouldAction = [
            # state.REMATCH, # No Rematch
            state.NO_AP,
            state.OSOUJI_COMFIRM,
            state.OSOUJI_LEVEL_COMFIRM,
            state.OSOUJI_RESULT_COMFIRM,
            state.SELECT_EVENT,
            state.SELECT_STAGE,
            state.SELECT_LEVEL,
            state.SELECT_LEVEL_CONFIRM,
            state.HOME,
            state.STORY_SKIP,
            state.NEXT,
            state.STAGE_LOOP_END,
            state.STAGE_NORMAL_IDLE,
        ]

        if self.state in statesShouldAction:            
            control.MouseLeftClick(top_left, bottom_right)
            
            # Special delays for certain states
            if self.state == state.OSOUJI_RESULT_COMFIRM:
                time.sleep(5)
            elif self.state == state.STAGE_LOOP_END:
                time.sleep(5)
            else:
                time.sleep(2.5)

        elif self.state == state.OSOUJI:
            control.OsoujiPathSlides()
            time.sleep(1)

    def DealAction_Loop_SingleLevel(self, control):
        top_left, bottom_right = self.localPosition

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
        ]

        if self.state in statesShouldAction:            
            control.MouseLeftClick(top_left, bottom_right)
            if self.state == state.OSOUJI_RESULT_COMFIRM:
                time.sleep(5)
            else:
                time.sleep(2.5)
        elif self.state == state.OSOUJI:
            control.OsoujiPathSlides()
            time.sleep(1)
        
    def StateAction(self, control):        
        if self.routine == Routine.LOOP_STAGE:
            self.DealAction_Loop_Stage(control)           

        elif self.routine == Routine.LOOP_SINGLE_LEVEL:
            self.DealAction_Loop_SingleLevel()
 
    def Process(self, frame, control):
        try:
            if self.state != state.DONE:
                self.Reset(frame)
                self.Update()
                self.QueryState()
                self.StateAction(control)
                return False, None
            else:
                return True, None
        except Exception as e:
            # sometime setForegroundWindow may raise error
            # pass the iteration instead.
            return False, e
