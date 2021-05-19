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

jobs = [['J7968', DEN, 'site', 'Pix4D'],['J8553', CLT, 'trailer', 'Pix4D']]
for job in jobs:
    run_pix(job)
