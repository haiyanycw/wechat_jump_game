# -*- coding: utf-8 -*-
#微信程序运行后，python获得截图，鼠标点击起始和终止位置，程序自动计算距离，再根据距离计算手机上触摸时间

import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import random
from subprocess import run
#%matplotlib qt5

def pull_screenshot():
    #os.system('adb shell screencap -p /sdcard/autojump.png')
    #os.system('adb pull /sdcard/autojump.png .')
    run('adb shell screencap -p /sdcard/autojump.png',shell=True)
    run('adb pull /sdcard/autojump.png .',shell=True)


def jump(distance):
    press_time = distance * 2.3
    press_time = int(press_time)
    right=random.uniform(600-50, 600+50)
    down=random.uniform(1150-50, 1150+50)
    cmd = 'adb shell input swipe {0} {1} {0} {1} '.format(right,down) + str(press_time)
    #cmd = 'adb shell input swipe 320 410 320 410 ' + str(press_time)
    print(cmd)
    run(cmd,shell=True)
    #os.system(cmd)


fig = plt.figure()
pull_screenshot()
img = np.array(Image.open('autojump.png'))
im = plt.imshow(img, animated=True)

update = True
click_count = 0
cor = []


def update_data():
    return np.array(Image.open('autojump.png'))


def updatefig(*args):
    global update
    if update:
        time.sleep(1.5)
        pull_screenshot()
        im.set_array(update_data())
        update = False
    return im,


def on_click(event):
    global update
    global ix, iy
    global click_count
    global cor

    ix, iy = event.xdata, event.ydata
    coords = [(ix, iy)]
    print('now = ', coords)
    cor.append(coords)

    click_count += 1
    if click_count > 1:
        click_count = 0
        cor1 = cor.pop()
        cor2 = cor.pop()

        distance = (cor1[0][0] - cor2[0][0])**2 + (cor1[0][1] - cor2[0][1])**2
        distance = distance ** 0.5
        print('distance = ', distance)
        jump(distance)
        update = True


fig.canvas.mpl_connect('button_press_event', on_click)
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
