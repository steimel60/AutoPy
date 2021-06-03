#----------------------------------------------------------------
#         Step-by-Step functions for Scene Automation
#----------------------------------------------------------------


##### Import Modules #####
from Settings import *
from scene_pics import *
import re
import glob
import os
import pyautogui as gui
import time
from time import sleep
from datetime import date
import subprocess

screen_center = (gui.size()[0] / 2, (gui.size()[1] / 2) - 50)

#Maximizes application after it starts
def start():
    time.sleep(10)
    gui.press('enter')
    check_for_image(application_png)
    gui.click()
    end = time.time() + 10
    while time.time() < end:
        image_location = gui.locateCenterOnScreen(maximize_png)
        gui.moveTo(image_location)
        if gui.position() == image_location:
            time.sleep(.3)
            gui.click()
            time.sleep(.3)
            break
    gui.click()
    time.sleep(3)

#Closes news pop ups at beginning
def close_pop_ups():
    check_for_image(close_png)
    time.sleep(.3)
    gui.click()

#Creates new project
def new_project(job):
    check_for_image(create_png)
    time.sleep(.3)
    gui.click()
    time.sleep(1)
    for i in range (0,2):
        gui.press('tab')
        time.sleep(.3)
    time.sleep(1)
    gui.write(job[0] + '_' + job[2])
    time.sleep(1)
    for i in range (0,3):
        gui.press('tab')
        time.sleep(.3)
    time.sleep(1)
    gui.press('enter')
    time.sleep(3)

#Loads in scans from local folder
def load_scans(job):
    scan_check = False
    close = False
    for file in glob.glob(new_job_folder + '\\' + job[0] + '_' + job[2] + '\\*'):
        if 'Scans' in file:
            scan_check = True
    if scan_check:
        pass
    else:
        error = 'no Scans folder detected for '
        error_report(job, error)
        close = True
        time.sleep(1)
        return True
    if close == False:
        scan_count = 0
        for file in glob.glob(new_job_folder + '\\' + job[0] + '_' + job[2] + '\\' + 'Scans\\' + job[2] + '\\*'):
            scan_count += 1
        if scan_count > 2:
            check_for_image(import_png)
            time.sleep(.3)
            gui.click()
            check_for_image(importscans_png)
            time.sleep(.3)
            gui.click()
            check_for_image(folder_explorer_png)
            time.sleep(.3)
            gui.mouseDown()
            time.sleep(.3)
            gui.moveTo(screen_center)
            time.sleep(.3)
            gui.mouseUp()
            check_for_image(file_explore_path_png)
            time.sleep(.3)
            gui.click()
            gui.write(new_job_folder + '\\' + job[0] + '_' + job[2] + scan_folder + '\\' + job[2])
            time.sleep(.3)
            gui.press('enter')
            time.sleep(5)
            for i in range (0,3):
                gui.press('tab')
                time.sleep(.3)
            gui.hotkey('ctrl', 'a')
            #drag selected folders to side panel
            check_for_image(selected_png)
            time.sleep(.3)
            gui.mouseDown()
            check_for_image(side_panel_png)
            time.sleep(.3)
            gui.mouseUp()
            check_for_image(cancel_png)
            time.sleep(.3)
            gui.click()
            time.sleep(.3)
            if import_error(job):
                return True
        else:
            error = 'not enough scans for '
            error_report(job, error)
            return True

#Begins processing of scans
def process_scans():
    check_for_image(process_png)
    time.sleep(.3)
    gui.click()
    check_for_image(process_scan_png)
    time.sleep(.3)
    gui.click()
    check_for_image(big_scan_png)
    time.sleep(.3)
    gui.click()
    check_for_image(configure_png)
    time.sleep(.3)
    gui.click()
    time.sleep(2)
    gui.click()

#Checks for error or success
def check_processing(job):
    if handle_errors(job):
        return True

