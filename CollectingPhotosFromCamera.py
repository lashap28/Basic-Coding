# import sys
# import subprocess

# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-python'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'uuid'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-time'])

import cv2
import uuid
import os
import time

Categories = ['Hello', 'ThumbsUp', 'ThumbsDown', 'WTF', 'Okay', 'FuckYou', 'LeftEye', 'RightEye', 'Tongue', 'Wink',
              'Smile']
MODELPHOTOS = 'ModelPhotos'

if not os.path.exists(os.path.join(os.getcwd(), MODELPHOTOS)):
    os.mkdir(os.path.join(os.getcwd(), MODELPHOTOS))

os.chdir(os.path.join(os.getcwd(), MODELPHOTOS))
for i in Categories:
    cur_cat = i
    if not os.path.exists(os.path.join(os.getcwd(), cur_cat)):
        os.mkdir(os.path.join(os.getcwd(), i))

cap = cv2.VideoCapture(0)

TIMER = int(3)
i = 0
while i < len(os.listdir()):

    ret, img = cap.read()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"Press C to Capture For Category - {os.listdir()[i]}", (20, 12), font, 0.4, (0, 255, 255), 1,
                cv2.LINE_AA)
    cv2.putText(img, f"Press R for Changing Category", (20, 24), font, 0.4, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img, f"Press W for Closing", (20, 36), font, 0.4, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('a', img)
    k = cv2.waitKey(1)

    if k == ord('r'):
        i += 1
        if i == len(os.listdir()):
            i = 0
    if k == ord('c'):
        prev = time.time()

        while TIMER >= 0:
            ret, img = cap.read()
            cv2.putText(img, str(TIMER), (50, 100), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow('a', img)
            cv2.waitKey(1)
            cur = time.time()
            if cur - prev >= 1:
                prev = cur
                TIMER = TIMER - 1
        else:
            ret, img = cap.read()
            cv2.imshow('a', img)
            # time for which image displayed
            cv2.waitKey(1000)
            TIMER = int(3)
            imgname = os.path.join(os.getcwd(), os.listdir()[i],
                                   os.listdir()[i] + '.' + '{}.jpg'.format(str(uuid.uuid1())))
            cv2.imwrite(imgname, img)

    if k == ord('w'):
        break
cap.release()
cv2.destroyAllWindows()
