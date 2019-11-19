import cv2
import utils

homePattern = utils.LoadPattern("Resources/home.PNG")
storyPattern = utils.LoadPattern("Resources/story.PNG")
missionPattern = utils.LoadPattern("Resources/mission.PNG")
changeMissionBriefPattern = utils.LoadPattern("Resources/changeMissionBrief.PNG")

eventPattern = utils.LoadPattern("Resources/event.PNG")
storySkipPattern = utils.LoadPattern("Resources/storySkip.PNG")
skipPattern = utils.LoadPattern("Resources/skip.PNG")

osoujiPattern = utils.LoadPattern("Resources/osouji.PNG")
osoujiPattern2 = utils.LoadPattern("Resources/osouji2.PNG")
osoujiTextPattern = utils.LoadPattern("Resources/osoujiText.PNG")

nextPattern = utils.LoadPattern("Resources/next.PNG")
okPattern = utils.LoadPattern("Resources/ok.PNG")
rematchPattern = utils.LoadPattern("Resources/rematch.PNG")
startPattern = utils.LoadPattern("Resources/start.PNG")

stagePattern = utils.LoadPattern("Resources/Stage/stage.PNG")
levelPattern = utils.LoadPattern("Resources/Stage/level.PNG")

osoujiBigLeftPattern = utils.LoadPattern("Resources/Osouji/enemy_big_left.PNG")
osoujiLeftPattern = utils.LoadPattern("Resources/Osouji/enemy_left.PNG")
osoujiRightPattern = utils.LoadPattern("Resources/Osouji/enemy_right.PNG")

logPattern = utils.LoadPattern("Resources/log.PNG")
pausePattern = utils.LoadPattern("Resources/pause.PNG")

patterns = [
    ['start', startPattern, 0.7],
    ['story', storyPattern, 0.8],
    ['event', eventPattern, 0.65],
    # ['changeMissionBrief', changeMissionBriefPattern, 0.8],
    
    ['skip', skipPattern, 0.8],
    ['mission', missionPattern, 0.8],
    # ['home', homePattern, 0.8],
    ['storySkip', storySkipPattern, 0.6],

    ['osouji', osoujiPattern, 0.8],
    ['osouji2', osoujiPattern2, 0.8],
    ['osoujiText', osoujiTextPattern, 0.8],

    ['next', nextPattern, 0.8],
    ['ok', okPattern, 0.4],
    ['rematch', rematchPattern, 0.8],

    ['stage', stagePattern, 0.8],
    ['level', levelPattern, 0.8],

    ['log', logPattern, 0.8],
    ['pause', pausePattern, 0.8]
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

    for name, pattern, threshold in patterns:
        isExist, top_left, bottom_right = Detect(frame, pattern, threshold)
        if isExist:
            cv2.rectangle(img, top_left, bottom_right, blue, 4)

    img = utils.BGRToRGB(img)
    return img