import os
import sys
import signal
import subprocess
import time
import logging
import datetime
import keyboard
from multiprocessing import Process, freeze_support
from win10toast import ToastNotifier
import argparse
import cv2

from screen import *
from logic import *
import screen

import utils
import Pattern
from State import State

from LoopStage import Routine_LoopStage
from LoopLevelByImage import Routine_LoopLevelByImage

# Global variable
shallQuit = False
shallPause = False
toaster = None # initialized after __init__ == "__main__"
toastDuration = 2
toastIcon = 'Resources/icon/icon.ico'
ApplicationName = 'SinoBot'
ConenctionExecutor = 'D:/_Programs/Programs/_Shortcuts/scrcpy-win64-v1.14/scrcpy.exe --window-height 720 --window-borderless -w'

def OnKeyPress(event):
    global shallQuit, shallPause, toaster
    if event.event_type == 'up':
        return
    if event.name == 'f9':
        shallPause = not shallPause
        if shallPause == True:
            toaster.show_toast(ApplicationName, "Paused", duration=toastDuration, icon_path=toastIcon)
        else:
            toaster.show_toast(ApplicationName, "Resumed", duration=toastDuration, icon_path=toastIcon)
        
    elif event.name == 'f10':
        toaster.show_toast(ApplicationName, "Exited", duration=toastDuration, icon_path=toastIcon)
        shallQuit = True
        shallPause = True

def SetupLogger():
    if not os.path.exists('log'):
        os.makedirs('log')

    log_filename = datetime.datetime.now().strftime("log/%Y-%m-%d_%H_%M_%S.log")
    print ('Logging File: {}'.format(log_filename))
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s', datefmt='%m-%d %H:%M:%S', filename=log_filename)

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
    parser = argparse.ArgumentParser(description='SinoBot, Based On Python3.7.2 (32 Bit)')
    parser.add_argument('--debug', default='false', help='enable debug mode')
    return parser.parse_args()

def MainLoop():    
    SetupLogger() # Setup Logger
    
    window = WindowScreen(windowsName, resizeFactor) # Get window instance
    control = Control(window) # Create controll instance

    """

    Select Your Main Routine:

    Routine_LoopLevelByImage: Loop Single Level (matched with Resource/Stage/level.PNG), won't terminate

    Routine_LoopStage: Explore All levels (normal & hard) in a stage, terminates if all levels are looped

    """
    routine = Routine_LoopLevelByImage('Routine.Loop_Level_By_Image', control, False)
    # routine = Routine_LoopStage('Routine.Loop_Stage', control, False)

    logic = Logic(routine, control) # Create Main Logic

    toaster.show_toast(ApplicationName, "Start", duration=toastDuration, icon_path=toastIcon) # Show Notifcation
    
    while shallQuit == False:

        # Set width = 360px, height = 360 * 21 / 9 = 840px
        # hasError, errorMsg = window.ResizeWindow(width=352)
        # hasError, errorMsg = None, ""
        # if hasError:
        #    print(errorMsg)

        if shallPause == True:
            continue

        tStart = time.time() # Start Recording
        
        img, error = window.GetScreen()
        if img == None:
            print('Window "{}" Not Found, raw = {}'.format(windowsName, error))
            continue

        img, frame = utils.LoadScreen(img) # Get ScreenShot of img
        # img, frame = utils.LoadScreenFromImage('test.jpg') # debug

        control.Update(window.top, window.left, window.bot, window.right) # update internal position of control instance
        
        isDone, logicError = logic.Process(frame) # Procress Main Logic
        
        if isDone == True:
            print("Done All Tasks! Leaving ...")
            shallQuit = True
                
        elif logicError:
            print(logicError)
            logging.error(logicError)
        
        if isDebug:
            img = Pattern.DebugDraw(img, frame, logic)
            cv2.namedWindow(windowsName, 0)
            cv2.resizeWindow(windowsName, window.size)
            cv2.imshow(windowsName, img)     

            if cv2.waitKey(30) == ord('q'):
                # for visual apperance, re-print last output to avoid clear by 'Leaving ...'
                print(outputStr, end='\n')
                print('Leaving ...')
                Cleanup()
                break
        
        tEnd = time.time() # End Recording
        deltaTime = (tEnd - tStart)
        fps = 1.0 / deltaTime
        outputStr = '[{}] FPS = {:2.2f}'.format(time.strftime('%Y/%m/%d %H:%M:%S'), fps) + logic.GetMessage()
        
        if isDebug or prevState != logic.state:
            logging.info(outputStr.encode("utf-8"))
        
        # output to console
        # print(outputStr, end='\r')
        print(outputStr, end='\n')

if __name__ == '__main__':
    
    freeze_support()
    
    toaster = ToastNotifier() # Setup Toast Notification
    
    # Setup Parser
    args = SetupParser() 
    isDebug = args.debug == 'true'
    
    # Hook hotkey
    signal.signal(signal.SIGINT, SigCleanup) 
    keyboard.hook(OnKeyPress)
    keywatchProcess = Process(target=keyboard.wait)
    keywatchProcess.start()

    resizeFactor = 1.0
    windowsName = 'SM-G955F'

    try:
       MainLoop()

    except Exception as e:
        utils.printErr(e)
        logging.exception (e)
    
    finally:
        # Clean up resources    
        Cleanup()