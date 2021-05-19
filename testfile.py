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


job = ['J8808',CLT,'site','Pix4D']
pix.import_gcp(job)
