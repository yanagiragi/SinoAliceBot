import win32api
import win32con
import win32gui
import time

from src.IControl import IControl

VK_CODE = {'backspace': 0x08,
           'tab': 0x09,
           'clear': 0x0C,
           'enter': 0x0D,
           'shift': 0x10,
           'ctrl': 0x11,
           'alt': 0x12,
           'pause': 0x13,
           'caps_lock': 0x14,
           'esc': 0x1B,
           'spacebar': 0x20,
           'page_up': 0x21,
           'page_down': 0x22,
           'end': 0x23,
           'home': 0x24,
           'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
           'select': 0x29,
           'print': 0x2A,
           'execute': 0x2B,
           'print_screen': 0x2C,
           'ins': 0x2D,
           'del': 0x2E,
           'help': 0x2F,
           '0': 0x30,
           '1': 0x31,
           '2': 0x32,
           '3': 0x33,
           '4': 0x34,
           '5': 0x35,
           '6': 0x36,
           '7': 0x37,
           '8': 0x38,
           '9': 0x39,
           'a': 0x41,
           'b': 0x42,
           'c': 0x43,
           'd': 0x44,
           'e': 0x45,
           'f': 0x46,
           'g': 0x47,
           'h': 0x48,
           'i': 0x49,
           'j': 0x4A,
           'k': 0x4B,
           'l': 0x4C,
           'm': 0x4D,
           'n': 0x4E,
           'o': 0x4F,
           'p': 0x50,
           'q': 0x51,
           'r': 0x52,
           's': 0x53,
           't': 0x54,
           'u': 0x55,
           'v': 0x56,
           'w': 0x57,
           'x': 0x58,
           'y': 0x59,
           'z': 0x5A,
           'numpad_0': 0x60,
           'numpad_1': 0x61,
           'numpad_2': 0x62,
           'numpad_3': 0x63,
           'numpad_4': 0x64,
           'numpad_5': 0x65,
           'numpad_6': 0x66,
           'numpad_7': 0x67,
           'numpad_8': 0x68,
           'numpad_9': 0x69,
           'multiply_key': 0x6A,
           'add_key': 0x6B,
           'separator_key': 0x6C,
           'subtract_key': 0x6D,
           'decimal_key': 0x6E,
           'divide_key': 0x6F,
           'F1': 0x70,
           'F2': 0x71,
           'F3': 0x72,
           'F4': 0x73,
           'F5': 0x74,
           'F6': 0x75,
           'F7': 0x76,
           'F8': 0x77,
           'F9': 0x78,
           'F10': 0x79,
           'F11': 0x7A,
           'F12': 0x7B,
           'F13': 0x7C,
           'F14': 0x7D,
           'F15': 0x7E,
           'F16': 0x7F,
           'F17': 0x80,
           'F18': 0x81,
           'F19': 0x82,
           'F20': 0x83,
           'F21': 0x84,
           'F22': 0x85,
           'F23': 0x86,
           'F24': 0x87,
           'num_lock': 0x90,
           'scroll_lock': 0x91,
           'left_shift': 0xA0,
           'right_shift ': 0xA1,
           'left_control': 0xA2,
           'right_control': 0xA3,
           'left_menu': 0xA4,
           'right_menu': 0xA5,
           'browser_back': 0xA6,
           'browser_forward': 0xA7,
           'browser_refresh': 0xA8,
           'browser_stop': 0xA9,
           'browser_search': 0xAA,
           'browser_favorites': 0xAB,
           'browser_start_and_home': 0xAC,
           'volume_mute': 0xAD,
           'volume_Down': 0xAE,
           'volume_up': 0xAF,
           'next_track': 0xB0,
           'previous_track': 0xB1,
           'stop_media': 0xB2,
           'play/pause_media': 0xB3,
           'start_mail': 0xB4,
           'select_media': 0xB5,
           'start_application_1': 0xB6,
           'start_application_2': 0xB7,
           'attn_key': 0xF6,
           'crsel_key': 0xF7,
           'exsel_key': 0xF8,
           'play_key': 0xFA,
           'zoom_key': 0xFB,
           'clear_key': 0xFE,
           '+': 0xBB,
           ',': 0xBC,
           '-': 0xBD,
           '.': 0xBE,
           '/': 0xBF,
           '`': 0xC0,
           ';': 0xBA,
           '[': 0xDB,
           '\\': 0xDC,
           ']': 0xDD,
           "'": 0xDE,
           '`': 0xC0}


