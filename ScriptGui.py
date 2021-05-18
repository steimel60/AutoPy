import tkinter as tk
from tkinter import *
from datetime import date
import ctypes, threading, sys, re, os
from ENTRY_FILE import *
from Settings import *
from PIL import Image, ImageTk

#Get list of jobs from text file
def find_jobs():
    today = date.today()
    tdate = today.strftime("%m-%d-%y")
    text_file = open(text_path + '\\' + tdate + '.txt', 'r')
    list = text_file.read().split()

    list_o_jobs = []
    scene_jobs = []
    pix4d_jobs = []

    for job in list:
        job2 = job.split(',')
        list_o_jobs.append(job2)

    for job in list_o_jobs:
        job[0] = job[0].upper()
    for job in list_o_jobs:
        if job[1] == 'CLT':
            job[1] = CLT
        elif job[1] == 'DEN':
            job[1] = DEN
        elif job[1] == 'ATL':
            job[1] = ATL
        elif job[1] == 'NAS':
            job[1] = NAS
    for job in list_o_jobs:
        job[2] = job[2].lower()
    for job in list_o_jobs:
        if job[3] == 'Scene':
            scene_jobs.append(job)
        if job[3] == 'Pix4D':
            pix4d_jobs.append(job)
        if job[3] == 'Both':
            scene_jobs.append(job)
            pix4d_jobs.append(job)

    return list_o_jobs, scene_jobs, pix4d_jobs

#Passes list of jobs that are checked by user
def confirmList():
    fullRunList = []
    for n in range(len(jobs)):
        if (var[n].get() == 1):
            fullRunList.append(jobs[n])
    automate(fullRunList)

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in gui
    gui.configure(scrollregion=gui.bbox('all'))

#Various declarations
job_list, scene_list, pix4d_list = find_jobs()
check = []
var = []
jobs = []
i = 0
z = 50

#create GUI
gui = Tk()
gui.title('Automation Script')
gui.geometry('803x600')
gui.configure(bg='#292d34')
windowWidth = gui.winfo_reqwidth()
windowHeight = gui.winfo_reqheight()
positionRight = int(gui.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(gui.winfo_screenheight()/3 - windowHeight/2)
gui.geometry("+{}+{}".format(positionRight, positionDown))
gui.resizable(False, False)

#Logo Image
img = ImageTk.PhotoImage(Image.open('img\\DeltaV_logo.png'))
panel = tk.Label(gui, image = img)
panel.pack(side = 'top')

#Title for program
programLabel = Label(gui, text='Automation Script')
programLabel.configure(bg='#292d34', fg='#fafafa', font=('Aerial', 20, 'bold'), pady=20)
programLabel.pack()

#Start Script Button
addFileButton = tk.Button(gui, text='Start', padx=10, pady=5, fg='black', bg='#889099', command=confirmList, font=('Aerial', 14, 'bold'))
addFileButton.pack()

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y",  expand="false")
        self.canvas = tk.Canvas(self,bg='#292d34', bd=0, height=350, highlightthickness=0, yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")
        self.canvas.place(x=290,y=20)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        self.bind('<Configure>', self.set_scrollregion)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def set_scrollregion(self, event=None):
        #Set the scroll region on the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

checkbox_pane = ScrollableFrame(gui, bg='#292d34')
checkbox_pane.pack(expand="true", fill="both")

job_list, scene_list, pix4d_list = find_jobs()
check = []
var = []
jobs = []
i = 0
z = 50

for job in job_list:
    jobs.append(job)
    var.append(str(i))
    var[i] = tk.IntVar(value=1)
    box = tk.Checkbutton(checkbox_pane.interior, text=job[0] + ' ' + job[2] + ' ' + job[3], variable=var[i], onvalue=1, offvalue=0)
    box.configure(bg='#292d34', fg='#fafafa', font=('Aerial', 12, 'bold'), selectcolor='black')
    box.pack()
    i+=1

gui.mainloop()
