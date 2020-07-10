import cv2
import sys, signal, traceback
import time
import logging, os, datetime
import keyboard
from multiprocessing import Process, freeze_support
from win10toast import ToastNotifier
import argparse

from screen import *
from logic import *
import screen

import utils
import pattern

# Global variable
shallQuit = False
shallPause = False
toaster = None # initialized after __init__ == "__main__"
toastDuration = 2
toastIcon = 'Resources/icon/icon.ico'

def OnKeyPress(event):
    global shallQuit, shallPause, toaster
    if event.event_type == 'up':
        return
    if event.name == 'f9':
        shallPause = not shallPause
        if shallPause == True:
            toaster.show_toast("SinoBot", "Paused", duration=toastDuration, icon_path=toastIcon)
        else:
            toaster.show_toast("SinoBot", "Resumed", duration=toastDuration, icon_path=toastIcon)
        
    elif event.name == 'f10':
        toaster.show_toast("SinoBot", "Exited", duration=toastDuration, icon_path=toastIcon)
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

if __name__ == '__main__':

    freeze_support()
    toaster = ToastNotifier()
    
    signal.signal(signal.SIGINT, SigCleanup)

    parser = argparse.ArgumentParser(description='SinoBot, Based On Python3.6 (32 Bit)')
    parser.add_argument('--debug', default='false', help='enable debug mode')
    args = parser.parse_args()

    isDebug = args.debug == 'true'
    
    keyboard.hook(OnKeyPress)
    keywatchProcess = Process(target=keyboard.wait)
    keywatchProcess.start()

    resizeFactor = 1.0
    windowsName = 'SM-G955F'

    battleCount = 0
    osoujiCount = 0
    prevState = state.IDLE
    waitTime = 0    
    lastBattleEndTime = time.time()

    try:
        SetupLogger()
        window = WindowScreen(windowsName, resizeFactor)
        control = Control(window)
        logic = Logic()

        toaster.show_toast("SinoBot", "Start", duration=toastDuration, icon_path=toastIcon)             
        
        while shallQuit == False:

            # Set width = 360px, height = 360 * 21 / 9 = 840px
            #hasError, errorMsg = window.ResizeWindow(width=352)

            hasError, errorMsg = None, ""

            if hasError:
                print(errorMsg)

            if shallPause == True:
                continue

            tStart = time.time()
            img, error = window.GetScreen()

            if img == None:
                print('Window "{}" Not Found, raw = {}'.format(windowsName, error))
                continue
            img, frame = utils.LoadScreen(img)
            # img, frame = utils.LoadScreenFromImage('test.jpg')
            control.Update(window.top, window.left, window.bot, window.right)
            
            isDone, logicError = logic.Process(frame, control)
            
            if isDone == True:
                print("Done All Tasks! Leaving ...")
                shallQuit = True
                    
            if logicError:
                print(logicError)
                logging.error(logicError)
            
            if isDebug:
                img = pattern.DebugDraw(img, frame, logic)
                cv2.namedWindow(windowsName, 0)
                cv2.resizeWindow(windowsName, window.size)
                cv2.imshow(windowsName, img)     

                if cv2.waitKey(30) == ord('q'):
                    # for visual apperance, re-print last output to avoid clear by 'Leaving ...'
                    print(outputStr, end='\n')
                    print('Leaving ...')
                    Cleanup()
                    break
            
            tEnd = time.time()
            deltaTime = (tEnd - tStart)
            fps = 1.0 / deltaTime
            if battleCount == 0:
                waitTimeStr = '00:00:00'
            else:
                waitTimeStr =  str(datetime.timedelta(seconds=int(float(waitTime)/float(battleCount))))

            outputStr = '[{}] FPS = {:2.2f}, Accomplished = {}, Avg Time = {}, Now Level = {}, state = {:30}'.format(time.strftime('%Y/%m/%d %H:%M:%S'), fps, battleCount, waitTimeStr, logic.prevLevel, logic.state.value)

            if prevState != logic.state and logic.state == state.REMATCH:
                battleCount += 1
                waitTime += tEnd - lastBattleEndTime
                lastBattleEndTime = tEnd

            elif prevState != logic.state and logic.state == state.OSOUJI_RESULT_COMFIRM:
                osoujiCount += 1
            
            if isDebug:    
                logging.info(outputStr.encode("utf-8"))
            elif prevState != logic.state:
                logging.info(outputStr.encode("utf-8"))

            # Update State
            prevState = logic.state

            # output to console
            # print(outputStr, end='\r')
            print(outputStr, end='\n')

    except Exception as e:
        print(e)
        logging.exception (e)
    
    finally:
        # Clean up resources    
        Cleanup()