import time

from src.State import State
from src.Routine import Routine


class Routine_BlueArchiveDaily(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)

    def Reset(self, frame):
        pass

    def Update(self):
        pass

    def QueryState(self):
        super().QueryState()
        
        # self.state = State.IDLE
        currentDetected = None

        if self.hasDetected['blue_archive icon'].IsExist:
            if self.prevState == State.OS_CLOSE_ALL_TASKS:
                self.state = State.DONE
            else:
                self.state = State.OS_HOME
            currentDetected = self.hasDetected['blue_archive icon']

        elif self.hasDetected['close_all_tasks'].IsExist:
            self.state = State.OS_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['close_all_tasks']

        elif self.hasDetected['blue_archive rating'].IsExist:
            self.state = State.BLUE_ARCHIVE_TITLE
            currentDetected = self.hasDetected['blue_archive rating']

        elif self.hasDetected['blue_archive event block'].IsExist:
            self.state = State.BLUE_ARCHIVE_ADS
            currentDetected = self.hasDetected['blue_archive event block']

        elif self.hasDetected['blue_archive announcement'].IsExist:
            self.state = State.BLUE_ARCHIVE_HOME
            currentDetected = self.hasDetected['blue_archive announcement']

        if (self.prevState == State.BLUE_ARCHIVE_HOME) and \
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
            State.BLUE_ARCHIVE_APP_HOME,
            State.BLUE_ARCHIVE_TITLE
        ]

        if self.state in statesShouldAction:
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(3)

        elif self.state == State.BLUE_ARCHIVE_ADS:
            self.control.MouseLeftClick([848, 55], [848, 55])
            time.sleep(3)

        elif self.state == State.BLUE_ARCHIVE_HOME:
            # press mission control button
            self.control.ReturnToHome()
            time.sleep(3)

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'
