import cv2
import utils

startPattern = utils.LoadPattern("Resources/start.PNG")
changeMissionBriefPattern = utils.LoadPattern("Resources/changeMissionBrief.PNG")
eventPattern = utils.LoadPattern("Resources/event.PNG")
skipPattern = utils.LoadPattern("Resources/skip.PNG")
missionPattern = utils.LoadPattern("Resources/mission.PNG")
storyPattern = utils.LoadPattern("Resources/story.PNG")
homePattern = utils.LoadPattern("Resources/home.PNG")
osoujiPattern = utils.LoadPattern("Resources/osouji.PNG")
osoujiPattern2 = utils.LoadPattern("Resources/osouji2.PNG")
osoujiPattern3 = utils.LoadPattern("Resources/osouji3.PNG")
storySkipPattern = utils.LoadPattern("Resources/storySkip.PNG")

nextPattern = utils.LoadPattern("Resources/next.PNG")
okPattern = utils.LoadPattern("Resources/ok.PNG")

stagePattern = utils.LoadPattern("Resources/stage.PNG")

patterns = [
    [startPattern, 0.8],
    [storyPattern, 0.8],
    [eventPattern, 0.8],
    [changeMissionBriefPattern, 0.8],
    
    [skipPattern, 0.8],
    [missionPattern, 0.8],
    [homePattern, 0.8],
    [storySkipPattern, 0.8],

    [osoujiPattern, 0.8],
    [osoujiPattern2, 0.8],
    [osoujiPattern3, 0.8],

    [nextPattern, 0.8],
    [okPattern, 0.4],

    [stagePattern, 0.8]
]

def Detect(frame, pattern, threshold=0.8):
    max_val, top_left, bottom_right = DetectTemplate(frame, pattern)
    return max_val > threshold, top_left, bottom_right

def DetectTemplate(frame, template):
    return DetectGrayScaleTemplate(frame, template)
    # return DetectColorTemplate(frame, template)

def DetectGrayScaleTemplate(frame, template):
    method = eval('cv2.TM_CCOEFF_NORMED')
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    return max_val, top_left, bottom_right

def DetectColorTemplate(frame, template):
    method = eval('cv2.TM_CCOEFF_NORMED')
    h, w, c = template.shape
    res = cv2.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    return max_val, top_left, bottom_right

def DebugDraw(img, frame, logic):

    # Draw Debug Rects, note this function does not consider early break in logic.Update
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    purple = (255, 0, 255)
    yellow = (255, 247, 0)
    orange = (255, 166, 0)
    cyan = (0, 242, 255)
    white = (255, 255, 255)

    # Convert to BGR for correct display rect color
    img = utils.RGBToBGR(img)

    for pattern, threshold in patterns:
        isExist, top_left, bottom_right = Detect(frame, pattern, threshold)
        if isExist:
            cv2.rectangle(img, top_left, bottom_right, blue, 4)

    img = utils.BGRToRGB(img)
    return img