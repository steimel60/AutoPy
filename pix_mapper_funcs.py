from Settings import *
from pix_mapper_pics import *
import re
import glob
import os
import pyautogui as gui
import time
from time import sleep
from datetime import date
import subprocess

screen_center = (gui.size()[0] / 2, (gui.size()[1] / 2) - 50)

def start():
    window = subprocess.Popen(pix_mapper_path)
    time.sleep(8)
    check_for_image(pixBeforeNew)
    gui.click()

def new_project(job):
    check_for_image(pixBeforeNew)
    gui.click()
    gui.hotkey('ctrl','n')
    gui.write(job[0] + '_' + job[2])
    gui.press('tab', presses=3)
    gui.press('enter')
    time.sleep(1)
    gui.press('tab', presses=2)
    gui.press('enter')
    time.sleep(1)

def load_pics(job):
    JPGs = []
    drone_check = 0
    for file in glob.glob(new_job_folder + '\\' + job[0] + '_' + job[2] + '\\*'):
        if 'Drone' in file:
            drone_check += 1
    if drone_check > 0:
        pass
    else:
        error = 'no Drone folder detected for '
        error_report(job, error)
        return True
    for file in glob.glob(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\' + job[2] + '\\' + '0' + job[2] + '\\*'):
        if file.endswith('.JPG'):
            JPGs.append(file)
    if len(JPGs) > 0:
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
        time.sleep(15)
        if job[2] != 'site':
            gui.press('down')
        else:
            gui.press('down')
            gui.press('up')
        gui.press('enter')
    else:
        error = 'with Drone folder organization for '
        error_report(job, error)
        return True

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
            time.sleep(1)
            gui.press('enter')
            time.sleep(1)
            gui.press('tab', presses=5)
            gui.press('enter')
            for file in glob.glob(new_job_folder + '/' + job[0] + '_' + job[2] + '/*'):
                if 'Drone' in file:
                    gui.write(file)
                    break
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
    #check_for_image(pixDSMOrthoIndex)
    #gui.click()
    if job[2] == 'site':
        check_for_image(pixPointCloudMesh)
        gui.click()
        pass
    else:
        pass
    check_for_image(pixMapperStart)
    gui.click()
    check_for_image(pixDone)

def close_pix():
    window.terminate()

def copy_files(job):
    shutil.copytree(pix_project + '\\' + job[0] + '_' + job[2], new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder + '\\' + job[0] + '_' + job[2])
    shutil.copy(pix_project + '\\' + job[0] + '_' + job[2] + '.p4d', new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder )
    return True

def check_for_image(image):
    checking = True
    while checking:
        image_location = gui.locateCenterOnScreen(image)
        gui.moveTo(image_location)
        if gui.position() == image_location:
            checking = False

def error_report(job, error):
    today = date.today()
    tdate = today.strftime("%m-%d-%y")
    fileInfo = 'Error ' + error + 'job: ' + job[0] + ' ' + job[2] + '\n'
    savePath = r'Z:\Automation Jobs\Automation Errors'
    fileName = 'Error_Report_' + tdate + '.txt'
    completeName = os.path.join(savePath, fileName)
    f = open(completeName, 'a+')
    f.write(fileInfo)
    f.close()
