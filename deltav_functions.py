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
        shutil.copytree(new_job_template, new_job_folder + '\\' + job[0] + '_' + job[2])
        #Copy Drone Data
        i = 0
        for file in glob.glob(job[1] + '/' + job[0] + '*' + '/*Drone*/*'):
            ind = str(i)
            name = file.lower()
            if job[2] in name:
                shutil.copytree(file, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\' + job[2] + '\\' + ind + job[2])
                i += 1
        #Copy Scan Data
        i = 0
        for file in glob.glob(job[1] + '/' + job[0] + '*' + '/Scans/*'):
            ind = str(i)
            name = file.lower()
            if (job[2] in name) and ('fls' in name):
                shutil.copytree(file, new_job_folder + '\\' + job[0] + '_' + job[2] + scan_folder + '\\' + job[2] + '\\' + ind + job[2])
                i += 1
        get_gcp(job)

################## RUN SCENE #####################
def run_scene(job):
    running = True
    while running:
        #open FARO
        scene.start()
        #Close license warning and pop up
        scene.close_pop_ups()
        #Open New Project
        scene.new_project(job)
        #Load in scans
        if scene.load_scans(job) == True:
            scene.close_scene()
            running = False
            break
        #Processing The Scans
        scene.process_scans()
        if scene.check_processing(job) == True:
            scene.close_scene()
            running = False
            break
        #Export after Successful Processing
        scene.create_point_cloud()
        scene.export_xyz_e57(job)
        scene.export_project(job)
        if scene.close_scene() == True:
            running = False
            break

################## RUN PIX #####################
def run_pix(job):
    #Open Pix4DMapper
    pix.start()
    #Create new project
    pix.new_project(job)
    #Load in drone pictures
    pix.load_pics(job)
    #Get GCP
    pix.import_gcp(job)
    #Start processing all 3 steps
    pix.start_processing(job)
    #Once done processing close Pix4DMapper
    pix.close_pix()
    #Copy project to processed folders
    pix.copy_files(job)

################## GET GCP #####################
def get_gcp(job):
    for file in glob.glob(job[1] + job[0] + '*' + '/*GCP*/*'):
        name = file.lower()
        if 'zip' in name:
            shutil.copy(file, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder)
    # Create a ZipFile Object and load sample.zip in it
            with ZipFile(file, 'r') as zipObj:
               # Get a list of all archived file names from the zip
               listOfFileNames = zipObj.namelist()
               # Iterate over the file names
               for fileName in listOfFileNames:
                   # Check filename endswith csv
                   #print(fileName)
                   if fileName.endswith('.csv'):
                       # Extract a single file from zip
                       zipObj.extract(fileName, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder)
                       df = pd.read_csv(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\'+ fileName)
                       #create upload file
                       df2 = df[['OBJECTID', 'Latitude', 'Longitude', 'Altitude']].copy()
                       df2.to_csv(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\' + 'GCP_edit.csv', header = None, index = False)