class Control(IControl):
    def __init__(self, window, resolution):
        self.top = 0
        self.left = 0
        self.size = 0
        self.window = window
        self.delay = 0.05
        self.resolution = resolution

        # Tick Setting
        self.width_step = 84 - 38
        self.height_step = 581 - 552
        self.startPos = [175, 531]
        self.startYear = 2020
        self.startMonth = 6
        self.startDate = 3
        self.currentPos = [self.startPos[0], self.startPos[1]]
        self.isPassMonth = False
        self.tickIdx = 0
        self.isDate = True

    def Update(self, top, left, bottom, right):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def CheckMousePosition(self, localPosition):
        x, y = localPosition
        if x < 0 or x > self.right:
            print(localPosition)
            raise RuntimeError
        elif y < 0 or y > self.bottom:
            raise RuntimeError

    def MouseMove(self, localPosition):
        self.window.SetForeground()
        self.CheckMousePosition(localPosition)
        globalPosition = [sum(x) for x in zip(
            localPosition, (self.left, self.top))]
        win32api.SetCursorPos(globalPosition)
        time.sleep(self.delay)

    # easier wrapper
    def MouseLeftClick(self, top_left, bottom_right):
        # click center
        localPosition = [int((top_left[0] + bottom_right[0])/2),
                         int((top_left[1] + bottom_right[1])/2)]
        self.MouseLeftClick_Impl(localPosition)
        # self.MouseMove([0,0])

    def MouseLeftClick_Impl(self, localPosition):
        self.MouseMove(localPosition)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        self.MouseLeftButtonDown()
        self.MouseLeftButtonUp()
        self.window.RestoreForeground()

    def MouseRightClick(self, localPosition):
        self.MouseMove(localPosition)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP |
                             win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        self.window.RestoreForeground()

    def KeyPress(self, arg):
        self.window.SetForeground()
        win32api.keybd_event(VK_CODE[arg], 0, 0, 0)
        time.sleep(self.delay)
        win32api.keybd_event(VK_CODE[arg], 0, win32con.KEYEVENTF_KEYUP, 0)
        self.window.RestoreForeground()

    def MouseLeftButtonDown(self, delay=0.1):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(delay)

    def MouseLeftButtonUp(self, delay=0.1):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(delay)

    def MouseMiddleClick(self, localPosition):
        self.MouseMove(localPosition)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
        time.sleep(self.delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
        time.sleep(self.delay)
        self.window.RestoreForeground()

    def SwipeUp(self, startLocalPosition, endLocalPosition, delay=0.05):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        startY = float(startLocalPosition[1])  # bottom_right y
        endY = float(endLocalPosition[1])  # bottom_right y
        currentY = endY

        while startY < currentY:
            currentY -= 10
            self.MouseMove([startLocalPosition[0], int(currentY)])
            time.sleep(delay)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.1)
        self.window.RestoreForeground()

    def SwipeDown(self, startLocalPosition, endLocalPosition, delay=0.05):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        startY = float(startLocalPosition[1])  # bottom_right y
        endY = float(endLocalPosition[1])  # bottom_right y
        currentY = startY

        while endY > currentY:
            currentY += 10
            self.MouseMove([startLocalPosition[0], int(currentY)])
            time.sleep(delay)

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.1)
        self.window.RestoreForeground()

    def OsoujiPathSlides(self, delay=0.05):
        center_1366 = [177, 356]
        osoujiPaths_1366 = [[198, 286], [267, 343], [265, 435], [
            246, 526], [166, 518], [86, 474], [75, 385], [126, 300]]

        center_1920 = [247, 463]
        osoujiPaths_1920 = [
            [164, 358],
            [271, 353],
            [380, 455],
            [388, 564],
            [343, 712],
            [239, 705],
            [122, 632],
            [96, 490],
        ]

        osoujiPaths = osoujiPaths_1920 if self.resolution == '1920x1080' else osoujiPaths_1366
        center = center_1920 if self.resolution == '1920x1080' else center_1366

        # Click first
        self.MouseMove(center)
        self.MouseLeftButtonDown(delay)
        self.MouseLeftButtonUp(delay)

        # Then loop the paths
        self.MouseMove(osoujiPaths[0])
        self.MouseLeftButtonDown(delay)
        for osoujiPath in osoujiPaths:
            self.MouseMove(osoujiPath)
            time.sleep(delay)
        self.MouseLeftButtonUp(delay)

        time.sleep(1)

    def ReturnToHome(self):
        self.window.SetForeground()
        self.MouseMiddleClick([50, 50])
        self.window.RestoreForeground()