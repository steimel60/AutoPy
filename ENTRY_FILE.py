from Settings import *
from deltav_functions import *

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
#job_list = [['J8553', CLT, 'site', 'Both'], ['J8553', CLT, 'kenworth', 'Both'], ['J8553', CLT, 'chevy', 'Scene'], ['J8553', CLT, 'hyundai', 'Both']]
#job = [['J9013', NAS, 'site', 'Scene'], ['J7897', CLT, 'volvo', 'Scene']]
#automate(job)
