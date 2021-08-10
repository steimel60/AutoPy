#----------------------------------------------------------------
#       Define Step-by-Step Functions for Pix4D Mapper
#----------------------------------------------------------------

##### Import Modules #####
from Settings import *
from pix_mapper_pics import *
import re, glob, os, time, subprocess
import pyautogui as gui
from time import sleep
from datetime import date

#Set variable to get center of screen
screen_center = (gui.size()[0] / 2, (gui.size()[1] / 2) - 50)

#Maximize Pix Mapper after application is started
def start():
    check_for_image(pixApplication)
    gui.click()
    end = time.time() + 10
    while time.time() < end:
        image_location = gui.locateCenterOnScreen(maximize)
        gui.moveTo(image_location)
        if gui.position() == image_location:
            time.sleep(.3)
            gui.click()
            time.sleep(.3)
            break
    gui.click()
    time.sleep(3)

#Create new project
def new_project(job):
    time.sleep(30)
    gui.hotkey('ctrl','n')
    time.sleep(.3)
    gui.write(job[0] + '_' + job[2])
    time.sleep(.3)
    for i in range (0,3):
        gui.press('tab')
        time.sleep(.3)
    gui.press('enter')
    time.sleep(1)
    for i in range (0,2):
        gui.press('tab')
        time.sleep(.3)
    gui.press('enter')
    time.sleep(1)

#Load pictures into project
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
        time.sleep(.3)
        gui.press('enter')
        time.sleep(10)
        gui.press('enter')
        time.sleep(10)
        gui.press('enter')
        time.sleep(10)
        for i in range (0,5):
            gui.press('tab')
            time.sleep(.3)
        time.sleep(10)
        gui.press('enter')
        time.sleep(10)
        gui.press('enter')
        check_for_image(pixProcessingOptions)
        gui.click()
        if job[2] != 'site':
            time.sleep(.3)
            gui.press('down')
        else:
            time.sleep(.3)
            gui.press('down')
            time.sleep(.3)
            gui.press('up')
            time.sleep(.3)
        gui.press('enter')
        time.sleep(.3)
    else:
        error = 'with Drone folder organization for '
        error_report(job, error)
        return True

#If site, import GCP file
def import_gcp(job):
    for file in glob.glob(new_job_folder + '/' + job[0] + '*' + '/Drone/*'):
        if 'GCP_EDIT' in file.upper():
            check_for_image(pixGCP)
            time.sleep(.3)
            gui.click()
            time.sleep(1)
            for i in range (0,3):
                gui.press('tab')
                time.sleep(.3)
            gui.press('enter')
            time.sleep(1)
            for i in range (0,2):
                gui.press('tab')
                time.sleep(.3)
            gui.write('4326')
            time.sleep(.3)
            gui.press('enter')
            time.sleep(1)
            gui.press('enter')
            time.sleep(1)
            gui.press('tab')
            time.sleep(1)
            gui.press('tab')
            time.sleep(.3)
            gui.press('enter')
            time.sleep(.3)
            for i in range (0,6):
                gui.press('tab')
                time.sleep(.3)
            gui.press('up')
            time.sleep(1)
            for i in range (0,2):
                gui.press('tab')
                time.sleep(.3)
            time.sleep(1)
            gui.press('enter')
            time.sleep(1)
            for i in range (0,5):
                gui.press('tab')
                time.sleep(.3)
            gui.press('enter')
            time.sleep(.3)
            #Searches through folders for drone and writes to file
            for file in glob.glob(new_job_folder + '/' + job[0] + '_' + job[2] + '/*'):
                if 'Drone' in file:
                    gui.write(file)
                    time.sleep(.3)
                    break
            gui.press('enter')
            time.sleep(1)
            for i in range(0,6):
                gui.press('tab')
                time.sleep(.3)
            gui.write('GCP_edit.csv')
            time.sleep(.3)
            gui.press('enter')
            time.sleep(1)
            gui.press('tab')
            time.sleep(.3)
            gui.press('enter')
            for i in range(0,6):
                gui.press('tab')
                time.sleep(.3)
            gui.press('enter')
            time.sleep(.3)

#Start proccessing job, if site, do first step, if vehicle, do all 3 steps
def start_processing(job):
    check_for_image(pixDSMOrthoIndex)
    gui.click()
    if job[2] == 'site':
        check_for_image(pixPointCloudMesh)
        time.sleep(.3)
        gui.click()
        pass
    else:
        pass
    check_for_image(pixMapperStart)
    time.sleep(.3)
    gui.click()
    check_for_image(pixDone)

#Copy project files created in processing
def copy_files(job):
    shutil.copytree(pix_project + '\\' + job[0] + '_' + job[2], new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder + '\\' + job[0] + '_' + job[2])
    shutil.copy(pix_project + '\\' + job[0] + '_' + job[2] + '.p4d', new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder )
    return True

#----------------------------------------------------------------
#                    Used in other functions
#----------------------------------------------------------------
#Check for image function to move cursor to image location
def check_for_image(image):
    checking = True
    while checking:
        image_location = gui.locateCenterOnScreen(image)
        gui.moveTo(image_location)
        if gui.position() == image_location:
            checking = False

#Create error report when error is encountered
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
