# -*- coding: utf-8 -*-
#用opencv拼配起点，用鼠标点击终点，根据距离计算手机触摸时间

from __future__ import print_function, division
import os
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
from subprocess import run
from PIL import Image
import random

scale = 0.25
template = cv2.imread('character.png')
template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
template_size = template.shape[:2]
#plt.imshow(template[:,:,::-1])

def search(img):
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    cv2.rectangle(
        img,
        (min_loc[0], min_loc[1]),
        (min_loc[0] + template_size[1], min_loc[1] + template_size[0]),
        (255, 0, 0),
        4)
    return img, min_loc[0] + template_size[1] / 2, min_loc[1] +  template_size[0]


def pull_screenshot():
    #filename = datetime.datetime.now().strftime("%H%M%S") + '.png'
    #os.system('mv autojump.png {}'.format(filename))
    #os.system('adb shell screencap -p /sdcard/autojump.png')
    #os.system('adb pull /sdcard/autojump.png .')
    #run('mv autojump.png {}'.format(filename),shell=True)
    run('adb shell screencap -p /sdcard/autojump.png',shell=True)
    run('adb pull /sdcard/autojump.png .',shell=True)


def jump(distance):
    press_time = distance * 2.3
    press_time = int(press_time)
    right=random.uniform(600-50, 600+50)
    down=random.uniform(1150-50, 1150+50)
    cmd = 'adb shell input swipe {0} {1} {0} {1} '.format(right,down) + str(press_time)
    print(cmd)
    #os.system(cmd)
    run(cmd,shell=True)

def update_data():
    global src_x, src_y

    img = cv2.imread('autojump.png')
    img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    img, src_x, src_y = search(img)
    return img[:,:,::-1]

pull_screenshot()
fig = plt.figure()
img = update_data()
#fig=cv2.imshow('jump',img)
im = plt.imshow(img, animated=True)

update = True


def updatefig(*args):
    global update

    if update:
        time.sleep(1)
        pull_screenshot()
        im.set_array(update_data())
        update = False
    return im,


def on_click(event):
    global update    
    global src_x, src_y
    
    dst_x, dst_y = event.xdata, event.ydata

    distance = (dst_x - src_x)**2 + (dst_y - src_y)**2 
    distance = (distance ** 0.5) / scale
    print('distance = ', distance)
    jump(distance)
    update = True


fig.canvas.mpl_connect('button_press_event', on_click)
ani = animation.FuncAnimation(fig, updatefig, interval=5, blit=True)
plt.show()
