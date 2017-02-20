#!/usr/bin/env python

import numpy as np
import cv2
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from subprocess import call
import time
import logging

'''
author: Rajmani Arya
date: 19 Feb 2017

Mobile Game Automation
playstore_link: https://play.google.com/store/apps/details?id=com.ketchapp.springninja&hl=en
Tools Required: OpenCV-Python, scikit-learn,Android Debugger Bridge (adb tools)
'''

# import math

import logging
logging.basicConfig(filename='spring.log', level=logging.DEBUG)

__gameover = False
# ml_algo = None
ml_algo = 'neural_net'

# Machine Learning Prediction
ds = np.genfromtxt('data.csv', dtype=float, delimiter=',', names=True)
train_X = []
train_y = []

for item in ds:
    train_X.append([item[0], item[1]])
    train_y.append(item[2])

if ml_algo == 'neural_net':
    regr = MLPRegressor(solver='lbfgs', hidden_layer_sizes=10, max_iter=5000, random_state=1)
else:
    regr = Ridge(alpha=0.5)

regr.fit(train_X, train_y)

print regr.score(train_X[:100], train_y[:100])

# Mathematics and Physics Prediction

def get_time(x,y,angle=60):
    t = 4.9/(x*math.tan(math.radians(angle)) - y)
    t = math.sqrt(t)
    t *= x/math.cos(math.radians(angle))
    return t

# logging.info("Running Instance of Game")

def one_move():
    # Screenshot and pull into your workspace
    call(['adb', 'shell', 'screencap', '/sdcard/spring.png'])
    call(['adb', 'pull', '/sdcard/spring.png'])

    im = cv2.imread('spring.png')
    # Resize image for faster processing
    im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)

    # Is GameOver ?
    if im[371][181][2] == 209:
        global __gameover
        print 'Game Over'
        __gameover = True
        return

    # Check BackGround and filter accordingly (only two type of backgrounds )

    if im[10][10][0] == 119:
        lower = np.array([26, 245, 220])
        upper = np.array([30, 249, 224])
    else:
        lower = np.array([64, 235, 189])
        upper = np.array([68, 239, 193])

    # Mask top of pole and find contours
    mask = cv2.inRange(im, lower, upper)
    image,contours,h = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    points = []

    for i,cnt in enumerate(contours):
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.05 * peri, True)
        if len(approx) == 2:
            x = (approx[0][0][0] + approx[1][0][0])/2
            y = (approx[0][0][1] + approx[1][0][1])/2
            points.append((x,y))

    # points containes top center of each pole
    points = sorted(points, key=lambda x: x[0])
    # remove pole less than 60 pixel
    if points[0][0] < 60:
        del points[0]

    # Find player position relative to top pole center
    hero = im[points[0][1]-40:points[0][1]-20, points[0][0]-25:points[0][0]+25]
    lower = np.array([250, 250, 250])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hero, lower, upper)
    image,contours,h = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    hero_pos = 0
    for i,cnt in enumerate(contours):
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.05 * peri, True)
        hero_pos = approx[1][0][0] - 25 # WRT to center of pole

    x = points[1][0] - points[0][0] - hero_pos
    y = points[0][1] - points[1][1]

    time = regr.predict([[x,y]])
    time = int(time[0])
    arr = (hero_pos, x, y, time)
    print arr
    logging.info(",".join(map(str, arr)))    
    # time = get_time(x,y)
    cmd = ['adb', 'shell', 'input', 'swipe', '360', '640', '360', '640']
    cmd.append(str(time))
    call(cmd)
    # cv2.imshow('Image', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    while __gameover == False:
        one_move()
        time.sleep(1.0)
    logging.info('GameOver')