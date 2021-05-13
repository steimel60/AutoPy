import tkinter as tk
from tkinter import *
from datetime import date
import ctypes, threading, sys, re, os
from ENTRY_FILE import *
from Settings import *
from PIL import Image, ImageTk


def confirmList():
    fullRunList = []
    for n in range(len(check)):
        if (var[n].get() == 1):
            fullRunList.append(jobs[n])
    automate(fullRunList)

job_list, scene_list, pix4d_list = find_jobs()

#create GUI
gui = Tk()
gui.title('Automation Script')
#gui.geometry('355x160')
gui.geometry('803x680')
gui.configure(bg='#292d34')
windowWidth = gui.winfo_reqwidth()
windowHeight = gui.winfo_reqheight()
positionRight = int(gui.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(gui.winfo_screenheight()/3 - windowHeight/2)
gui.geometry("+{}+{}".format(positionRight, positionDown))

###### Logo Image ######
logo_img = PhotoImage(file='img\\DeltaV_logo.png')
img = ImageTk.PhotoImage(Image.open('img\\DeltaV_logo.png'))
panel = tk.Label(gui, image = img)
panel.pack(side = "top")

#Title for program
programLabel = Label(gui, text='FARO Scene Automation Script')
programLabel.configure(bg='#302c34', fg='#fafafa', font=('Arial', 20, 'bold'))
programLabel.pack()
programLabel.place(y=240, x=200)

#Start Script Button
addFileButton = tk.Button(gui, text='Start', padx=10, pady=5, fg='black', bg='#889099', command=confirmList, font=('Arial', 14, 'bold'))
addFileButton.pack()
addFileButton.place(y=300, x=355)


#Create check boxes
check = []
var = []
jobs = []
i = 0
z = 25
for job in job_list:
    jobs.append(job)
    var.append(str(i))
    var[i] = tk.IntVar()
    box = tk.Checkbutton(gui, text=job[0] + ' ' + job[2] + ' ' + job[3], variable=var[i], onvalue=1, offvalue=0)
    check.append(box)
    check[i].pack()
    check[i].place(y=370+z*i, x=300)
    i+=1
