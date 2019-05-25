import win32api
import win32con
from win32gui import *
from io import BytesIO
from PIL import ImageGrab
import numpy as np
import time
import cv2
import random
from find import compare

titles = []
#TODO running state list or run 3 times and compare threshod
app_name = '明日方舟'

dir1='resource/map_temp.png'
dir2='resource/chara_temp.png'
dir3='resource/finish_temp.png'

# how many times to loop
loop_time = 1

def find_all_window(hwnd, _):
    global titles
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.append(GetWindowText(hwnd))

def find_arknights():
    global titles
    EnumWindows(find_all_window, 0)
    for i in range(len(titles)):
        if titles[i].find(app_name, 0) != -1:
            return titles[i]

def get_pos(window_name):
    window = FindWindow(None,window_name)
    SetForegroundWindow(window)
    return GetWindowRect(window)

def cap_scr():
    img = ImageGrab.grab()
    np_img = np.array(img)
    buffer = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    return buffer

def mouse_left_click(x1,y1,x2,y2):

    point = (int(random.uniform(x1+10,x2)),int(random.uniform(y1,y2)))
    win32api.SetCursorPos(point)
    time.sleep(random.uniform(0.05,0.2))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def get_click_range(box):
    x1 = box[0][0][0]
    y1 = box[0][0][1]

    x2 = box[2][0][0]
    y2 = box[2][0][1]

    return x1, y1, x2, y2


def agent(map_tmp, chara_tmp, finish_tmp, game_page, game_pos):
    global loop_time
    print("running")

    while loop_time > 0:
        print("Remaining Loop --->", loop_time-1)
        while True:
            game_page = cap_scr()
            box = compare(map_tmp, game_page)
            time.sleep(random.uniform(1, 2))
            if box is None:
                print("Loading... Map page")

            else:
                x1, y1, x2, y2 = get_click_range(box)
                mouse_left_click(x1,y1,x2,y2)
                break


        while True:
            game_page = cap_scr()
            box = compare(chara_tmp,game_page)
            time.sleep(random.uniform(1, 2))
            if box is None:
                print("Loading... Chara Page")

            else:
                x1, y1, x2, y2 = get_click_range(box)
                mouse_left_click(x1,y1,x2,y2)
                break

        while True:

            game_page = cap_scr()
            box = compare(finish_tmp, game_page)
            time.sleep(random.uniform(5, 10))
            if box is None:
                print("in battle...Remaining loop--->",loop_time-1)
            else:
                x1, y1, x2, y2 = get_click_range(box)
                mouse_left_click(x1,y1,x2,y2)
                break

        loop_time -= 1
    print("Agent finished!!!")

def compare_temp(img):
    pass

def load_temp(dir):
    return cv2.imread(dir, 0)

if __name__ == '__main__':

    window_name = find_arknights()
    if window_name is None:
        print("ArkNights not running, please retry")
        exit(1)

    #load 3 tmps
    map_tmp = load_temp(dir1)
    chara_tmp = load_temp(dir2)
    finish_tmp = load_temp(dir3)

    game_pos = get_pos(window_name)
    print(app_name,"at",game_pos)

    game_page = cap_scr()

    agent(map_tmp, chara_tmp, finish_tmp,
          game_page, game_pos )




