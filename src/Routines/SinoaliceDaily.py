import time

from src.State import State
from src.Routine import Routine
from src.utils import SaveScreenshot


class Routine_SinoaliceDaily(Routine):
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

        if self.hasDetected['sinoalice icon'].IsExist:
            if self.prevState == State.OS_CLOSE_ALL_TASKS:
                self.state = State.DONE
            else:
                self.state = State.OS_HOME
            currentDetected = self.hasDetected['sinoalice icon']

        elif self.hasDetected['close_all_tasks'].IsExist:
            self.state = State.OS_CLOSE_ALL_TASKS
            currentDetected = self.hasDetected['close_all_tasks']

        elif self.hasDetected['sinoalice logo'].IsExist:
            self.state = State.SINOALICE_LOGO
            currentDetected = self.hasDetected['sinoalice logo']

        elif self.hasDetected['sinoalice cancel'].IsExist:
            self.state = State.SINOALICE_CANCEL
            currentDetected = self.hasDetected['sinoalice cancel']

        elif self.hasDetected['sinoalice close'].IsExist:
            self.state = State.SINOALICE_CLOSE
            currentDetected = self.hasDetected['sinoalice close']

        elif self.hasDetected['sinoalice sent_to_box'].IsExist:
            self.state = State.SINOALICE_RECEIVE_REWARD
            currentDetected = None
   
        elif self.hasDetected['sinoalice mission_logo'].IsExist:
            if self.hasDetected['sinoalice daily'].IsExist:
                self.state = State.SINOALICE_MISSION_MAIN
                currentDetected = self.hasDetected['sinoalice daily']
            elif self.hasDetected['sinoalice daily_no'].IsExist:
                self.state = State.SINOALICE_MISSION_DAILY_NO_REWARD
                currentDetected = self.hasDetected['sinoalice daily_no']
            elif self.hasDetected['sinoalice get_all'].IsExist:
                self.state = State.SINOALICE_MISSION_DAILY
                currentDetected = self.hasDetected['sinoalice get_all']

        elif self.hasDetected['sinoalice mission'].IsExist:
            self.state = State.SINOALICE_HOME
            currentDetected = self.hasDetected['sinoalice mission']

        if (self.prevState == State.SINOALICE_RECEIVE_REWARD or \
                self.prevState == State.SINOALICE_MISSION_DAILY_NO_REWARD) and \
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
            State.SINOALICE_LOGO,
            State.SINOALICE_CANCEL,
            State.SINOALICE_CLOSE,
            State.SINOALICE_MISSION_MAIN,
            State.SINOALICE_MISSION_DAILY,
            State.SINOALICE_HOME,
        ]

        if self.state in statesShouldAction:
            self.control.MouseLeftClick(top_left, bottom_right)
            time.sleep(3)
        
        elif self.state == State.SINOALICE_RECEIVE_REWARD or \
                self.state == State.SINOALICE_MISSION_DAILY_NO_REWARD:
            # press mission control button
            self.control.ReturnToHome()
            time.sleep(3)

        if self.state != self.prevState:
            SaveScreenshot(self.frame, f'SA-{self.state}') # no unicode support!

    def GetMessage(self):
        return super().GetMessage() + f', state = {self.state.value}'
