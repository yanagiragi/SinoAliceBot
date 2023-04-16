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
from src.Window import Window
import src.utils as utils

from src.Routines import *

# Const settings
isPc = False

resizeFactor = 1.0  # scale factor of the screenshot of the window
debugWindowScaleFactor = 1  # scale factor of the debug window

toastDuration = 2
toastIcon = 'Resources/icon/icon.ico'

ApplicationName = 'SinoBot'
dmmTitle = 'Myゲーム - DMM GAME PLAYER'

windowsName = 'SM-G955F'
resultion = '461x976'

maxExecutionTime = 60 * 5

# Global variable
isDebug = True
shallQuit = False
shallPause = False
toaster = None  # initialized after __init__ == "__main__"
lastFrame = None
startTime = datetime.datetime.now()

predefined_routines = {
    # 'BlueArchiveDaily': lambda control, targetLevel, targetCount: BlueArchiveDaily.Routine_BlueArchiveDaily('Open Blue Archive', control),
    'HeavenBurnsRedDaily': lambda control, targetLevel, targetCount: HeavenBurnsRedDaily.Routine_HeavenBurnsRedDaily('Open Heaven Burns Red', control),
    'ProjectSekaiDaily': lambda control, targetLevel, targetCount: ProjectSekaiDaily.Routine_ProjectSekaiDaily('Open Heaven Burns Red', control),
    'Deemo2Daily': lambda control, targetLevel, targetCount: Deemo2Daily.Routine_Deemo2Daily('Open Deemo2', control)
}


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
        utils.SaveScreenshot(frame, 'Cleanup-')


def SigCleanup():
    global lastFrame
    Cleanup(lastFrame)
    sys.exit(0)


def SetupParser():
    parser = argparse.ArgumentParser(
        description='SinoBot, Based On Python3.7.2 (32 Bit)')
    parser.add_argument('--debug', default='false', help='enable debug mode')
    parser.add_argument('--routine', help='routine schema')
    parser.add_argument('--target', help='level to loop')
    parser.add_argument('--count', default=0, help='level to loop')
    return parser.parse_args()


def SelectRoutine(targetRoutine, control, targetLevel=None, targetCount=None):
    return predefined_routines[targetRoutine](control, targetLevel, targetCount)


"""def OpenSinoalice():
    window = Window(dmmTitle, resizeFactor)
    control = Control(window, resultion)
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


"""
Returns shall quit or not
"""


def Tick(window, logic, control) -> bool:
    global lastFrame
    
    if shallQuit is True:
        return True

    elif shallPause is True:
        return False

    tStart = time.time()  # Start Recording

    img, error = window.GetScreen()
    if img is None:
        print('Window "{}" Not Found, raw = {}'.format(window.name, error))
        return True

    img, frame = utils.LoadScreen(img)  # Get ScreenShot of img
    # img, frame = img[58:-10, 10:-10], frame[58:-10, 10:-10] # slice out window title
    # img, frame = utils.LoadScreenFromImage('test.jpg') # debug

    lastFrame = frame

    # update internal position of control instance
    control.Update(window.top, window.left, window.bot, window.right)

    isDone, logicError = logic.Process(frame)  # Procress Main Logic
    # isDone, logicError = False, None  # Freeze Logic for Debugging

    if isDone is True:
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
            Cleanup(lastFrame)
            return True

    # if isDebug or logic.prevState != logic.state:
    #    logging.info(outputStr)
    logging.info(outputStr)

    # output to console, currently only works with utf-8 console
    try:
        print(outputStr, end='\n')
    except Exception as e:
        print(outputStr.encoding('utf-8') + f', exception = {e}', end='\n')
    finally:
        return False


def MainLoop():
    global shallQuit, startTime

    window = Window(windowsName, resizeFactor)

    control = Control(window, resultion)  # Create controll instance
    # control = ControlAdb(window) # Create controll instance

    routine = SelectRoutine(targetRoutine, control, targetLevel, targetCount)
    logic = Logic(routine, control)  # Create Main Logic

    patternPrefix = "PC" if isPc else "Android"
    patternPrefix = f'{patternPrefix}/{resultion}'
    Pattern.patterns = Pattern.LoadPatterns(patternPrefix)

    window.SetForeground()

    toaster.show_toast(ApplicationName, "Start", duration=toastDuration,
                       icon_path=toastIcon)  # Show Notifcation

    while not shallQuit:
        shallQuit = Tick(window, logic, control) or shallQuit
        if (datetime.datetime.now() - startTime).seconds > maxExecutionTime:
            print('Reach max execution time!')
            shallQuit = True


def Main():
    global lastFrame
    try:
        MainLoop()
    except Exception as e:
        utils.printErr(e)
        logging.exception(e)
    finally:
        Cleanup(lastFrame)


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

    if targetRoutine not in predefined_routines.keys():
        print('Error Arguments. Abort.')
        print('')
        print('Possible values = ' + ','.join(predefined_routines.keys()))
        print('Examples:')
        print('python main.py --debug true --routine Loop_Level_By_Name --target "level EX-L" --count 10')
        Cleanup(None)
    else:
        Main()
