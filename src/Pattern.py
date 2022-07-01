import cv2
import src.utils as utils

# Global variables
existsPatternString = ''
patterns = []


def LoadPatterns(resourcePrefix):

    print(f"Load pattern with prefix: {resourcePrefix}")

    homePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/home.PNG")                                 # noqa
    storyPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/story.PNG")                               # noqa
    missionPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/mission.PNG")                           # noqa
    changeMissionBriefPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/changeMissionBrief.PNG")     # noqa

    eventPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/event.PNG")                               # noqa
    storySkipPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/storySkip.PNG")                       # noqa
    skipPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/skip.PNG")                                 # noqa

    osoujiPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/osouji.PNG")                             # noqa
    osoujiPattern2 = utils.LoadPattern(f"Resources/{resourcePrefix}/osouji2.PNG")                           # noqa
    osoujiTextPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/osoujiText.PNG")                     # noqa

    nextPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/next.PNG")                                 # noqa
    okPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/ok.PNG")                                     # noqa
    closePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/close.PNG")                               # noqa
    rematchPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/rematch.PNG")                           # noqa
    startPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/start.PNG")                               # noqa

    stagePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Target/stage.PNG")                        # noqa
    levelPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Target/level.PNG")                        # noqa

    #osoujiBigLeftPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Osouji/enemy_big_left.PNG")      # noqa
    #osoujiLeftPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Osouji/enemy_left.PNG")             # noqa
    #osoujiRightPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Osouji/enemy_right.PNG")           # noqa

    logPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/log.PNG")                                   # noqa
    pausePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/pause.PNG")                               # noqa

    stageHeaderPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/stageHeader.PNG")                   # noqa

    hardPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/hard.png")                           # noqa
    normalPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/normal.png")                       # noqa

    levelPattern1 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level1.PNG")                       # noqa
    levelPattern2 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level2.PNG")                       # noqa
    levelPattern3 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level3.PNG")                       # noqa
    levelPattern4 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level4.PNG")                       # noqa
    levelPattern5 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level5.PNG")                       # noqa
    levelPattern6 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level6.PNG")                       # noqa
    levelPattern7 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level7.PNG")                       # noqa
    levelPattern8 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level8.PNG")                       # noqa
    levelPattern9 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level9.PNG")                       # noqa
    levelPattern10 = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level10.PNG")                     # noqa

    levelPattern_exl = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level_ex_l.PNG")                # noqa
    levelPattern_ex = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level_ex.PNG")                   # noqa
    levelPattern_cx = utils.LoadPattern(f"Resources/{resourcePrefix}/Stage/level_cx.PNG")                   # noqa

    sinoaliceTextPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/sinoaliceText.PNG")               # noqa
    sinoaliceDownloadingPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/downloading.PNG")          # noqa
    dmmUpdatePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/dmmUpdate.PNG")                       # noqa

    supportPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/support.PNG")                           # noqa
    coopPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/coop.PNG")                                 # noqa

    refreshPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/refresh.PNG")                           # noqa
    guildMemberPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/guildMember.PNG")                   # noqa
    coopStagePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Target/coopStage.PNG")                # noqa

    storyLevelPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/storyLevel.PNG")                     # noqa
    storyMidStagePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Target/storyMidStage.PNG")        # noqa
    storyStagePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/Target/storyStage.PNG")              # noqa

    maintencePattern = utils.LoadPattern(f"Resources/{resourcePrefix}/maintence.PNG")                       # noqa
    crossPattern = utils.LoadPattern(f"Resources/{resourcePrefix}/cross.PNG")                               # noqa

    return [
        ['start', startPattern, 0.7],
        ['story', storyPattern, 0.8],
        ['event', eventPattern, 0.65],
        ['coop', coopPattern, 0.65],
        ['mission', missionPattern, 0.8],
        ['storySkip', storySkipPattern, 0.6],
        ['next', nextPattern, 0.8],
        ['ok', okPattern, 0.6],
        ['log', logPattern, 0.8],

        ['skip', skipPattern, 0.8],  # NOT OK

        ['osouji', osoujiPattern, 0.8],
        ['osouji2', osoujiPattern2, 0.8],
        ['osoujiText', osoujiTextPattern, 0.8],

        ['close', closePattern, 0.6],
        ['rematch', rematchPattern, 0.8],

        ['target stage', stagePattern, 0.8],
        ['target level', levelPattern, 0.8],

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
        ['story Stage', storyStagePattern, 0.8],

        ['maintence', maintencePattern, 0.8],
        ['cross', crossPattern, 0.8]
    ]


def Detect(frame, pattern, threshold=0.8):
    max_val, top_left, bottom_right = DetectTemplate(frame, pattern)
    return max_val > threshold, max_val, top_left, bottom_right


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
        isExist, val, top_left, bottom_right = Detect(frame, pattern, threshold)  # noqa
        if isExist:
            if name[0:5] == ('target level'):
                cv2.rectangle(img, top_left, bottom_right, white, 2)
            else:
                cv2.rectangle(img, top_left, bottom_right,
                              colors[idx % len(colors)], 2)
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
