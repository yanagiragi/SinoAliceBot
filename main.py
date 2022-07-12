import os
import sys
import signal
import time
import logging
import datetime
import keyboard
import argparse
import cv2
from multiprocessing import Process, freeze_support
from win10toast import ToastNotifier

import src.Pattern as Pattern
from src.Control import Control
from src.ControlAdb import ControlAdb
from src.Logic import Logic
from src.LoopLevelByName import Routine_LoopLevelByName
from src.LoopStage import Routine_LoopStage
from src.StartSinoalice import Routine_StartSinoalice
from src.GuildCoop import Routine_GuildCoop
from src.GuildStory import Routine_GuildStory
from src.Guild import Routine_Guild
from src.Window import Window
import src.utils as utils

#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# Const settings
isDebug = True
isPc = True

resizeFactor = 1.0  # scale factor of the screenshot of the window
debugWindowScaleFactor = 1  # scale factor of the debug window

toastDuration = 2
toastIcon = 'Resources/icon/icon.ico'

dmmTitle = 'Myゲーム - DMM GAME PLAYER'
windowsName = 'SINoALICE'  # 'SM-G955F'

ApplicationName = 'SinoBot'
ConenctionExecutor = 'D:/_Programs/Programs/_Shortcuts/scrcpy-win64-v1.14/scrcpy.exe --window-height 720 --window-borderless -w'

# Global variable
shallQuit = False
shallPause = False
toaster = None  # initialized after __init__ == "__main__"


def OnKeyPress(event):
    global shallQuit, shallPause, toaster
    if event.event_type == 'up':
        return
    if event.name == 'f9':
        shallPause = not shallPause
        if shallPause == True:
            toaster.show_toast(ApplicationName, "Paused",
                               duration=toastDuration, icon_path=toastIcon)
        else:
            toaster.show_toast(ApplicationName, "Resumed",
                               duration=toastDuration, icon_path=toastIcon)

    elif event.name == 'f10':
        toaster.show_toast(ApplicationName, "Exited",
                           duration=toastDuration, icon_path=toastIcon)
        shallQuit = True
        shallPause = True


def SetupLogger():
    if not os.path.exists('log'):
        os.makedirs('log')

    log_filename = datetime.datetime.now().strftime("log/%Y-%m-%d_%H_%M_%S.log")
    print('Logging File: {}'.format(log_filename))
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M:%S', handlers=[logging.FileHandler(log_filename, 'w', 'utf-8')])


def Cleanup(frame=None):
    print("\nClose.")
    if keywatchProcess.is_alive:
        keywatchProcess.terminate()
    cv2.destroyAllWindows()
    if frame is not None:
        cv2.imwrite('screenshot.png', frame)


def SigCleanup(sig, frame):
    Cleanup()
    sys.exit(0)


def SetupParser():
    parser = argparse.ArgumentParser(
        description='SinoBot, Based On Python3.7.2 (32 Bit)')
    parser.add_argument('--debug', default='false', help='enable debug mode')
    parser.add_argument('--routine', help='routine schema')
    parser.add_argument('--target', help='level to loop')
    parser.add_argument('--count', default=0, help='level to loop')
    return parser.parse_args()


"""
    Select Your Main Routine:
    Routine_LoopLevelByImage: Loop Single Level (matched with Resource/Stage/level.PNG), won't terminate
    Routine_LoopStage: Explore All levels (normal & hard) in a stage, terminates if all levels are looped
"""


def SelectRoutine(targetRoutine, control, targetLevel=None, targetCount=None):
    if targetRoutine == 'Loop_Stage':
        return Routine_LoopStage('Routine.Loop_Stage', control, False)
    elif targetRoutine == 'Loop_Level_By_Image':
        return Routine_LoopLevelByImage('Routine.Loop_Level_By_Image', control, False)
    elif targetRoutine == 'Loop_Level_By_Name':
        return Routine_LoopLevelByName('Routine.Loop_Level_By_Name', control, targetLevel, targetCount, False)
    elif targetRoutine == 'Guild_Coop':
        return Routine_GuildCoop('Routine.Guild_Coop', control, False)
    elif targetRoutine == 'Guild_Story':
        return Routine_GuildStory('Routine.Guild_Story', control, False)
    elif targetRoutine == 'Guild':
        return Routine_Guild('Routine.Guild', control, False)
    return None


