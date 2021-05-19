from Settings import *
from pix_mapper_pics import *
import re
import glob
import os
import pyautogui as gui
import time
from time import sleep

screen_center = (gui.size()[0] / 2, (gui.size()[1] / 2) - 50)

def start():
    os.startfile(pix_mapper_path)
    time.sleep(15)

def new_project(job):
    gui.hotkey('ctrl','n')
    gui.write(job[0] + '_' + job[2])
    gui.press('tab', presses=3)
    gui.press('enter')
    time.sleep(1)
    gui.press('tab', presses=2)
    gui.press('enter')
    time.sleep(1)

def load_pics(job):
    gui.write(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\' + job[2] + '\\' + '0' + job[2])
    gui.press('enter')
    time.sleep(2)
    gui.press('enter')
    time.sleep(2)
    gui.press('enter')
    time.sleep(5)
    gui.press('tab',presses=5)
    time.sleep(5)
    gui.press('enter')
    time.sleep(1)
    gui.press('enter')
    time.sleep(10)
    if job[2] != 'site':
        gui.press('down')
    else:
        gui.press('down')
        gui.press('up')
    gui.press('enter')

def import_gcp(job):
    for file in glob.glob(new_job_folder + '/' + job[0] + '*' + '/Drone/*'):
        if 'GCP_EDIT' in file.upper():
            check_for_image(pixGCP)
            gui.click()
            time.sleep(1)
            gui.press('tab', presses=3)
            gui.press('enter')
            time.sleep(1)
            gui.press('tab', presses=2)
            gui.write('4326')
            gui.press('enter')
            time.sleep(1)
            gui.press('enter')
            time.sleep(1)
            gui.press('tab')
            time.sleep(1)
            gui.press('tab')
            gui.press('enter')
            for i in range (0,6):
                gui.press('tab')
                time.sleep(.5)
            gui.press('up')
            time.sleep(1)
            gui.press('tab', presses=2)
            gui.press('enter')
            time.sleep(1)
            gui.press('tab', presses=5)
            gui.press('enter')
            for file in glob.glob(new_job_folder + '/' + job[0] + '*' + '/*'):
                if 'Drone' in file:
                    gui.write(file)
            gui.press('enter')
            time.sleep(1)
            for i in range(0,6):
                gui.press('tab')
                time.sleep(.5)
            gui.write('GCP_edit.csv')
            gui.press('enter')
            time.sleep(1)
            gui.press('tab')
            gui.press('enter')
            for i in range(0,6):
                gui.press('tab')
                time.sleep(.5)
            gui.press('enter')

def start_processing(job):
    if job[2] != 'site':
        check_for_image(pixDSMOrthoIndex)
        gui.click()
    else:
        pass
    check_for_image(pixMapperStart)
    gui.click()

def close_pix():
    check_for_image(pixDone)
    gui.hotkey('alt','f4')

def copy_files(job):
    shutil.copytree(pix_project + '\\' + job[0] + '_' + job[2], new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder + '\\' + job[0] + '_' + job[2])

def check_for_image(image):
    checking = True
    while checking:
        image_location = gui.locateCenterOnScreen(image)
        gui.moveTo(image_location)
        if gui.position() == image_location:
            checking = False
