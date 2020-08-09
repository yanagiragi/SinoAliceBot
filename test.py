import subprocess
import cv2
import numpy as np

print('Popen Done')
while True:
    #pipe.stdin.write(b'screencap -p')
    #pipe.stdin.write(b'wm size\n')
    #pipe = subprocess.Popen("adb shell wm size", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    #out_bytes = pipe.stdout.read()
    #print(out_bytes)
    #continue
    pipe = subprocess.Popen("adb shell screencap -p", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    h, w, c = image.shape
    factor = 4
    image = cv2.resize(image, (int(w / factor), int(h / factor)))
    cv2.imshow("", image)
cv2.waitKey(0)
cv2.destroyWindow("")

# factor = 4.11
# 27 51 -> 100 200
# 347 x 723 > 1440x2960