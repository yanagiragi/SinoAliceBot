import time

from src.State import State
from src.Routine import Routine
from src.utils import SaveScreenshot


class Routine_Deemo2Daily(Routine):
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

        if self.hasDetected['deemo2 icon'].IsExist:
            if self.prevState == State.OS_CLOSE_ALL_TASKS:
                self.state = State.DONE
            else:
                self.state = State.OS_HOME
            currentDetected = self.hasDetected['deemo2 icon']

        elif self.hasDetected['close_all_tasks'].IsExist:
            self.state = State.OS_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['close_all_tasks']

        elif self.hasDetected['deemo2 confirm'].IsExist:
            self.state = State.DEEMO2_CONFRIM
            currentDetected = self.hasDetected['deemo2 confirm']

        elif self.hasDetected['deemo2 close'].IsExist:
            if self.hasDetected['deemo2 stampCard'].IsExist:
                self.state = State.DEEMO2_LOGIN_BONUS
            else:
                self.state = State.DEEMO2_CLOSE
            currentDetected = self.hasDetected['deemo2 close']

        elif self.hasDetected['deemo2 setting'].IsExist:
            self.state = State.DEEMO2_LOGO
            currentDetected = None
            self.localPosition = [(150, 150), (300, 300)]

        elif self.hasDetected['deemo2 echoFace'].IsExist:
            self.state = State.DEEMO2_HOME

        if self.prevState == State.DEEMO2_HOME and \
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
            State.DEEMO2_CONFRIM,
            State.DEEMO2_LOGIN_BONUS,
            State.DEEMO2_LOGO,
            State.DEEMO2_CLOSE
        ]

        if self.state in statesShouldAction:
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(3)

        elif self.state == State.DEEMO2_HOME:
            # press mission control button
            self.control.ReturnToHome()
            time.sleep(3)

        if self.state != self.prevState:
            SaveScreenshot(self.frame, f'D2-{self.state}')  # no unicode support! 

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'
