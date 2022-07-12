import cv2
import src.utils as utils

# Global variables
existsPatternString = ''
patterns = []


def LoadPatterns(resourcePrefix):

    print(f"Load pattern with prefix: {resourcePrefix}")

    config = [
        ['start', 'start.png', 0.7],
        ['story', 'story.png', 0.8],
        ['event', 'event.png', 0.65],
        ['coop', 'coop.png', 0.65],
        ['mission', 'mission.png', 0.8],
        ['storySkip', 'storySkip.png', 0.6],
        ['next', 'next.png', 0.8],
        ['ok', 'ok.png', 0.6],
        ['log', 'log.png', 0.8],

        ['skip', 'skip.png', 0.8],  # NOT OK

        ['osouji', 'osouji.png', 0.8],
        ['osouji2', 'osouji2.png', 0.8],
        ['osoujiText', 'osoujiText.png', 0.8],

        ['close', 'close.png', 0.6],
        ['rematch', 'rematch.png', 0.8],

        ['target stage', 'Target/stage.png', 0.8],
        ['target level', 'Target/level.png', 0.8],

        ['pause', 'pause.png', 0.8],

        ['stage header', 'stageHeader.png', 0.95],

        ['hard', 'Stage/hard.png', 0.8],
        ['normal', 'Stage/normal.png', 0.6],
        ['level 1', 'Stage/level1.png', 0.85],
        ['level 2', 'Stage/level2.png', 0.85],
        ['level 3', 'Stage/level3.png', 0.85],
        ['level 4', 'Stage/level4.png', 0.85],
        ['level 5', 'Stage/level5.png', 0.85],
        ['level 6', 'Stage/level6.png', 0.85],
        ['level 7', 'Stage/level7.png', 0.85],
        ['level 8', 'Stage/level8.png', 0.85],
        ['level 9', 'Stage/level9.png', 0.85],
        ['level 10', 'Stage/level10.png', 0.85],
        ['level EX-L', 'Stage/level_ex_l.png', 0.85],
        ['level EX', 'Stage/level_ex.png', 0.85],
        ['level CX', 'Stage/level_cx.png', 0.85],

        ['Sinoalice Text', 'sinoaliceText.png', 0.85],
        ['Downloading', 'downloading.png', 0.85],
        ['Update App', 'dmmUpdate.png', 0.85],

        ['support', 'support.png', 0.8],
        ['refresh', 'refresh.png', 0.8],

        ['guild Member', 'guildMember.png', 0.8],
        ['coop stage', 'Target/coopStage.png', 0.8],
        ['story Level', 'Target/level.png', 0.8],
        ['story MidStage', 'Target/storyMidStage.png', 0.8],
        ['story Stage', 'Target/storyStage.png', 0.8],

        ['maintence', 'maintence.png', 0.8],
        ['cross', 'cross.png', 0.8]
    ]

    return [[c[0], utils.LoadPattern(f"Resources/{resourcePrefix}/{c[1]}"), c[2]] for c in config]


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
        isExist, val, top_left, bottom_right = Detect(
            frame, pattern, threshold)
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
