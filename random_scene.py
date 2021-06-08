#----------------------------------------------------------------
#                    Run random Scene jobs
#----------------------------------------------------------------


##### Import Modules #####
from Settings import *
from scene_pics import *
from ENTRY_FILE import *
import scene_funcs as scene
import pix_mapper_funcs as pix
import pyautogui as gui
import os, time, random, re
from datetime import date as dt
from time import sleep
from datetime import date


##### Init Job list and choose number of jobs run #####
job_list = []
total_jobs = 10


##### Run Random Jobs #####
for i in  range(0,total_jobs):
    scans_exist = False
    job = random.choice(os.listdir(CLT))
    if job[0] == 'J':
        pass
    else:
        i -= 1
        continue
    job_match = re.search('(J\d*)', job)
    print(job)
    job_num =  job_match.group(1)

    #### Check that random folder has scans ####
    for file in glob.glob(CLT + job + '/*'):
        if 'scan' in file.lower():
            scan_folder = file
            scans_exist = True
    if scans_exist:
        sorted = False
        asset_list = []
        for file in glob.glob(scan_folder + '/*'):
            if file.endswith('.fls'):
                sorted = True
                asset_match = re.search('([a-zA-Z]*)_*\d*\.fls', file)
                asset = asset_match.group(1)
                if (asset not in asset_list) and (asset != ''):
                    asset_list.append(asset)
        for asset in asset_list:
            full_job = [job_num,CLT,asset,'Scene']
            job_list.append(full_job)
        if not sorted:
            print(job_num + ' scans folder organization incompatible')
    else:
        print('No scan folder')
        i -= 1

    automate(job_list)

random_scene(5)
