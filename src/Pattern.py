import cv2
import src.utils as utils
import json

# Global variables
existsPatternString = ''
patterns = []


def LoadPatterns(resourcePrefix):

    print(f"Load pattern with prefix: {resourcePrefix}")

    raw = open('src/pattern.json')
    config = json.load(raw)

    def parse_config(config):
        return [
            config['name'],
            utils.LoadPattern(f"Resources/{resourcePrefix}/{config['pattern']}"),
            config['threshold']
        ]

    return [parse_config(c) for c in config]


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
            color_idx = int(hash(name)) % len(colors)
            cv2.rectangle(img, top_left, bottom_right,
                              colors[color_idx], 2)
            exists.append(name)

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
