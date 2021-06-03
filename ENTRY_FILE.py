from Settings import *
from deltav_functions import *

#----------------------------------------------------------------
#        This file is where we define Automation Steps
#----------------------------------------------------------------

#----------------------------------------------------------------
#         See deltav_functions for work flow functions
#----------------------------------------------------------------

def automate(job_list):
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
