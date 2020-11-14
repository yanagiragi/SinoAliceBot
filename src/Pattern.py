import cv2
import src.utils as utils

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
closePattern = utils.LoadPattern("Resources/close.PNG")
rematchPattern = utils.LoadPattern("Resources/rematch.PNG")
startPattern = utils.LoadPattern("Resources/start.PNG")

stagePattern = utils.LoadPattern("Resources/Target/stage.PNG")
levelPattern = utils.LoadPattern("Resources/Target/level.PNG")

#osoujiBigLeftPattern = utils.LoadPattern("Resources/Osouji/enemy_big_left.PNG")
#osoujiLeftPattern = utils.LoadPattern("Resources/Osouji/enemy_left.PNG")
#osoujiRightPattern = utils.LoadPattern("Resources/Osouji/enemy_right.PNG")

logPattern = utils.LoadPattern("Resources/log.PNG")
pausePattern = utils.LoadPattern("Resources/pause.PNG")

stageHeaderPattern = utils.LoadPattern("Resources/stageHeader.PNG")

hardPattern = utils.LoadPattern("Resources/Stage/hard.png")
normalPattern = utils.LoadPattern("Resources/Stage/normal.png")

levelPattern1 = utils.LoadPattern("Resources/Stage/level1.PNG")
levelPattern2 = utils.LoadPattern("Resources/Stage/level2.PNG")
levelPattern3 = utils.LoadPattern("Resources/Stage/level3.PNG")
levelPattern4 = utils.LoadPattern("Resources/Stage/level4.PNG")
levelPattern5 = utils.LoadPattern("Resources/Stage/level5.PNG")
levelPattern6 = utils.LoadPattern("Resources/Stage/level6.PNG")
levelPattern7 = utils.LoadPattern("Resources/Stage/level7.PNG")
levelPattern8 = utils.LoadPattern("Resources/Stage/level8.PNG")
levelPattern9 = utils.LoadPattern("Resources/Stage/level9.PNG")
levelPattern10 = utils.LoadPattern("Resources/Stage/level10.PNG")

levelPattern_exl = utils.LoadPattern("Resources/Stage/level_ex_l.PNG")
levelPattern_ex = utils.LoadPattern("Resources/Stage/level_ex.PNG")
levelPattern_cx = utils.LoadPattern("Resources/Stage/level_cx.PNG")

sinoaliceTextPattern = utils.LoadPattern("Resources/sinoaliceText.PNG")
sinoaliceDownloadingPattern = utils.LoadPattern("Resources/downloading.PNG")
dmmUpdatePattern = utils.LoadPattern("Resources/dmmUpdate.PNG")

supportPattern = utils.LoadPattern("Resources/support.PNG")
coopPattern = utils.LoadPattern("Resources/coop.PNG")

refreshPattern = utils.LoadPattern("Resources/refresh.PNG")
guildMemberPattern = utils.LoadPattern("Resources/guildMember.PNG")
coopStagePattern = utils.LoadPattern("Resources/Target/coopStage.PNG")

storyLevelPattern = utils.LoadPattern("Resources/storyLevel.PNG")
storyMidStagePattern = utils.LoadPattern("Resources/Target/storyMidStage.PNG")
storyStagePattern = utils.LoadPattern("Resources/Target/storyStage.PNG")


patterns = [
    ['start', startPattern, 0.7],
    ['story', storyPattern, 0.8],
    ['event', eventPattern, 0.65],
    
    ['coop', coopPattern, 0.65],
    # ['changeMissionBrief', changeMissionBriefPattern, 0.8],
    
    ['skip', skipPattern, 0.8],
    ['mission', missionPattern, 0.8],
    # ['home', homePattern, 0.8],
    ['storySkip', storySkipPattern, 0.6],

    ['osouji', osoujiPattern, 0.8],
    ['osouji2', osoujiPattern2, 0.8],
    ['osoujiText', osoujiTextPattern, 0.8],

    ['next', nextPattern, 0.8],
    ['ok', okPattern, 0.5],
    
    ['close', closePattern, 0.6],
    ['rematch', rematchPattern, 0.8],

    ['target stage', stagePattern, 0.8],
    ['target level', levelPattern, 0.8],

    ['log', logPattern, 0.8],
    ['pause', pausePattern, 0.8],

    ['stage header', stageHeaderPattern, 0.95],
    
    ['hard', hardPattern, 0.8],
    ['normal', normalPattern, 0.6],

    ['level 1', levelPattern1, 0.85],
    ['level 2', levelPattern2, 0.85],
    ['level 3', levelPattern3, 0.85],
    ['level 4', levelPattern4, 0.85],
    ['level 5', levelPattern5, 0.85],
    ['level 6', levelPattern6, 0.85],
    ['level 7', levelPattern7, 0.85],
    ['level 8', levelPattern8, 0.85],
    ['level 9', levelPattern9, 0.85],
    ['level 10', levelPattern10, 0.85],
    ['level EX-L', levelPattern_exl, 0.85],
    ['level EX', levelPattern_ex, 0.85],
    ['level CX', levelPattern_cx, 0.85],

    ['Sinoalice Text', sinoaliceTextPattern, 0.85],
    ['Downloading', sinoaliceDownloadingPattern, 0.85],
    ['Update App', dmmUpdatePattern, 0.85],

    ['support', supportPattern, 0.8],

    ['refresh', refreshPattern, 0.8],
    ['guild Member', guildMemberPattern, 0.8],
    ['coop stage', coopStagePattern, 0.8],

    ['story Level', storyLevelPattern, 0.8],
    ['story MidStage', storyMidStagePattern, 0.8],
    ['story Stage', storyStagePattern, 0.8]
]

existsPatternString = ''

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
    global existsPatternString

    # Draw Debug Rects, note this function does not consider early break in logic.Update
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    purple = (255, 0, 255)
    yellow = (255, 247, 0)
    orange = (255, 166, 0)
    cyan = (0, 242, 255)
    white = (255, 255, 255)

    colors = [red, green, blue, purple, yellow, orange, cyan]

    # Convert to BGR for correct display rect color
    img = utils.RGBToBGR(img)

    exists = []
    for idx, (name, pattern, threshold) in enumerate(patterns):
        isExist, top_left, bottom_right = Detect(frame, pattern, threshold)
        if isExist:
            if name[0:5] == ('target level'):
                cv2.rectangle(img, top_left, bottom_right, white, 2)
            else:
                cv2.rectangle(img, top_left, bottom_right, colors[idx % len(colors)], 2)
            exists.append(name)
        
        if name == 'osoujiText':
            max_val, top_left, bottom_right = DetectTemplate(frame, pattern)
            
    if len(exists) > 0:
        existsPatternString = ', Exists: [' + '], ['.join(exists) + ']'
    else:
        existsPatternString = ''
    
    """
    # stage debugging
    heightIncrement = (352 - 220)
    for i in range(3):
        cv2.rectangle(img, (36, 188 + heightIncrement * i), (315, 266 + heightIncrement * i), cyan, 1)
        
    # level
    heightIncrement = (330 - 252)
    for i in range(4):
        cv2.rectangle(img, (22, 252 + heightIncrement * i), (327, 317 + heightIncrement * i), cyan, 1)
        cv2.rectangle(img, (117, 264 + heightIncrement * i), (144, 278 + heightIncrement * i), cyan, 1)
    """ 

    img = utils.BGRToRGB(img)
    return img