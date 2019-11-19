import cv2
import sys, signal
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
    
    parser = argparse.ArgumentParser(description='SinoBot, Based On Python3.6 (32 Bit)')
    parser.add_argument('--debug', default='false', help='enable debug mode')
    parser.add_argument('--keyboard', default='true', help='enable f9 as hotkey')
    parser.add_argument('--combo', default='0', help='Perform combo when battle')
    args = parser.parse_args()

    isDebug = args.debug == 'true'
    isEnableKeyboard = args.keyboard == 'true'
    usingCombo = int(args.combo)

    if usingCombo != 0:
        print('using Combo: {}'.format(usingCombo))

    signal.signal(signal.SIGINT, SigCleanup)

    keyboard.hook(OnKeyPress)
    keywatchProcess = Process(target=keyboard.wait)
    keywatchProcess.start()

    resizeFactor = 1.0
    windowsName = 'Galaxy S8+'

    battleCount = 0
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
            hasError, errorMsg = window.ResizeWindow(width=360)
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
            
            tEnd1 = time.time()
            deltaTime1 = (tEnd1 - tStart)
            
            # img, frame = utils.LoadScreenFromImage('test.jpg')
            control.Update(window.top, window.left, window.bot, window.right)
            logicError = logic.Process(frame, control)
                    
            if logicError:
                print(logicError)
                logging.error(logicError)
            
            tEnd2 = time.time()
            deltaTime2 = (tEnd2- tEnd1)
            
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
            deltaTime3 = (tEnd - tEnd2)
            fps = 1.0 / deltaTime
            if battleCount == 0:
                waitTimeStr = '00:00:00'
            else:
                waitTimeStr =  str(datetime.timedelta(seconds=int(float(waitTime)/float(battleCount))))

            if isDebug:
                outputStr = '[{}] FPS = {:2.2f} ({:4.2f} ms, {:4.2f}/ {:4.2f}/ {:4.2f}), Accomplished = {}, Avg Time = {}, state = {:30}'.format(time.strftime('%Y/%m/%d %H:%M:%S'), fps, deltaTime * 1000, deltaTime1 * 1000, deltaTime2 * 1000, deltaTime3 * 1000, battleCount, waitTimeStr , logic.state.value)
            else:
                outputStr = '[{}] FPS = {:2.2f}, Accomplished = {}, Avg Time = {}, state = {:30}'.format(time.strftime('%Y/%m/%d %H:%M:%S'), fps, battleCount, waitTimeStr, logic.state.value)

            if prevState != logic.state and logic.state == state.END_BATTLE:
                battleCount += 1
                waitTime += tEnd - lastBattleEndTime
                lastBattleEndTime = tEnd
            
            if isDebug:    
                logging.info(outputStr)
            elif prevState != logic.state:
                logging.info(outputStr)

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