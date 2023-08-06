import time

from src.State import State
from src.Routine import Routine
from src.utils import SaveScreenshot
import src.Pattern as Pattern


class Routine_BlueArchiveDaily(Routine):
    def __init__(self, name, control, optimized=True):
        super().__init__(name, control, optimized)

    def Reset(self, frame):
        self.frame = frame
        pass

    def Update(self):
        pass

    def GetPatterns(self):
        return filter(lambda pattern: pattern[0].startswith('blue_archive ') or pattern[0].startswith('os '), Pattern.patterns)

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

        elif self.hasDetected['blue_archive daily login reward'].IsExist:
            self.state = State.BLUE_ARCHIVE_LOGIN_BONUS
            currentDetected = self.hasDetected['blue_archive daily login reward']

        elif self.hasDetected['blue_archive additional login reward'].IsExist:
            self.state = State.BLUE_ARCHIVE_ADDITIONAL_LOGIN_BOUNS
            currentDetected = self.hasDetected['blue_archive additional login reward']

        elif self.hasDetected['blue_archive close'].IsExist:
            self.state = State.BLUE_ARCHIVE_ANNOUNCEMENT
            currentDetected = self.hasDetected['blue_archive close']

        elif self.hasDetected['os close_all_tasks'].IsExist:
            self.state = State.OS_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['os close_all_tasks']

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
                self.hasDetected['os mission_control'].IsExist:
            self.state = State.OS_ABOUT_TO_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['os mission_control']

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
            State.BLUE_ARCHIVE_TITLE,
            State.BLUE_ARCHIVE_LOGIN_BONUS,
            State.BLUE_ARCHIVE_ADDITIONAL_LOGIN_BOUNS,
            State.BLUE_ARCHIVE_ANNOUNCEMENT
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

        if self.state != self.prevState:
            SaveScreenshot(self.frame, f'BA-{self.state}')  # no unicode support!

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'
