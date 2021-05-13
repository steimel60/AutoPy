import os
import pyautogui as gui
import time
from time import sleep
from Settings import *
from scene_pics import *
import scene_funcs as scene


scene_path = 'C:\Program Files\FARO\SCENE\SCENE.exe'
def run_scene():
    start()
    close_warning_and_pop_up()




def start():
    os.startfile(scene_path)
    time.sleep(5)
def close_warning_and_pop_up():
    gui.press('enter')
    scene.check_for_image(close_png)
    gui.click()
def close_scene():
    check_for_image(closeScene_png)
    gui.move(30, -20)
    gui.click()


run_scene()