def OpenSinoalice():
    window = Window(dmmTitle, resizeFactor)
    control = Control(window)
    routine = Routine_StartSinoalice('Routine.StartSinoalice', control)
    logic = Logic(routine, control)  # Create Main Logic
    window.SetForeground()

    toaster.show_toast(ApplicationName, "OpenSinoalice", duration=toastDuration,
                       icon_path=toastIcon)  # Show Notifcation

    while shallQuit == False:
        try:
            shallQuit = Tick(window, logic, control)
        except Exception as e:
            logging.exception(e)
            window.Close()


"""
Returns shall quit or not
"""


def Tick(window, logic, control) -> bool:

    if shallPause == True:
        return False

    elif shallQuit == True:
        return True

    tStart = time.time()  # Start Recording

    img, error = window.GetScreen()
    if img == None:
        print('Window "{}" Not Found, raw = {}'.format(window.name, error))
        return True

    img, frame = utils.LoadScreen(img)  # Get ScreenShot of img
    # img, frame = img[58:-10, 10:-10], frame[58:-10, 10:-10] # slice out window title
    # img, frame = utils.LoadScreenFromImage('test.jpg') # debug

    # update internal position of control instance
    control.Update(window.top, window.left, window.bot, window.right)

    isDone, logicError = logic.Process(frame)  # Procress Main Logic
    # isDone, logicError = False, None  # Freeze Logic for Debugging

    if isDone == True:
        print("Done All Tasks! Leaving ...")
        return True

    elif logicError:
        print(logicError)
        logging.error(logicError)

    tEnd = time.time()  # End Recording
    deltaTime = (tEnd - tStart)
    fps = 1.0 / deltaTime
    outputStr = '[{}] FPS = {:2.2f}'.format(time.strftime(
        '%Y/%m/%d %H:%M:%S'), fps) + logic.GetMessage()

    if isDebug:
        img = Pattern.DebugDraw(img, frame, logic)
        displayWindowsName = f'{windowsName} (Debug Mode)'
        cv2.namedWindow(displayWindowsName, 0)
        _w, _h = window.size
        cv2.resizeWindow(displayWindowsName, _w //
                         debugWindowScaleFactor, _h // debugWindowScaleFactor)
        cv2.imshow(displayWindowsName, img)

        outputStr += Pattern.existsPatternString  # Call after Pattern.DebugDraw()

        if cv2.waitKey(30) == ord('q'):
            # for visual apperance, re-print last output to avoid clear by 'Leaving ...'
            print(outputStr, end='\n')
            print('Leaving ...')
            Cleanup()
            return True

    # if isDebug or logic.prevState != logic.state:
    #    logging.info(outputStr)
    logging.info(outputStr)

    # output to console, currently only works with utf-8 console
    try:
        print(outputStr, end='\n')
    except Exception as e:
        print(outputStr.encoding('utf-8'), end='\n')
    finally:
        return False


def MainLoop():
    global shallQuit

    window = Window(windowsName, resizeFactor)
    control = Control(window)  # Create controll instance
    # control = ControlAdb(window) # Create controll instance
    routine = SelectRoutine(targetRoutine, control, targetLevel, targetCount)
    logic = Logic(routine, control)  # Create Main Logic

    patternPrefix = "PC" if isPc else "Android"
    patternPrefix = f'{patternPrefix}/1920x1080'
    Pattern.patterns = Pattern.LoadPatterns(patternPrefix)

    window.SetForeground()

    toaster.show_toast(ApplicationName, "Start", duration=toastDuration,
                       icon_path=toastIcon)  # Show Notifcation

    while not shallQuit:
        shallQuit = Tick(window, logic, control)

    # window.Close()


def Main():
    try:
        MainLoop()
    except Exception as e:
        utils.printErr(e)
        logging.exception(e)
    finally:
        Cleanup()


if __name__ == '__main__':

    freeze_support()

    toaster = ToastNotifier()  # Setup Toast Notification

    # Hook hotkey
    signal.signal(signal.SIGINT, SigCleanup)
    keyboard.hook(OnKeyPress)
    keywatchProcess = Process(target=keyboard.wait)
    keywatchProcess.start()

    # Setup Parser
    args = SetupParser()
    isDebug = args.debug == 'true'
    targetLevel = args.target
    targetRoutine = args.routine
    targetCount = int(args.count)

    SetupLogger()  # Setup Logger

    if targetRoutine not in ['Loop_Stage', 'Loop_Level_By_Image', 'Loop_Level_By_Name', 'Guild_Coop', 'Guild_Story', 'Guild']:
        print('Error Arguments. Abort.')
        print('')
        print('Examples:')
        print('python main.py --debug true --routine Loop_Level_By_Name --target "level EX-L" --count 10')
        Cleanup()
    else:
        Main()
