from Settings import *
from scene_pics import *
import re
import glob
import os
import pyautogui as gui
import scene_funcs as scene
import time
from time import sleep
from datetime import date


job = ['J7968',DEN,'chevy','Scene']
scene.export_xyz_e57(job)
scene.export_project(job)
