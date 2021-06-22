import fileinput, os, sys, glob, re, ctypes, threading
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
from Settings import *
from ENTRY_FILE import *
from datetime import date

#--------------------------------------------------------------------------------------------------------------
#                                   Initialize Variables/Lists
#--------------------------------------------------------------------------------------------------------------
#Array of options for location dropdown
locationOptions = [
    'ATL',
    'DEN',
    'NAS',
    'CLT'
]

locationConversion = [
    ATL,
    DEN,
    NAS,
    CLT
]

#Array of options for program dropdown
programOptions = [
    'Scene',
    'Pix4D',
    'Both'
]

#Get todays date
today = date.today()
date = today.strftime("%m-%d-%y")

#Get directory for images
#--------------------------------------------------------------------------------------------------------------
#                                   Initialize Functions
#--------------------------------------------------------------------------------------------------------------
#Gets values from GUI and adds them to text file
def addJob():
    if confirmationBox.isChecked():
        jobInput = jobNumberBox.text()
        locationInput = locationOptions[locations.currentIndex()]
        assetInput = assetBox.text()
        programInput = programOptions[program.currentIndex()]
        if jobInput == '' or assetInput == '':
            return
        fileInfo = jobInput + ',' + locationInput + ',' + assetInput + ',' + programInput + ' '
        savePath = text_path
        fileName = date + '.txt'
        completeName = os.path.join(savePath, fileName)
        f = open(completeName, 'a+')
        f.write(fileInfo)
        f.close()

        jobNumberBox.setText('')
        assetBox.setText('')
        confirmationBox.setChecked(False)
    else:
        pass

checkBox = []
jobList = []
#Loads list of jobs from text file
def loadJobs():
    try:
        textFile = open(text_path + '\\' + date + '.txt', 'r')
        errorLabel.setHidden(True)
    except:
        tab2Layout.addWidget(errorLabel)
        errorLabel.setHidden(False)

    lines = textFile.read().split()
    for i in range(0,len(lines)):
        jobList.append(lines[i].split(','))

    checkBox = []
    for i in range(0,len(jobList)):
        checkBox.append('')

    for i in range(0,len(jobList)):
        checkBox[i]=QCheckBox(jobList[i][0] + ' ' + jobList[i][2] + ' ' + jobList[i][3])

    for box in checkBox:
        tab2Layout.addWidget(box)

    tab2.show()

#Passes list of jobs that are checked by user
def runJobs():
    fullRunList = []
    for n in range(len(checkBox)):
        if (checkBox[n].isChecked()):
            fullRunList.append(jobList[n])
    automate(fullRunList)

#--------------------------------------------------------------------------------------------------------------
#                                   Create GUI Window
#--------------------------------------------------------------------------------------------------------------
app = QApplication(sys.argv)
window = QWidget()
windowLayout = QVBoxLayout()
window.setWindowTitle('AutoPy')
window.setWindowIcon(QIcon("img/AutoPyThumbnail.png"))
window.setFixedWidth(400)
qtRectangle = window.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(centerPoint)
window.move(qtRectangle.topLeft())
window.move(1200, 600)
banner = QLabel()
pixmap = QPixmap("img/AutoPyHeaderNoCherryGore.jpg")
pixmap = pixmap.scaled(380, 700, Qt.KeepAspectRatio, Qt.FastTransformation)
banner.setPixmap(pixmap)
banner.resize(pixmap.width(), pixmap.height())

#--------------------------------------------------------------------------------------------------------------
#                                   Create Widgets
#--------------------------------------------------------------------------------------------------------------
blankLabel = QLabel()
#Tab Widgets
tabWidget = QTabWidget()
tab1 = QWidget()
tab2 = QWidget()
tabWidget.addTab(tab1, 'Task Creator')
tabWidget.addTab(tab2, 'Script Runner')

#Job Number Widgets
jobNumberLabel = QLabel()
jobNumberLabel.setText('Job Number')
jobNumberBox = QLineEdit()
jobNumberBox.setPlaceholderText('Ex: J1234')

#Regions widgets
locationLabel = QLabel()
locationLabel.setText('Region')
locations = QComboBox()
for item in locationOptions:
    locations.addItem(item)

#Asset Widgets
assetLabel = QLabel()
assetLabel.setText('Asset Name')
assetBox = QLineEdit()
assetBox.setPlaceholderText('Ex: Site / Volvo / Lambo')

#Program widgets
programLabel = QLabel()
programLabel.setText('Program')
program = QComboBox()
for item in programOptions:
    program.addItem(item)

#Button Widgets
addJobButton = QPushButton('Add Job')
loadJobsButton = QPushButton('Load Jobs')
runJobsButton = QPushButton('Run Jobs')

errorLabel = QLabel('ERROR: No job list exists')

#Confirmation Box
confirmationBox = QCheckBox('Check to confirm the information entered is correct')

#--------------------------------------------------------------------------------------------------------------
#                                   Make Layout
#--------------------------------------------------------------------------------------------------------------
tab1Layout = QVBoxLayout()
tab2Layout = QVBoxLayout()
tab1Layout.addWidget(jobNumberLabel)
tab1Layout.addWidget(jobNumberBox)
tab1Layout.addWidget(blankLabel)
tab1Layout.addWidget(locationLabel)
tab1Layout.addWidget(locations)
tab1Layout.addWidget(blankLabel)
tab1Layout.addWidget(assetLabel)
tab1Layout.addWidget(assetBox)
tab1Layout.addWidget(blankLabel)
tab1Layout.addWidget(programLabel)
tab1Layout.addWidget(program)
tab1Layout.addWidget(blankLabel)
tab1Layout.addWidget(confirmationBox)
tab1Layout.addWidget(blankLabel)
tab1Layout.addWidget(addJobButton)
tab1.setLayout(tab1Layout)
tab2Layout.addWidget(loadJobsButton)
tab2Layout.addWidget(runJobsButton)
tab2.setLayout(tab2Layout)
windowLayout.addWidget(banner)
windowLayout.addWidget(tabWidget)
window.setLayout(windowLayout)

#--------------------------------------------------------------------------------------------------------------
#                                   Make Connections
#--------------------------------------------------------------------------------------------------------------
addJobButton.clicked.connect(addJob)
loadJobsButton.clicked.connect(loadJobs)
runJobsButton.clicked.connect(runJobs)

#--------------------------------------------------------------------------------------------------------------
#                                   Show GUI Window
#--------------------------------------------------------------------------------------------------------------
window.show()
sys.exit(app.exec_())
