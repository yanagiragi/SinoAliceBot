import time

from src.State import State
from src.Routine import Routine
from src.utils import SaveScreenshot


class Routine_ProjectSekaiDaily(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)

    def Reset(self, frame):
        self.frame = frame
        pass

    def Update(self):
        pass

    def QueryState(self):
        super().QueryState()
    
        #self.state = State.IDLE
        currentDetected = None

        if self.hasDetected['project_sekai icon'].IsExist:
            if self.prevState == State.OS_CLOSE_ALL_TASKS:
                self.state = State.DONE
            else:
                self.state = State.OS_HOME
            currentDetected = self.hasDetected['project_sekai icon']

        elif self.hasDetected['close_all_tasks'].IsExist:
            self.state = State.OS_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['close_all_tasks']

        elif self.hasDetected['project_sekai logo'].IsExist:
            self.state = State.PROJECT_SEKAI_APP_HOME
            currentDetected = self.hasDetected['project_sekai logo']

        elif self.hasDetected['project_sekai live'].IsExist or \
                self.hasDetected['project_sekai info'].IsExist:
            self.state = State.PROJECT_SEKAI_HOME
            currentDetected = None

        elif self.hasDetected['project_sekai later'].IsExist:
            self.state = State.PROJECT_SEKAI_PLAY_LOGIN
            currentDetected = self.hasDetected['project_sekai later']
   
        elif self.hasDetected['project_sekai loginBonus'].IsExist:
            self.state = State.PROJECT_SEKAI_LOGIN_BONUS
            currentDetected = self.hasDetected['project_sekai skip']

        elif self.hasDetected['project_sekai skip'].IsExist:
            self.state = State.PROJECT_SEKAI_COMFIRM
            currentDetected = self.hasDetected['project_sekai skip']

        elif self.hasDetected['project_sekai download'].IsExist:
            self.state = State.PROJECT_SEKAI_DOWNLOAD
            currentDetected = self.hasDetected['project_sekai download']

        if self.prevState == State.PROJECT_SEKAI_HOME and \
                self.state == State.OS_HOME and \
                self.hasDetected['mission_control'].IsExist:
            self.state = State.OS_ABOUT_TO_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['mission_control']

        # update Local Position
        if currentDetected is not None:
            self.localPosition = currentDetected.LocalPosition

    def StateAction(self):
        super().StateAction()
        top_left, bottom_right = self.localPosition

        statesShouldAction = [
            State.OS_HOME,
            State.OS_CLOSE_ALL_TASKS,
            State.OS_ABOUT_TO_CLOSE_ALL_TASKS,
            State.PROJECT_SEKAI_APP_HOME,
            State.PROJECT_SEKAI_LOGIN_BONUS,
            State.PROJECT_SEKAI_COMFIRM,
            State.PROJECT_SEKAI_DOWNLOAD,
            State.PROJECT_SEKAI_PLAY_LOGIN
        ]

        if self.state in statesShouldAction:
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(3)
        
        elif self.state == State.PROJECT_SEKAI_HOME:
            # press mission control button
            self.control.ReturnToHome()
            time.sleep(3)

        if self.state != self.prevState:
            SaveScreenshot(self.frame, f'-PS-{self.state}') # no unicode support!
        

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'
