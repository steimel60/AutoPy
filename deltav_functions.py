#----------------------------------------------------------------
#           This file defines work flow functions
#----------------------------------------------------------------

#----------------------------------------------------------------
#     See scene_funcs and pix_funcs for step by step functions
#----------------------------------------------------------------


################ Import Modules ######################
from Settings import *
from scene_pics import *
import scene_funcs as scene
import pix_mapper_funcs as pix
import pyautogui as gui
import os
from datetime import date as dt
import time
from time import sleep
from zipfile import ZipFile
import pandas as pd
import subprocess

############## READ JOBS FROM SERVER TXT FILE #################
def find_jobs():
    today = dt.today()
    date = today.strftime("%m-%d-%y")
    text_file = open(text_path + date + '.txt', 'r')
    list = text_file.read().split()

    list_o_jobs = []
    scene_jobs = []
    pix4d_jobs = []

    for job in list:
        job2 = job.split(',')
        list_o_jobs.append(job2)
    for job in list_o_jobs:
        job[0] = job[0].upper()
    for job in list_o_jobs:
        if job[1] == 'CLT':
            job[1] = CLT
        elif job[1] == 'DEN':
            job[1] = DEN
        elif job[1] == 'ATL':
            job[1] = ATL
        elif job[1] == 'NAS':
            job[1] = NAS
    for job in list_o_jobs:
        job[2] = job[2].lower()
    for job in list_o_jobs:
        if job[3] == 'Scene':
            scene_jobs.append(job)
        if job[3] == 'Pix4D':
            pix4d_jobs.append(job)
        if job[3] == 'Both':
            scene_jobs.append(job)
            pix4d_jobs.append(job)

    return list_o_jobs, scene_jobs, pix4d_jobs

########### COPY JOB DATA FROM SERVER TO LOCAL FOLDER ###############
def create_local_files(job_list):
    for job in job_list:
        #Create Local Folder
        try:
            shutil.copytree(new_job_template, new_job_folder + '\\' + job[0] + '_' + job[2])
            #Copy Drone Data
            i = 0
            if job[3] != 'Scene':
                print('Fetching Drone Folder')
                for file in glob.glob(job[1] + '/' + job[0] + '*' + '/*Drone*/*'):
                    ind = str(i)
                    name = file.lower()
                    if job[2].lower() in name:
                        shutil.copytree(file, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\' + job[2] + '\\' + ind + job[2])
                        i += 1

                print('Searching for GCP job: ' + job[0])
                get_gcp(job)
                print('Copying drone data for job: ' + job[0])
            #Copy Scan Data
            i = 0
            if job[3] != 'Pix4D':
                print('Copying scan data for job: ' + job[0])
                for file in glob.glob(job[1] + '/' + job[0] + '*' + '/*Scan*/*'):
                    ind = str(i)
                    name = file.lower()
                    if (job[2].lower() in name) and (name.endswith('fls')):
                        shutil.copytree(file, new_job_folder + '\\' + job[0] + '_' + job[2] + scan_folder + '\\' + job[2] + '\\' + ind + job[2])
                        i += 1
            print('')
        except Exception as e:
            scene.error_report(job, str(e))

################## RUN SCENE #####################
def run_scene(job):
    running = True
    while running:
        #open FARO
        print('Starting job: ' + job[0])
        window = subprocess.Popen(scene_path)
        scene.start()
        #Close license warning and pop up
        print('Closing pop ups')
        #scene.close_pop_ups()
        #Open New Project
        print('Opening new project')
        scene.new_project(job)
        #Load in scans
        print('Opening new scans')
        if scene.load_scans(job) == True:
            print('Closing Scene\n')
            window.terminate()
            running = False
            break
        #Processing The Scans
        print('Processing scans')
        scene.process_scans()
        if scene.check_processing(job) == True:
            print('Closing Scene\n')
            window.terminate()
            running = False
            break
        print('Creating point cloud')
        scene.create_point_cloud()
        #Export after Successful Processing
        print('Exporting xyz and e57')
        scene.export_xyz_e57(job)
        print('Exporting project')
        scene.export_project(job)
        print('Scene process successful :)\n\n')
        window.terminate()
        running = False

################## RUN PIX #####################
def run_pix(job):
    running = True
    while running:
        #Open Pix4DMapper
        print('Opening Pix4D')
        window = subprocess.Popen(pix_mapper_path)
        pix.start()
        #Create new project
        print('Creating new project')
        pix.new_project(job)
        #Load in drone pictures
        print('Loading in drone images')
        if pix.load_pics(job) == True:
            print('Closing pix')
            window.terminate()
            running = False
            break
        #Get GCP
        if job[2] == 'site':
            print('Importing GCP')
            pix.import_gcp(job)
        #Start processing all 3 steps
        print('Starting processing')
        pix.start_processing(job)
        #Copy project to processed folders
        print('Copying files')
        if pix.copy_files(job) == True:
            running = False
            break
        #Once done processing close Pix4DMapper
        print('Pix process successful :)\n\n')
        window.terminate()

################## GET GCP #####################
def get_gcp(job):
    if job[2] == 'site':
        print('Searching for GCP folder')
        for file in glob.glob(job[1] + job[0] + '*' + '/*GCP*/*'):
            name = file.lower()
            if 'zip' in name:
                print('Found zip')
                shutil.copy(file, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder)
        # Create a ZipFile Object and load sample.zip in it
                with ZipFile(file, 'r') as zipObj:
                   # Get a list of all archived file names from the zip
                   listOfFileNames = zipObj.namelist()
                   # Iterate over the file names
                   print('Searching for csv')
                   for fileName in listOfFileNames:
                       # Check filename endswith csv
                       if fileName.endswith('.csv'):
                           print('Found csv')
                           print('Extracting stuff')
                           # Extract a single file from zip
                           zipObj.extract(fileName, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder)
                           df = pd.read_csv(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\'+ fileName)
                           #create upload file
                           df2 = df[['OBJECTID', 'Latitude', 'Longitude', 'Altitude']].copy().dropna()
                           print('Creating new csv')
                           df2.to_csv(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\' + 'GCP_edit.csv', header = None, index = False)
