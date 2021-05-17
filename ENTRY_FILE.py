from Settings import *
from deltav_functions import *
from new_deltav_functions import run_pix

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
            run_pix(job)
        else:
            run_scene(job)
            run_pix(job)
job_list = [['J8553', CLT, 'kenworth', 'Both'], ['J8553', CLT, 'chevy', 'Both'], ['J8553', CLT, 'hyundai', 'Both']]

automate(job_list)