#Creates project point cloud
def create_point_cloud():
    check_for_image(explore_png)
    time.sleep(.3)
    gui.click()
    time.sleep(5)
    check_for_image(pointCloud_png)
    time.sleep(.3)
    gui.click()
    time.sleep(1)
    gui.move(0, 55)
    time.sleep(.3)
    gui.click()
    time.sleep(1)
    gui.press('enter')
    time.sleep(1)
    gui.press('enter')
    check_for_image(cloudDone_png)
    time.sleep(.3)
    gui.press('enter')

#Exports eyz and e57
def export_xyz_e57(job):
    check_for_image(exportTab_png)
    time.sleep(.3)
    gui.click()
    check_for_image(exportPointCloud_png)
    time.sleep(.3)
    gui.click()
    check_for_image(exportDropBox_png)
    time.sleep(.3)
    gui.click()
    time.sleep(1)
    gui.press('e')
    time.sleep(.3)
    gui.press('enter')
    time.sleep(.3)
    gui.press('tab')
    time.sleep(.3)
    gui.write(new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + scene_folder + '\\' + job[0] + '_' + job[2] +'.e57')
    time.sleep(.3)
    gui.press('enter')
    time.sleep(1)
    check_for_image(exportPointCloud_png)
    time.sleep(.3)
    gui.click()
    check_for_image(exportDropBox_png)
    time.sleep(.3)
    gui.click()
    time.sleep(1)
    gui.press('x')
    time.sleep(.3)
    gui.press('enter')
    time.sleep(.3)
    gui.press('tab')
    time.sleep(.3)
    gui.write(new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + scene_folder + '\\' + job[0] + '_' + job[2] +'.xyz')
    time.sleep(.3)
    gui.press('enter')
    time.sleep(.3)
    check_for_exports(job)

#Exports project folder
def export_project(job):
    check_for_image(exportProj_png)
    time.sleep(.3)
    gui.click()
    time.sleep(1)
    #save before export
    gui.press('enter')
    time.sleep(1)
    gui.press('enter')
    time.sleep(2)
    for i in range (0,3):
        gui.press('tab')
        time.sleep(.3)
    time.sleep(1)
    gui.write(new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + scene_folder)
    time.sleep(1)
    gui.press('enter')
    check_for_image(exportSuccess_png)
    time.sleep(.3)
    gui.press('enter')
    #close save success
    check_for_image(lastOk_png)
    time.sleep(.3)
    gui.click()

##### USED IN OTHER FUNCS#####

#Checks for image and moves cursor to location
def check_for_image(image):
    checking = True
    while checking:
        image_location = gui.locateCenterOnScreen(image)
        gui.moveTo(image_location)
        if gui.position() == image_location:
            checking = False

#Wait during processing
def wait_for_load(image):
    waiting = True
    while waiting:
        image_location = gui.locateCenterOnScreen(image)
        if gui.position() != image_location:
            waiting = False

#Deletes imports if error importing
def delete_imports():
    check_for_image(import_png)
    time.sleep(.3)
    gui.click()
    check_for_image(scansMini_png)
    time.sleep(.3)
    gui.click()
    time.sleep(.3)
    gui.press('delete')
    time.sleep(1)
    gui.press('enter')
    time.sleep(.3)

