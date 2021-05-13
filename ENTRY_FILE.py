from Settings import *
from deltav_functions import *

scene_list = []
pix4d_list = []
job_list = []


def automate(job_list):
    ########GET LIST OF JOBS TO PROCESS############
    #job_list, scene_list, pix4d_list = find_jobs()

    ############ COPY FILES FROM SERVER ############
    create_local_files(job_list)

    ################# RUN JOBS #####################
    for job in job_list:
        if job[3] == 'Scene':
            run_scene(job)
            #print('run scene ' + str(job))
        elif job[3] == 'Pix4D':
            print('Run pix ' + str(job))
        else:
            run_scene(job)
            print('Run Pix4D ' + str(job))
    #job = ['J8808', CLT, 'buick']
    #run_scene(job)
