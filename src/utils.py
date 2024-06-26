import numpy as np
import cv2
import sys
import traceback
from datetime import datetime
import os


def ToGrayScale(img):
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    return frame


def RGBToBGR(img):
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return frame


def BGRToRGB(img):
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    return frame

def LoadScreenFromImage(path):
    """
    Debug Use Function
    """
    img = cv2.imread(path)
    img_np = np.array(img)
    x, y, c = img_np.shape
    size = (int(y/2), int(x/2))
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    return img_np, ToGrayScale(img_np)


def LoadScreen(img):
    img_np = np.array(img)
    x, y, c = img_np.shape
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    return frame, ToGrayScale(frame)
    # return frame, frame


def LoadPattern(path):
    print(f'Read {path} ...', end='')
    img = cv2.imread(path)
    img_np = np.array(img)
    x, y, c = img_np.shape
    print('Done.')
    return ToGrayScale(img_np)
    # return img_np


def SaveScreenshot(frame, postfix = ''):
    if not os.path.exists('ScreenShots'):
        os.makedirs('ScreenShots')
    now = datetime.now()
    nowStr = datetime.strftime(now, '%Y-%m-%d-%H-%M-%S')
    outputStr = f'ScreenShots/ScreenShot-{nowStr}{postfix}.png'
    success = cv2.imwrite(outputStr, frame)
    if success:
        print(f'Save {outputStr}.')
    else:
        print(f'Save {outputStr} Failed.')


def printErr(e):
    error_class = e.__class__.__name__              # 取得錯誤類型
    detail = e.args[0] if len(e.args) > 0 else None  # 取得詳細內容
    cl, exc, tb = sys.exc_info()                    # 取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]    # 取得Call Stack的最後一筆資料
    fileName = lastCallStack[0]                     # 取得發生的檔案名稱
    lineNum = lastCallStack[1]                      # 取得發生的行號
    funcName = lastCallStack[2]                     # 取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
        fileName, lineNum, funcName, error_class, detail)
    print(errMsg)
