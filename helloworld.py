import os
import shutil

OG = r'C:\Users\DylanSteimel\Desktop\Template'

New = r'C:\Users\DylanSteimel\Desktop\New_Job'

new_job = shutil.copytree(OG, New)
