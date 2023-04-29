import time

from src.State import State
from src.Routine import Routine
from src.utils import SaveScreenshot


class Routine_HeavenBurnsRedDaily(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)

    def Reset(self, frame):
        self.frame = frame
        pass

    def Update(self):
        pass

    def QueryState(self):
        super().QueryState()
    
        self.state = State.IDLE
        currentDetected = None

        if self.hasDetected['heaven_burns_red icon'].IsExist:
            if self.prevState == State.OS_CLOSE_ALL_TASKS:
                self.state = State.DONE
            else:
                self.state = State.OS_HOME
            currentDetected = self.hasDetected['heaven_burns_red icon']

        elif self.hasDetected['close_all_tasks'].IsExist:
            self.state = State.OS_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['close_all_tasks']

        elif self.hasDetected['heaven_burns_red inherit'].IsExist:
            self.state = State.HEAVEN_BURNS_RED_INHERIT
            currentDetected = self.hasDetected['heaven_burns_red inherit']

        elif self.hasDetected['heaven_burns_red battleResult'].IsExist or \
                self.hasDetected['heaven_burns_red okaeri'].IsExist or \
                self.hasDetected['heaven_burns_red home'].IsExist or \
                self.hasDetected['heaven_burns_red arena'].IsExist or \
                self.hasDetected['heaven_burns_red menu'].IsExist:
            self.state = State.HEAVEN_BURNS_RED_HOME
            currentDetected = None
   
        elif self.hasDetected['heaven_burns_red loginBonus'].IsExist:
            self.state = State.HEAVEN_BURNS_RED_LOGIN_BONUS
            currentDetected = self.hasDetected['heaven_burns_red loginBonus']

        elif self.hasDetected['heaven_burns_red ok'].IsExist:
            self.state = State.HEAVEN_BURNS_RED_COMFIRM
            currentDetected = self.hasDetected['heaven_burns_red ok']

        elif self.hasDetected['heaven_burns_red skip'].IsExist:
            self.state = State.HEAVEN_BURNS_RED_COMFIRM
            currentDetected = self.hasDetected['heaven_burns_red skip']

        elif self.hasDetected['heaven_burns_red downloadAll'].IsExist:
            self.state = State.HEAVEN_BURNS_RED_DOWNLOAD
            currentDetected = self.hasDetected['heaven_burns_red downloadAll']

        elif self.hasDetected['heaven_burns_red criware'].IsExist:
            self.state = State.HEAVEN_BURNS_RED_APP_HOME
            currentDetected = self.hasDetected['heaven_burns_red criware']

        if self.prevState == State.HEAVEN_BURNS_RED_HOME and \
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
            State.HEAVEN_BURNS_RED_LOGIN_BONUS,
            State.HEAVEN_BURNS_RED_COMFIRM,
            State.HEAVEN_BURNS_RED_SKIP,
            State.HEAVEN_BURNS_RED_DOWNLOAD,
            State.HEAVEN_BURNS_RED_APP_HOME,
            State.HEAVEN_BURNS_RED_INHERIT,
        ]

        if self.state in statesShouldAction:
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(3)
        
        elif self.state == State.HEAVEN_BURNS_RED_HOME:
            # press mission control button
            self.control.ReturnToHome()
            time.sleep(3)

        if self.state != self.prevState:
            SaveScreenshot(self.frame, f'-HBR-{self.state}') # no unicode support!
        

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'
