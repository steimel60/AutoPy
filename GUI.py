import tkinter as tk
from tkinter import *
from datetime import date
import ctypes, threading, sys, re, os
import ENTRY_FILE
from Settings import *

#create GUI
gui = Tk()
gui.title('Job List Maker')
gui.geometry('300x500')
gui.configure(bg='#292d34')
windowWidth = gui.winfo_reqwidth()
windowHeight = gui.winfo_reqheight()
positionRight = int(gui.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(gui.winfo_screenheight()/3 - windowHeight/2)
gui.geometry("+{}+{}".format(positionRight, positionDown))
gui.resizable(False, False)

#Get todays date
today = date.today()
date = today.strftime("%m-%d-%y")

#Array of options for location dropdown
locationOptions = [
    'ATL',
    'DEN',
    'NAS',
    'CLT'
]

#Array of options for program dropdown
programOptions = [
    'Scene',
    'Pix4D',
    'Both'
]

#Function to add jobs to text file
def addFile():
    fileInfo = jobInput + ',' + locationInput + ',' + assetInput + ',' + programInput + ' '
    savePath = text_path
    fileName = date + '.txt'
    completeName = os.path.join(savePath, fileName)
    f = open(completeName, 'a+')
    f.write(fileInfo)
    f.close()
    jobBox.delete('1.0', END)
    assetBox.delete('1.0', END)

#Function to check input of text box
def checkJob():
    global jobInput, assetInput, locationInput, programInput
    jobInput = jobBox.get("1.0",'end-1c')
    locationInput = locationPlaceholder.get()
    assetInput = assetBox.get("1.0",'end-1c')
    programInput = programPlaceholder.get()
    #Checks for correct input and give popup on incorrect input
    if jobInput.isalnum() and assetInput.isalnum():
        addFile()
    else:
        for i in range(11):
            if i%11 == 0:
                popup = ctypes.windll.user32.MessageBoxW
                threading.Thread(target = lambda :popup(None, '\t Invalid Input\n\n      Letters and numbers only.\n       Must not contain spaces.', 'Error', 0)).start()
        jobBox.delete('1.0', END)
        assetBox.delete('1.0', END)

#Job Number Text Box
jobLabel = Label(gui, text='Job Number')
jobLabel.configure(bg='#302c34', fg='white', font='bold')
jobBox = Text(gui, bg='white', height=1, width=10, padx=5, pady=5)
jobLabel.pack()
jobLabel.place(y=20, x=105)
jobBox.pack()
jobBox.place(y=45, x=105)

#Job Location Dropdown
locationLabel = Label(gui, text='Job Location')
locationLabel.configure(bg='#302c34', fg='white', font='bold')
locationPlaceholder = StringVar()
locationPlaceholder.set('ATL')
locationDrop = OptionMenu(gui, locationPlaceholder,  *locationOptions)
locationLabel.pack()
locationLabel.place(y=100, x=102)
locationDrop.pack()
locationDrop.place(y=125, x=117)

#Vehicle Text Box
assetLabel = Label(gui, text='Asset Name')
assetLabel.configure(bg='#302c34', fg='white', font='bold')
assetBox = Text(gui, bg='white', height=1, width=10, padx=5, pady=5)
assetLabel.pack()
assetLabel.place(y=180, x=105)
assetBox.pack()
assetBox.place(y=205, x=105)

#Program Dropdown
programLabel = Label(gui, text='Program')
programLabel.configure(bg='#302c34', fg='white', font='bold')
programPlaceholder = StringVar()
programPlaceholder.set('Scene')
programDrop = OptionMenu(gui, programPlaceholder,  *programOptions)
programLabel.pack()
programLabel.place(y=260, x=110)
programDrop.pack()
programDrop.place(y=285, x=110)

#Add to File Button
addFileButton = tk.Button(gui, text='Add Job', padx=10, pady=5, fg='black', bg='#889099', command=checkJob, font='bold')
addFileButton.pack()
addFileButton.place(y=400, x=105)

gui.mainloop()
