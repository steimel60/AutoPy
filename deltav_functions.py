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
import os, time
from datetime import date as dt
from subprocess_maximize import Popen
from time import sleep
from zipfile import ZipFile
import pandas as pd

############## READ JOBS FROM SERVER TXT FILE #################
def updateList(currentJobList):
    #Open text file and store information
    today = dt.today()
    date = today.strftime("%m-%d-%y")
    text_file = open(text_path + '/' + date + '.txt', 'r')
    print(text_path + '/' + date + '.txt')
    jobList = text_file.read().split()
    print(jobList)
    text_file.close()

    #Split list with commas
    for i in range(0,len(jobList)):
        jobList[i] = jobList[i].split(',')

    #Convert locations for searching
    print(jobList)
    for job in currentJobList:
        job[0] = job[0].upper()
        job[2] = job[2].lower()
        if job[1] == CLT:
            job[1] = 'CLT'
        elif job[1] == DEN:
            job[1] = 'DEN'
        elif job[1] == ATL:
            job[1] = 'ATL'
        elif job[1] == NAS:
            job[1] = 'NAS'

    #Standardize capitalization
    for job in jobList:
        job[0] = job[0].upper()
        job[2] = job[2].lower()

    #Add jobs in list if not in current list
    jobList = [job for job in jobList if job not in currentJobList]

    #Open file and write jobs to it
    text_file = open(text_path + '/' + date + '.txt', 'w+')
    print(jobList)
    for job in jobList:
        line = job[0] +','+job[1]+','+job[2]+','+job[3]
        text_file.write(line + ' ')

    text_file.close()

    return jobList


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
        window = Popen(scene_path, show='maximize')
        time.sleep(30)
        #Close license warning and pop up
        print('Closing pop ups')
        scene.close_pop_ups()
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
        window = Popen(pix_mapper_path, show='maximize')
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
        #Copy project to processed folders and close pix
        print('Copying files')
        if pix.copy_files(job) == True:
            running = False
            print('Pix process successful :)\n\n')
            window.terminate()
            break

################## GET GCP #####################
def get_gcp(job):
    if job[2] == 'site':
        print('Searching for GCP folder')
        for file in glob.glob(job[1] + job[0] + '*' + '/*GCP*/*'):
            name = file.lower()
            if 'zip' in name:
                print('Found zip')
                shutil.copy(file, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder)
                #Create a ZipFile Object and load sample.zip in it
                with ZipFile(file, 'r') as zipObj:
                   #Get a list of all archived file names from the zip
                   listOfFileNames = zipObj.namelist()
                   #Iterate over the file names
                   print('Searching for csv')
                   for fileName in listOfFileNames:
                       #Check filename endswith csv
                       if fileName.endswith('.csv'):
                           print('Found csv')
                           print('Extracting stuff')
                           #Extract a single file from zip
                           zipObj.extract(fileName, new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder)
                           df = pd.read_csv(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\'+ fileName)
                           #Create upload file
                           df2 = df[['OBJECTID', 'Latitude', 'Longitude', 'Altitude']].copy().dropna()
                           print('Creating new csv')
                           df2.to_csv(new_job_folder + '\\' + job[0] + '_' + job[2] + drone_folder + '\\' + 'GCP_edit.csv', header = None, index = False)
