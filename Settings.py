import os
import shutil
import glob

####### PATHS TO FILES #######
new_job_template = 'TestTemplate'
user_profile = os.environ['USERPROFILE']

new_job_folder = user_profile + '\\Desktop'
pix_project = user_profile + '\\Documents\\pix4d'

##########APP PATHS###############
scene_path = 'C:\Program Files\FARO\SCENE\SCENE.exe'
pix_path = 'C:\Program Files\Pix4Dmatic\Pix4Dmatic.exe'
pix_mapper_path = 'C:\Program Files\Pix4Dmapper\pix4dmapper.exe'

#######SERVER PATHS#############
CLT = 'Z:\\'
ATL = 'W:\\'
DEN = 'X:\\'
NAS = 'Y:\\'

######## FOLDERS TO FETCH ################
drone_folder = r'\Drone'
scan_folder = r'\Scans'
processed_folder = r'\Processed'
scene_folder = r'\Scene'
pix4d_folder = r'\Pix4D'

#############Text File Path#####################
text_path = 'Z:\\Automation Jobs\\Automation Tasks'
