import cv2
import numpy as np

image = cv2.imread("resources/in.png")
image = cv2.resize(image, (800, 800))

imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

win = cv2.namedWindow("image")
# cv2.drawContours(image, contours, -1, (0, 255, 0), 3)


def resize(val):
    cs = contours
    im = image.copy()

    coef_y = image.shape[0] * (1 + val / 100)
    coef_x = image.shape[1] * (1 + val / 100)

    retu = list()

    for cnt in cs:
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cnt_norm = cnt - [cx, cy]
        cnt_scaled = cnt_norm * (1 + val / 100)
        cnt_scaled = cnt_scaled + [cx, cy]
        cnt_scaled = cnt_scaled.astype(np.int32)
        retu.append(cnt_scaled)

    return im, retu

    # return cs


def on_change(val):
    # cs = resize(val)
    # im = image
    im, cs = resize(val)
    cv2.drawContours(im, cs, 1, (0, 255, 0), 3)
    cv2.imshow("image", im)


cv2.createTrackbar("track", "image", 1, 100, on_change)
while True:
    key = cv2.waitKey(20) & 0xFF
    if key == 27:  # ASCII ESCape
        break
