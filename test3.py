import os
from Settings import *
import time

import subprocess
p = subprocess.Popen(scene_path)
time.sleep(5)
p.terminate()
