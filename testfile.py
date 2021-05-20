from Settings import *
from scene_pics import *
from deltav_functions import *
from ENTRY_FILE import *
import re
import glob
import os
import pyautogui as gui
import scene_funcs as scene
import time
from time import sleep
from datetime import date
import random



job_list = []
scans_exist = False
for i in  range(0,20):
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

for job in job_list:
    print(job)
automate(job_list)
