import sys
import cv2
import win32gui
import numpy as np

from desktopmagic.screengrab_win32 import getRectAsImage

class WindowScreen:
    def __init__(self, name='KurtzPel:混沌的使者  ', factor='0.5'):
        self.name = name
        self.instance = win32gui.FindWindow(None, self.name)
        self.factor = factor
        self.foreground = None

    def SetForeground(self):
        self.foreground = win32gui.GetForegroundWindow()
        win32gui.SetForegroundWindow(self.instance)

    def RestoreForeground(self):
        if self.foreground:
            win32gui.SetForegroundWindow(self.foreground)
        self.foreground = None

    def GetScreen(self):
        try :
            self.left, self.top, self.right, self.bot = win32gui.GetWindowRect(self.instance)
            self.img = getRectAsImage((self.left, self.top, self.right, self.bot))
            self.size = (int((self.right - self.left) * self.factor), int((self.bot - self.top) * self.factor))
            return self.img, None
        except :
            return None, sys.exc_info()

    def ResizeWindow(self, width, height = None):
        try :
            self.left, self.top, self.right, self.bot = win32gui.GetWindowRect(self.instance)
            if height is None:
                height = float(width) * 21.0 / 9.0
            win32gui.MoveWindow(self.instance, self.left, self.top, int(width), int(height), True)
            return False, None
        except :
            return True, sys.exc_info()
    
    @staticmethod
    def ListAllWindows():
        hWndList = []
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
        print([win32gui.GetWindowText(hWnd) for hWnd in hWndList])
    
if __name__ == '__main__':
    WindowScreen.ListAllWindows()