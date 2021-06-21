#----------------------------------------------------------------
#                   Run random jobs in Pix4D
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

##### Init Job list and set total job number #####
job_list = []
total_jobs = 10

##### Run random jobs #####
for i in  range(0,total_jobs):
    drone_exist = False
    job = random.choice(os.listdir(CLT))
    if job[0] == 'J':
        pass
    else:
        i -= 1
        continue
    job_match = re.search('(J\d*)', job)
    print(job)
    job_num =  job_match.group(1)
    for file in glob.glob(CLT + job + '/*'):
        if 'drone' in file.lower():
            drone_folder = file
            drone_exist = True
    if drone_exist:
        sorted = False
        asset_list = []
        for file in glob.glob(drone_folder + '/*'):
            for new_file in glob.glob(file + '/*'):
                if new_file.endswith('.JPG'):
                    sorted = True
                if sorted:
                    asset_match = re.search('\\.*([a-zA-Z]*)$', file)
                    asset = asset_match.group(1)
                    if (asset not in asset_list) and (asset != ''):
                        asset_list.append(asset)
        for asset in asset_list:
            full_job = [job_num,CLT,asset,'Pix4D']
            job_list.append(full_job)
        if not sorted:
            print(job_num + ' drone folder organization incompatible')
    else:
        print('No drone folder')

    automate(job_list)
