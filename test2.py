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

job = ['J8770','CLT','honda','Pix4D']

#shutil.copytree(pix_project + '\\' + job[0] + '_' + job[2], new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder + '\\' + job[0] + '_' + job[2])
shutil.copy(pix_project + '\\' + job[0] + '_' + job[2] + '.p4d', new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder )


#print(pix_project + '\\' + job[0] + '_' + job[2], new_job_folder + '\\' + job[0] + '_' + job[2] + processed_folder + pix4d_folder + '\\' + job[0] + '_' + job[2] + '.p4d')
