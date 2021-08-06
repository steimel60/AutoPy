#Imports all needed libraries
import fileinput, os, sys, glob, re, ctypes, threading
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
from Settings import *
from datetime import date

#--------------------------------------------------------------------------------------------------------------
#                                   Initialize Variables/Lists
#--------------------------------------------------------------------------------------------------------------
#Array of options for location dropdown
locationOptions = ['ATL', 'DEN', 'NAS', 'CLT']

#Array of locations to pass
locationConversion = [ATL, DEN, NAS, CLT]

#Array of options for program dropdown
programOptions = ['Scene', 'Pix4D', 'Both']

#Get todays date
today = date.today()
date = today.strftime("%m-%d-%y")

#--------------------------------------------------------------------------------------------------------------
#                                   Initialize Functions
#--------------------------------------------------------------------------------------------------------------
#Gets values from GUI and adds them to text file
def addJob():
    #Check if confirmation box is checked before writing to file
    if confirmationBox.isChecked():
        #Get values from text boxes and dropdowns
        jobInput = jobNumberBox.text().strip()
        locationInput = locationOptions[locations.currentIndex()]
        assetInput = assetBox.text().strip()
        programInput = programOptions[program.currentIndex()]

        if jobInput == '' or assetInput == '':
            return
        fileInfo = jobInput + ',' + locationInput + ',' + assetInput + ',' + programInput + ' '
        savePath = text_path
        fileName = date + '.txt'
        completeName = os.path.join(savePath, fileName)

        #Open text file and write inputted information into it
        f = open(completeName, 'a+')
        f.write(fileInfo)
        f.close()

        #Reset text boxes to be blank
        jobNumberBox.setText('')
        assetBox.setText('')
        confirmationBox.setChecked(False)

    #If confirmation box is not checked then it does nothing
    else:
        pass

#--------------------------------------------------------------------------------------------------------------
#                                   Create GUI Window
#--------------------------------------------------------------------------------------------------------------
#Creates GUI, adds image, sets size, and moves it to center
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
tabWidget.addTab(tab1, 'Task Creator')

#Job Number Widgets
jobNumberLabel = QLabel()
jobNumberLabel.setText('Job Number')
jobNumberBox = QLineEdit()
jobNumberBox.setPlaceholderText('Ex: J1234')

#Regions widgets
locationLabel = QLabel()
locationLabel.setText('Region')
locations = QComboBox()
#Create dropdown list for region options
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
#Create dropdown list for program options
for item in programOptions:
    program.addItem(item)

#Button Widgets
addJobButton = QPushButton('Add Job')
loadJobsButton = QPushButton('Load Jobs')
runJobsButton = QPushButton('Run Jobs')

#Error if no list exists
errorLabel = QLabel('ERROR: No job list exists')

#Confirmation Box
confirmationBox = QCheckBox('Check to confirm the information entered is correct')

#--------------------------------------------------------------------------------------------------------------
#                                   Make Layout
#--------------------------------------------------------------------------------------------------------------
#Create vertical box layout and add everything to the layout
tab1Layout = QVBoxLayout()
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
windowLayout.addWidget(banner)
windowLayout.addWidget(tabWidget)
window.setLayout(windowLayout)

#--------------------------------------------------------------------------------------------------------------
#                                   Make Connections
#--------------------------------------------------------------------------------------------------------------
#Carries out function when button is clicked
addJobButton.clicked.connect(addJob)

#--------------------------------------------------------------------------------------------------------------
#                                   Show GUI Window
#--------------------------------------------------------------------------------------------------------------
window.show()
sys.exit(app.exec_())
