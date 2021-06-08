from random_pix import *
from random_scene import *
import random

programs = ['scene', 'pix']

for i in range (0, 10):
    run = random.choice(programs)
    if run == 'scene':
        random_scene(1)
    else:
        random_pix(1)