#Begins processing again if error processing
def reprocess(job):
    delete_imports()
    check_for_image(process_png)
    time.sleep(.3)
    gui.click()
    check_for_image(import_png)
    time.sleep(.3)
    gui.click()
    check_for_image(importscans_png)
    time.sleep(.3)
    gui.click()
    check_for_image(folder_explorer_png)
    time.sleep(.3)
    gui.mouseDown()
    gui.moveTo(screen_center)
    time.sleep(.3)
    gui.mouseUp()
    check_for_image(file_explore_path_png)
    time.sleep(.3)
    gui.click()
    gui.write(new_job_folder + '\\' + job[0] + '_' + job[2] + scan_folder + '\\' + job[2])
    time.sleep(.3)
    gui.press('enter')
    check_for_image(folders_png)
    time.sleep(.3)
    gui.click()
    time.sleep(.3)
    gui.hotkey('ctrl', 'a')
    #drag selected folders to side panel
    check_for_image(selected_png)
    time.sleep(.3)
    gui.mouseDown()
    check_for_image(side_panel2_png)
    time.sleep(.3)
    gui.mouseUp()
    check_for_image(cancel_png)
    time.sleep(.3)
    gui.click()
    check_for_image(ok_png)
    time.sleep(.3)
    gui.click()
    check_for_image(process_png)
    time.sleep(.3)
    gui.click()
    check_for_image(process_scan_png)
    time.sleep(.3)
    gui.click()
    check_for_image(big_scan_png)
    time.sleep(.3)
    gui.click()
    check_for_image(configure_png)
    time.sleep(.3)
    gui.click()
    check_for_image(scrollBar_png)
    time.sleep(.3)
    gui.mouseDown()
    time.sleep(.3)
    gui.move(0,300)
    time.sleep(.3)
    gui.mouseUp()
    check_for_image(regMethod_png)
    time.sleep(.3)
    gui.click()
    check_for_image(targetBased_png)
    time.sleep(.3)
    gui.click()
    check_for_image(startProcessing_png)
    time.sleep(.3)
    gui.click()

#Handles errors and reacts accordingly
def handle_errors(job):
    error_check = False
    checking = True
    while checking:
        time_loop = time.time() + 30
        while time.time() < time_loop:
            success = gui.locateCenterOnScreen(process_success_png)
            if success != None:
                gui.moveTo(success)
            if gui.position() == success:
                error_check = False
                checking = False
        next_loop = time.time() + 30
        while time.time() < next_loop:
            failure = gui.locateCenterOnScreen(errorAutoReg_png)
            if failure != None:
                gui.moveTo(failure)
            if gui.position() == failure:
                error_check = True
                checking = False
    check_for_image(ok_png)
    time.sleep(.3)
    gui.click()
    if error_check == True:
        reprocess(job)
        error_check2 = False
        checking2 = True
        while checking2:
            time_loop = time.time() + 30
            while time.time() < time_loop:
                success = gui.locateCenterOnScreen(process_success_png)
                if success != None:
                    gui.moveTo(success)
                if gui.position() == success:
                    error_check2 = False
                    checking2 = False
            next_loop = time.time() + 30
            while time.time() < next_loop:
                failure = gui.locateCenterOnScreen(errorAutoReg_png)
                if failure != None:
                    gui.moveTo(failure)
                if gui.position() == failure:
                    error_check2 = True
                    checking2 = False
        check_for_image(ok_png)
        time.sleep(.3)
        gui.click()
        if error_check2 == True:
            error = 'processing'
            error_report(job, error)
            return True

#Creates error report when error happens
def error_report(job, error):
    today = date.today()
    tdate = today.strftime("%m-%d-%y")
    fileInfo = 'Error ' + error + ' job: ' + job[0] + ' ' + job[2] + '\n'
    savePath = r'Z:\Automation Jobs\Automation Errors'
    fileName = 'Error_Report_' + tdate + '.txt'
    completeName = os.path.join(savePath, fileName)
    f = open(completeName, 'a+')
    f.write(fileInfo)
    f.close()

#Error when importing scans
def import_error(job):
    time_loop = time.time() + 30
    error_flag = False
    while time.time() < time_loop:
        failure = gui.locateCenterOnScreen(errorImport_png)
        if failure != None:
            gui.moveTo(failure)
        if gui.position() == failure:
            error = 'importing scans for'
            error_report(job, error)
            error_flag = True
    check_for_image(ok_png)
    time.sleep(.3)
    gui.click()
    if error_flag == True:
        return True

#Checks files for exports
def check_for_exports(job):
    e57 = False
    xyz = False
    while (e57 == False) or (xyz == False):
        for file in glob.glob(new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + scene_folder + '/*'):
            if file.endswith('.e57'):
                e57 = True
            if file.endswith('.xyz'):
                xyz = True
            time.sleep(2)
