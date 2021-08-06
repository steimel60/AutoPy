#Import other python files
from Settings import *
from deltav_functions import *

#----------------------------------------------------------------
#        This file is where we define Automation Steps
#----------------------------------------------------------------

#----------------------------------------------------------------
#         See deltav_functions for work flow functions
#----------------------------------------------------------------

#Carry out all automation steps
def automate(job_list):
    ############## String to Path #################
    for job in job_list:
        job[0] = job[0].upper()
        job[2] = job[2].lower()
        if job[1] == 'CLT':
            job[1] = CLT
        elif job[1] == 'DEN':
            job[1] = DEN
        elif job[1] == 'ATL':
            job[1] = ATL
        elif job[1] == 'NAS':
            job[1] = NAS
    ############ COPY FILES FROM SERVER ############
    create_local_files(job_list)
    ################# RUN JOBS #####################
    for job in job_list:
        if job[3] == 'Scene':
            run_scene(job)
        elif job[3] == 'Pix4D':
            run_pix(job)
        else:
            run_scene(job)
            run_pix(job)

    job_list = updateList(job_list)
    if len(job_list) != 0:
        automate(job_list)

running = True
while running:
    try:
        today = dt.today()
        date = today.strftime("%m-%d-%y")
        text_file = open(text_path + '/' + date + '.txt', 'r')
        jobList = text_file.read().split()
        text_file.close()

        if len(jobList) > 0:
            for i in range(0,len(jobList)):
                jobList[i] = jobList[i].split(',')

            automate(jobList)
    except:
        pass
