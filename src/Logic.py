
import src.Pattern as Pattern
import src.utils as utils
from src.State import State
from src.Routine import Routine
from src.Detection import Detection

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
            # sometime setForegroundWindow may raise error, pass the iteration instead.
            utils.printErr(e)
            return False, e

    def GetMessage(self):
        return self.routine.GetMessage()
