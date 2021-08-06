#Imports needed libraries
import fileinput, os, sys, subprocess
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pandas as pd

#Creates GUI
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('GCP Converter')
window.setFixedWidth(300)
window.setFixedHeight(100)
qtRectangle = window.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(centerPoint)
window.move(qtRectangle.topLeft())
window.move(1200, 600)

#Variable to hold path to desktop
desktopDir = os.environ['USERPROFILE'] + '\\Desktop'

#Function that retrieves the path to GCP file
def getLocation():
    return GCPZipBox.text()

#Opens file explorer and sets text box to path selected
def openExplorer():
    fileLocation = QFileDialog.getOpenFileName(None, '', desktopDir)[0]
    if fileLocation == "":  # If they cancel the dialog
        return  # Then just don't open anything
    GCPZipBox.setText(fileLocation)

#Pulls only the needed lines out of the GCP file and creates a new one
def convertGCP():
    location = getLocation()
    df = pd.read_csv(location)
    df2 = df[['OBJECTID', 'Latitude', 'Longitude', 'Altitude']].copy().dropna()
    df2.to_csv(desktopDir + '\\' + 'GCP_edit.csv', header = None, index = False)
    GCPZipBox.setText('')

#--------------------------------------------------------------------------------------------------------------
#                                   Create Widgets
#--------------------------------------------------------------------------------------------------------------
GCPZipBox = QLineEdit()
GCPZipBox.setPlaceholderText('Ground_Control_0 File')
fileButton = QPushButton('Open File Explorer')
convertGCPButton = QPushButton('Convert GCP')

#--------------------------------------------------------------------------------------------------------------
#                                   Make Layout
#--------------------------------------------------------------------------------------------------------------
layout = QGridLayout()
layout.addWidget(GCPZipBox, 0, 0, 1, 3)
layout.addWidget(fileButton, 0, 3, 1, 1)
layout.addWidget(convertGCPButton, 1,0,1,4)
window.setLayout(layout)

#--------------------------------------------------------------------------------------------------------------
#                                   Make Connections
#--------------------------------------------------------------------------------------------------------------
fileButton.clicked.connect(openExplorer)
convertGCPButton.clicked.connect(convertGCP)

#--------------------------------------------------------------------------------------------------------------
#                                   Show GUI Window
#--------------------------------------------------------------------------------------------------------------
window.show()
sys.exit(app.exec_())
