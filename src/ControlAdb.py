import win32api, win32con, win32gui, time

from src.IControl import IControl
from src.Control import Control
import subprocess

class ControlAdb(IControl):
    def __init__(self, window):
        self.control = Control(window)
        self.factor = 4.11

    def Update(self, top, left, bottom, right):
        pass

    # transform fixedCoordinate to physical device coordinate
    def TransformCoordinate(self, fixedCoordinate):        
        return [fixedCoordinate[0] * self.factor, fixedCoordinate[1] * self.factor]

    def Tap(self, position):
        subprocess.Popen(f"adb shell input tap {position[0]} {position[1]}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    # args.length must = 4 to properly work
    def Swipe(self, *args):
        cmd = f"adb shell input swipe "
        if len(args) > 0:
            for arg in args:
                cmd += f"{int(arg[0])} {int(arg[1])} "
        subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    def MouseLeftClick(self, top_left, bottom_right):
        localPosition = [int((top_left[0] + bottom_right[0])/2), int((top_left[1] + bottom_right[1])/2)] # click on center
        localPosition = self.TransformCoordinate(localPosition)
        self.Tap(localPosition)
    
    def SwipeUp(self, abovePosition, belowPosition, delay=0.05):
        self.Swipe(startLocalPosition, endLocalPosition)
        pass

    def SwipeDown(self, abovePosition, belowPosition, delay=0.05):        
        self.Swipe(belowPosition, abovePosition)

    def OsoujiPathSlides(self, delay=0.05):
        center = [177, 356]
        osoujiPaths = [[198, 286], [267, 343], [265, 435], [246, 526], [166, 518], [86, 474], [75, 385], [126, 300], [198, 286]]

        # Click first
        self.Tap(self.TransformCoordinate(center))

        # Then loop the paths
        transformedOsoujiPaths = []
        """for osoujiPath in osoujiPaths:
            transformedOsoujiPaths.append(self.TransformCoordinate(osoujiPath))
            if len(transformedOsoujiPaths) == 2:
                self.Swipe(*transformedOsoujiPaths)
                transformedOsoujiPaths[0] = transformedOsoujiPaths[1]
                del transformedOsoujiPaths[1]
                time.sleep(0.2)"""
        
        # Faster Solution
        for osoujiPath in osoujiPaths:
            self.Tap(self.TransformCoordinate(osoujiPath))
            time.sleep(0.2)

        pass