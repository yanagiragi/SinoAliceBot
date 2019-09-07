import numpy as np
import cv2

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

# Debug Function
def LoadScreenFromImage(path):
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
    img = cv2.imread(path)
    img_np = np.array(img)
    x, y, c = img_np.shape
    return ToGrayScale(img_np)
    # return img_np
