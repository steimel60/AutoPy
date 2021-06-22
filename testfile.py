
##### INPUT CODE TO TEST #####
################ Import Modules ######################
from Settings import *
from scene_pics import *
import scene_funcs as scene
import pix_mapper_funcs as pix
import pyautogui as gui
import os
from datetime import date as dt
import time
from subprocess_maximize import Popen
from time import sleep
from zipfile import ZipFile
import pandas as pd
#import subprocess

############## READ JOBS FROM SERVER TXT FILE #################

currentJobList = [['J8808', CLT, 'Buick', 'Scene']]

today = dt.today()
date = today.strftime("%m-%d-%y")
text_file = open(text_path + '/' + date + '.txt', 'r')
print(text_path + '/' + date + '.txt')
jobList = text_file.read().split()
print(jobList)
text_file.close()

for i in range(0,len(jobList)):
    jobList[i] = jobList[i].split(',')

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

for job in jobList:
    job[0] = job[0].upper()
    job[2] = job[2].lower()

jobList = [job for job in jobList if job not in currentJobList]

text_file = open(text_path + '/' + date + '.txt', 'w+')
print(jobList)
for job in jobList:
    line = job[0] +','+job[1]+','+job[2]+','+job[3]
    text_file.write(line + ' ')

text_file.close()
