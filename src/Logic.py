from enum import Enum

import src.Pattern as Pattern
import src.utils as utils
from src.Control import Control
from src.State import State
from src.Routine import Routine
from src.Detection import Detection


class Routines(Enum):
    LOOP_SINGLE_LEVEL = 'LOOP LEVEL'
    LOOP_STAGE = 'LOOP STAGE'  # 第一次跑關卡時，跑通整個流程


class Logic(Routine):
    def __init__(self, routine, control, optimized=True):
        super().__init__("Main Logic", control, optimized)

        # Set Current Routine
        self.routine = routine

    def Reset(self, frame):
        super().Reset(frame)

        # Call Reset() to current routine
        self.routine.Reset(frame)

    def Update(self):
        super().Update()

        for name, template, threshold in Pattern.patterns:
            isExist, _, top_left, bottom_right = Pattern.Detect(
                self.frame, template, threshold)

            # Need Refactor
            self.routine.hasDetected[name] = Detection(
                name, isExist, top_left, bottom_right)

        # Call Update() to current routine
        self.routine.Update()

    def QueryState(self):
        super().QueryState()

        # Call QueryState() to current routine
        self.routine.QueryState()

    def StateAction(self):
        super().StateAction()

        # Call StateAction() to current routine
        self.routine.StateAction()

    def Process(self, frame):
        try:
            if self.routine.state != State.DONE:
                self.Reset(frame)
                self.Update()
                self.QueryState()
                self.StateAction()
                return False, None
            else:
                return True, None
        except Exception as e:
            # sometime setForegroundWindow may raise error
            utils.printErr(e)
            # pass the iteration instead.
            return False, e

    def GetMessage(self):
        return self.routine.GetMessage()

    def DealAction_Loop_SingleLevel(self, control):
        top_left, bottom_right = self.localPosition

        statesShouldAction = [
            State.REMATCH,
            State.NO_AP,
            State.OSOUJI_COMFIRM,
            State.OSOUJI_LEVEL_COMFIRM,
            State.OSOUJI_RESULT_COMFIRM,
            State.SELECT_EVENT,
            State.SELECT_STAGE,
            State.SELECT_LEVEL,
            State.HOME,
        ]

        if self.state in statesShouldAction:
            control.MouseLeftClick(top_left, bottom_right)
            if self.state == State.OSOUJI_RESULT_COMFIRM:
                time.sleep(5)
            else:
                time.sleep(2.5)
        elif self.state == State.OSOUJI:
            control.OsoujiPathSlides()
            time.sleep(1)
