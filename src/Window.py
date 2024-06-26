import sys
import win32gui
import win32com.client
import win32con

from desktopmagic.screengrab_win32 import getRectAsImage


class Window:
    def __init__(self, name, factor='0.5'):
        self.name = name
        self.instance = win32gui.FindWindow(None, self.name)
        self.factor = factor
        self.foreground = None
        self.offsetX = 10
        self.offsetY = 31
        self.paddingX = 10
        self.paddingY = 10

    def SetForeground(self):
        self.foreground = win32gui.GetForegroundWindow()

        # https://stackoverflow.com/questions/14295337/win32gui-setactivewindow-error-the-specified-procedure-could-not-be-found
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.instance)

    def RestoreForeground(self):
        if self.foreground:
            win32gui.SetForegroundWindow(self.foreground)
        self.foreground = None

    def GetScreen(self):
        try:
            self.left, self.top, self.right, self.bot = win32gui.GetWindowRect(
                self.instance)
            self.img = getRectAsImage(
                (self.left, self.top, self.right, self.bot))

            # w, h = self.img.size
            # self.img = self.img.crop((offsetX, self.offsetY, w - self.paddingX, h - self.paddingY))

            self.size = (int((self.right - self.left) * self.factor),
                         int((self.bot - self.top) * self.factor))
            return self.img, None
        except:
            return None, sys.exc_info()

    def ResizeWindow(self, width, height=None):
        try:
            self.left, self.top, self.right, self.bot = win32gui.GetWindowRect(
                self.instance)
            if height is None:
                height = float(width) * 21.0 / 9.0
            win32gui.MoveWindow(self.instance, self.left,
                                self.top, int(width), int(height), True)
            return False, None
        except:
            return True, sys.exc_info()

    @staticmethod
    def GetAllWindows():
        hWndList = []
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
        return [win32gui.GetWindowText(hWnd) for hWnd in hWndList]

    @staticmethod
    def ListAllWindows():
        hWndList = []
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
        print([win32gui.GetWindowText(hWnd) for hWnd in hWndList])

    def Close(self):
        win32gui.PostMessage(self.instance, win32con.WM_CLOSE, 0, 0)


if __name__ == '__main__':
    Window.ListAllWindows()
