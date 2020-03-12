# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 09:51:31 2017

@author: v-stpurc
"""
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QRadioButton, QVBoxLayout, QCheckBox, QProgressBar,
    QGroupBox, QComboBox, QLineEdit, QPushButton, QMessageBox, QInputDialog, QDialog, QDialogButtonBox, QSlider)
from PyQt5.QtGui import QIcon, QPainter, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot

sys.path.append("C:\\Users\\v-stpur\\Documents\\XBoxScripts\\instrument_Libraries")

import visa
#import time
#import threading 
import waveFormLib
import chromaLib
import tekScopeLib
#import xlsxwriter
import timerThread
import dutInfoDialog

version_Info = "Python PyQt5 Slammer Frequency Sweep V0.1"

        
class MainWindow(QWidget):

    StartFreq = 0
    StopFreq = 0
    Steps = 0
    logSteps = 0
    
    Scope = 0
    Waveform = 0
    Load = 0
    
    slammer = 0

    duty = 0
    edgeTimes = 0
    amplitude = 0
    configID = 0
    pcbaSN = 0
    productSN = 0
    scopeType = 0
    probeType = 0 
    runNotes = 0 
    vregText = 0 
    vregSelection = 0
    frequencySweep = False
    logSweep = False
    sweepWidth = 0
#    workBook = 0 
#    workSheet = 0 
    vout_DC_Value = 0  
    limitsGood = 0 
    

    sense_Resistor = 0
    
    slamLoad = 0
    chromaLoad = 0
    chromaStartLoad = 0
    chromaStopLoad = 0
    
    scopeShot_Signal = pyqtSignal(str)
    dutyCycle_Signal = pyqtSignal(str, int)
    edgeTime_Signal = pyqtSignal(str, int)
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.initUI()
#        self.openInstruments()
#        self.createRadioButtonGroup()
#        #Bring up a default look on scope
#        self.configureScope()
 
       
    def initUI(self):
        
        self.setGeometry(300, 300, 1000, 300)
        self.setWindowTitle('Micro Slammer Frequency Sweep Test For All Rails')
        self.setWindowIcon(QIcon('xbox_icon.ico')) 
        
        scopeLabel = QLabel(self)
        scopeLabel.move(10,10)
        scopeLabel.setText("Scope")
    
        waveformLabel = QLabel(self)
        waveformLabel.move(10,25)
        waveformLabel.setText("Waveform Generator")
    
        loadLabel = QLabel(self)
        loadLabel.move(10,40)
        loadLabel.setText("Chroma Load")
  
#        self.scopeInstr = QLabel(self)
#        self.scopeInstr.setGeometry(150, 10, 1000, 10)
#        self.scopeInstr.setText("Scope")
    
#        self.waveformInstr = QLabel(self)
#        self.waveformInstr.setGeometry(150, 25, 1000, 10)
#        self.waveformInstr.setText("Waveform Generator")
    
#        self.loadInstr = QLabel(self)
#        self.loadInstr.setGeometry(150, 40, 1000, 10)
#        self.loadInstr.setText("Chroma Load")

        self.scopeIDN = QLabel(self)
        self.scopeIDN.setGeometry(150, 10, 1000, 10)
        self.scopeIDN.setText("Scope")
    
        self.waveformIDN = QLabel(self)
        self.waveformIDN.setGeometry(150, 25, 1000, 10)
        self.waveformIDN.setText("Waveform Generator")
    
        self.loadIDN = QLabel(self)
        self.loadIDN.setGeometry(150, 40, 1000, 10)
        self.loadIDN.setText("Chroma Load")
        
        self.slammerGroupBox = QGroupBox(self)
        self.slammerGroupBox.setGeometry(10, 65, 120, 65)
        self.slammerGroupBox.setTitle("Slammer Selection")
        
        self.enableExtraFeatures = QCheckBox('Enable Extra Features', self)
        self.enableExtraFeatures.move(500, 10)
        self.enableExtraFeatures.stateChanged.connect(self.extraFeatures)
        
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(500, 40, 500, 10)
        
        self.progressLabel = QLabel(self)
        self.progressLabel.setGeometry(700, 22, 100, 10)
        self.progressLabel.setText("Test Progress")
         

        
        vregLabel = QLabel(self)
        vregLabel.setGeometry(150, 60, 80, 20)
        vregLabel.setText("Vreg Selection")
        
        self.vregComboBox = QComboBox(self)
        self.vregComboBox.setGeometry(150, 85, 80, 20)
        
        self.vregComboBox.addItem("V_MEMPHY")
        self.vregComboBox.addItem("V_MEMIO")
        self.vregComboBox.addItem("V_3P3")
        self.vregComboBox.addItem("V_FUSE")
        self.vregComboBox.addItem("V_SOCPHY")
        self.vregComboBox.addItem("V_SOC1P8")
        self.vregComboBox.addItem("V_SOC")
        self.vregComboBox.addItem("V_GFXCORE")
        self.vregComboBox.addItem("V_CPUCORE")
        self.vregComboBox.setCurrentIndex(7)
        
        self.vregComboBox.currentIndexChanged.connect(self.vregSelectionChange)

        slamLabel = QLabel(self)
        slamLabel.setGeometry(250, 60, 80, 20)
        slamLabel.setText("Slammer Load")
        
        self.slamComboBox = QComboBox(self)
        self.slamComboBox.setGeometry(250, 85, 60, 20)
        
        self.slamComboBox.addItem("350")
        self.slamComboBox.addItem("300")
        self.slamComboBox.addItem("254")
        self.slamComboBox.addItem("191")
        self.slamComboBox.addItem("180")
        self.slamComboBox.addItem("170")
        self.slamComboBox.addItem("160")
        self.slamComboBox.addItem("150")
        self.slamComboBox.addItem("140")
        self.slamComboBox.addItem("130")
        self.slamComboBox.addItem("127")
        self.slamComboBox.addItem("110")
        self.slamComboBox.addItem("100")
        self.slamComboBox.addItem("90")
        self.slamComboBox.addItem("80")
        self.slamComboBox.addItem("70")
        self.slamComboBox.addItem("64")
        self.slamComboBox.addItem("60")
        self.slamComboBox.addItem("50")
        self.slamComboBox.addItem("40")
        self.slamComboBox.addItem("25")
        self.slamComboBox.addItem("20")
        self.slamComboBox.addItem("10")
       
        self.slamComboBox.currentIndexChanged.connect(self.slamSelectionChange)

        chromaLabel = QLabel(self)
        chromaLabel.setGeometry(335, 60, 80, 20)
        chromaLabel.setText("Chroma Load")
        
        self.chromaComboBox = QComboBox(self)
        self.chromaComboBox.setGeometry(335, 85, 60, 20)
        
        self.chromaComboBox.addItem("0")
        self.chromaComboBox.addItem("5A")
        self.chromaComboBox.addItem("10A")
        self.chromaComboBox.addItem("15A")
        self.chromaComboBox.addItem("20A")
       
        self.chromaComboBox.currentIndexChanged.connect(self.chromaSelectionChange)

        self.chromaStartLabel = QLabel(self)
        self.chromaStartLabel.setGeometry(400, 230, 120, 20)
        self.chromaStartLabel.setText("Start Chroma Load")
        self.chromaStartLabel.setEnabled(False)
        
        self.chromaStartComboBox = QComboBox(self)
        self.chromaStartComboBox.setGeometry(400, 255, 60, 20)
        
        self.chromaStartComboBox.addItem("0")
        self.chromaStartComboBox.addItem("0.5A")
        self.chromaStartComboBox.addItem("1A")
    #    self.chromaComboBox.addItem("20A")
        self.chromaStartComboBox.setEnabled(False)
       
        self.chromaStartComboBox.currentIndexChanged.connect(self.chromaStartSelectionChange)

        self.chromaStopLabel = QLabel(self)
        self.chromaStopLabel.setGeometry(500, 230, 120, 20)
        self.chromaStopLabel.setText("End Chroma Load")
        self.chromaStopLabel.setEnabled(False)
        
        self.chromaStopComboBox = QComboBox(self)
        self.chromaStopComboBox.setGeometry(500, 255, 60, 20)
        
        self.chromaStopComboBox.addItem("0.5A")
        self.chromaStopComboBox.addItem("1A")
        self.chromaStopComboBox.addItem("1.5A")
    #    self.chromaComboBox.addItem("20A")
        self.chromaStopComboBox.setEnabled(False)
       
        self.chromaStopComboBox.currentIndexChanged.connect(self.chromaStopSelectionChange)

        startFreqLabel = QLabel(self)
        startFreqLabel.setGeometry(420, 60, 95, 20)
        startFreqLabel.setText("Starting Frequency")
        
        self.startFreqLineEdit = QLineEdit(self)
        self.startFreqLineEdit.setGeometry(420, 85, 95, 20)
        self.startFreqLineEdit.setText("10000")
        
        stopFreqLabel = QLabel(self)
        stopFreqLabel.setGeometry(535, 60, 95, 20)
        stopFreqLabel.setText("Ending Frequency")
        
        self.stopFreqLineEdit = QLineEdit(self)
        self.stopFreqLineEdit.setGeometry(535, 85, 95, 20)
        self.stopFreqLineEdit.setText("130000")
        
        stepsLabel = QLabel(self)
        stepsLabel.setGeometry(650, 60, 150, 20)
        stepsLabel.setText("Number of Frequency Steps")
        
        self.logFreqCheckBox = QCheckBox('Log Frequency Sweep', self)
        self.logFreqCheckBox.move(650, 110)
        self.logFreqCheckBox.stateChanged.connect(self.logFrequencyStep)
        self.logFreqCheckBox.setEnabled(True)
        self.logFreqCheckBox.setChecked(False)
        
        self.stepsLineEdit = QLineEdit(self)
        self.stepsLineEdit.setGeometry(650, 85, 95, 20)
        self.stepsLineEdit.setText("60")
        
        self.startStopButton = QPushButton('Start Test', self)
        self.startStopButton.setGeometry(800, 70, 180, 50)
#        self.startStopButton.setCheckable(True)

        self.font = QFont()
        self.font.setBold(True)
        self.font.setPointSize(16)
        self.startStopButton.setFont(self.font)
        self.startStopButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.startStopButton.setText("Start Test")
        self.startStopButton.clicked[bool].connect(self.startStopTest)
        
        #Use Dual Slammer by Default
        self.slammer = 2
        
        self.pictureLabel = QLabel(self)
        self.pictureLabel.setGeometry(10, 140, 200, 150)
        self.pictureLabel.setText("Current Scope Shot")
        self.pictureLabel.setScaledContents(True)
        pixmap = QPixmap("xbox_icon.ico")
        self.pictureLabel.setPixmap(pixmap)

        self.stepLabel = QLabel(self)
        self.stepLabel.setGeometry(230, 140, 150, 15)
        self.stepLabel.setText("Step")

        self.freqLabel = QLabel(self)
        self.freqLabel.setGeometry(230, 160, 150, 15)
        self.freqLabel.setText("Frequency")

        self.pktopkLabel = QLabel(self)
        self.pktopkLabel.setGeometry(230, 180, 150, 15)
        self.pktopkLabel.setText("Peak to Peak")

        self.maxLabel = QLabel(self)
        self.maxLabel.setGeometry(230, 200, 150, 15)
        self.maxLabel.setText("Maximum")

        self.minLabel = QLabel(self)
        self.minLabel.setGeometry(230, 220, 150, 15)
        self.minLabel.setText("Minimum")

        self.overLabel = QLabel(self)
        self.overLabel.setGeometry(230, 240, 150, 15)
        self.overLabel.setText("Overshoot")

        self.underLabel = QLabel(self)
        self.underLabel.setGeometry(230, 260, 150, 15)
        self.underLabel.setText("Undershoot")
        
        self.dutyCycleSlider = QSlider(Qt.Horizontal, self)
        self.dutyCycleSlider.setFocusPolicy(Qt.NoFocus)
        self.dutyCycleSlider.setRange(1, 50)
        self.dutyCycleSlider.setValue(50)
        self.dutyCycleSlider.setGeometry(720, 150, 200, 20)
        self.dutyCycleSlider.setEnabled(False)
        self.dutyCycleSlider.valueChanged[int].connect(self.dutyChanged)
        
        self.dutyLabel = QLabel(self)
        self.dutyLabel.setGeometry(795, 134, 100, 15)
        self.dutyLabel.setText("Duty Cycle")

        self.dutyLineEdit = QLineEdit(self)
        self.dutyLineEdit.setGeometry(930, 150, 50, 20)
        self.dutyLineEdit.setText("50%")
        self.dutyLineEdit.setReadOnly(True)

        self.edgeTimeSlider = QSlider(Qt.Horizontal, self)
        self.edgeTimeSlider.setFocusPolicy(Qt.NoFocus)
        self.edgeTimeSlider.setRange(3, 5000)
        self.edgeTimeSlider.setValue(200)
        self.edgeTimeSlider.setGeometry(720, 180, 200, 20)
        self.edgeTimeSlider.setEnabled(False)
        self.edgeTimeSlider.valueChanged[int].connect(self.edgeTimeChanged)
        
        self.edgeTimeLabel = QLabel(self)
        self.edgeTimeLabel.setGeometry(795, 164, 100, 15)
        self.edgeTimeLabel.setText("Edge Times")

        self.edgeTimeLineEdit = QLineEdit(self)
        self.edgeTimeLineEdit.setGeometry(930, 180, 50, 20)
        self.edgeTimeLineEdit.setText("200ns")
        self.edgeTimeLineEdit.setReadOnly(True)

        self.sweepWidthSlider = QSlider(Qt.Horizontal, self)
        self.sweepWidthSlider.setFocusPolicy(Qt.NoFocus)
        self.sweepWidthSlider.setRange(100, 10000)
        self.sweepWidthSlider.setValue(1000)
        self.sweepWidthSlider.setGeometry(720, 210, 200, 20)
        self.sweepWidthSlider.setEnabled(False)
        self.sweepWidthSlider.valueChanged[int].connect(self.sweepWidthChanged)
        
        self.sweepWidthLabel = QLabel(self)
        self.sweepWidthLabel.setGeometry(795, 194, 100, 15)
        self.sweepWidthLabel.setText("Sweep Width")

        self.sweepWidthLineEdit = QLineEdit(self)
        self.sweepWidthLineEdit.setGeometry(930, 210, 50, 20)
        self.sweepWidthLineEdit.setText("1000Hz")
        self.sweepWidthLineEdit.setReadOnly(True)

        self.singleFreqCheckBox = QCheckBox('Single Frequency Slam', self)
        self.singleFreqCheckBox.move(400, 150)
        self.singleFreqCheckBox.stateChanged.connect(self.singleFrequencySlam)
        self.singleFreqCheckBox.setEnabled(False)
        self.singleFreqCheckBox.setChecked(False)
        
        self.font.setPointSize(14)
        self.scopeShotButton = QPushButton('Get Scope Shot', self)
        self.scopeShotButton.setGeometry(530, 143, 160, 30)
        self.scopeShotButton.setFont(self.font)
        self.scopeShotButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.scopeShotButton.clicked[bool].connect(self.getScopeShot)
        self.scopeShotButton.setEnabled(False)
        self.scopeShotButton.setStyleSheet("background-color: lightgray")
        
        self.useChromaCheckBox = QCheckBox('Use Chroma Load', self)
        self.useChromaCheckBox.move(400, 180)
        self.useChromaCheckBox.stateChanged.connect(self.chromaLoadSlam)
        self.useChromaCheckBox.setEnabled(False)
        self.useChromaCheckBox.setChecked(False)
            
        self.useChromaSlam = False
 
        self.frequencySweepCheckBox = QCheckBox('Frequency Sweep', self)
        self.frequencySweepCheckBox.move(400, 210)
        self.frequencySweepCheckBox.stateChanged.connect(self.sweepFrequencySlam)
        self.frequencySweepCheckBox.setEnabled(False)
        self.frequencySweepCheckBox.setChecked(False)
 
        self.font.setPointSize(12)
        self.quitButton = QPushButton('Quit', self)
        self.quitButton.setFont(self.font)
        self.quitButton.setGeometry(890, 260, 100, 30)
        self.quitButton.clicked[bool].connect(self.closeEvent)

        self.show()

    def closeEvent(self, event):
        self.close()

    def getScopeShot(self):
#        print "get scope shot"
        returnString = self.startStopButton.text()
        if returnString.find("Start Test") != -1:
            QMessageBox.about(self, "Test Not Started","Click the Start Test Button Before Capturing Scope Shot")
        else:
            self.scopeShot_Signal.emit('hi from main thread')
            self.scopeShotButton.setEnabled(False)
            self.scopeShotButton.setStyleSheet("background-color: lightgray")

    def singleFrequencySlam(self):
        if self.singleFreqCheckBox.isChecked():
#            print "do single Freq"
            self.stopFreqLineEdit.setEnabled(False)
            self.stopFreqLineEdit.clear()
            self.stepsLineEdit.setEnabled(False)
            self.stepsLineEdit.clear()
            self.scopeShotButton.setEnabled(True)
            self.scopeShotButton.setStyleSheet("background-color: yellow")
        
            self.frequencySweepCheckBox.setEnabled(False)
            self.frequencySweepCheckBox.setChecked(False)
            self.sweepWidthSlider.setEnabled(False)
        else:
#            print "don't do single Freq"
            self.stopFreqLineEdit.setEnabled(True)
            self.stepsLineEdit.setEnabled(True)
            self.scopeShotButton.setEnabled(False)
            self.scopeShotButton.setStyleSheet("background-color: lightgray")
             
            self.frequencySweepCheckBox.setEnabled(True)
            self.frequencySweepCheckBox.setChecked(False)
            
    def logFrequencyStep(self):
        if self.logFreqCheckBox.isChecked():
            self.logFreqCheckBox.setChecked(True)
            self.logSweep = True
        else:
            self.logFreqCheckBox.setChecked(False)
            self.logSweep = False

    def chromaLoadSlam(self):
        
        self.slamComboBox.setEnabled(False)
        self.chromaComboBox.setEnabled(False)

        if self.useChromaCheckBox.isChecked():
            self.chromaStartLabel.setEnabled(True)
            self.chromaStartComboBox.setEnabled(True)
            self.chromaStopLabel.setEnabled(True)
            self.chromaStopComboBox.setEnabled(True)
            self.useChromaSlam = True
        else:
            self.chromaStartLabel.setEnabled(False)
            self.chromaStartComboBox.setEnabled(False)
            self.chromaStopLabel.setEnabled(False)
            self.chromaStopComboBox.setEnabled(False)
            self.useChromaSlam = False
            
        if self.singleFreqCheckBox.isChecked():
#            print "do single Freq"
            self.stopFreqLineEdit.setEnabled(False)
            self.stopFreqLineEdit.clear()
            self.stepsLineEdit.setEnabled(False)
            self.stepsLineEdit.clear()
            self.scopeShotButton.setEnabled(True)
            self.scopeShotButton.setStyleSheet("background-color: yellow")
        
            self.frequencySweepCheckBox.setEnabled(False)
            self.frequencySweepCheckBox.setChecked(False)
            self.sweepWidthSlider.setEnabled(False)
        else:
#            print "don't do single Freq"
            self.stopFreqLineEdit.setEnabled(True)
            self.stepsLineEdit.setEnabled(True)
            self.scopeShotButton.setEnabled(False)
            self.scopeShotButton.setStyleSheet("background-color: lightgray")
             
            self.frequencySweepCheckBox.setEnabled(True)
            self.frequencySweepCheckBox.setChecked(False)
           
    def sweepFrequencySlam(self):
        if self.frequencySweepCheckBox.isChecked():
#            print "do single Freq"
            self.stopFreqLineEdit.setEnabled(True)
#            self.stopFreqLineEdit.clear()
            self.stepsLineEdit.setEnabled(True)
#            self.stepsLineEdit.clear()
#            self.scopeShotButton.setEnabled(True)
#            self.scopeShotButton.setStyleSheet("background-color: yellow")
             
            self.scopeShotButton.setEnabled(False)
            self.scopeShotButton.setStyleSheet("background-color: lightgray")
       
            self.singleFreqCheckBox.setEnabled(False)
            self.singleFreqCheckBox.setChecked(False)
            
            self.frequencySweep = True
            self.sweepWidthSlider.setEnabled(True)
        else:
#            print "don't do single Freq"
            self.stopFreqLineEdit.setEnabled(True)
            self.stepsLineEdit.setEnabled(True)
            self.scopeShotButton.setEnabled(False)
            self.scopeShotButton.setStyleSheet("background-color: lightgray")
             
            self.singleFreqCheckBox.setEnabled(True)
            self.singleFreqCheckBox.setChecked(False)
             
            self.frequencySweep = False
            self.sweepWidthSlider.setEnabled(False)
          
    def sweepWidthChanged(self):
        sweepWidth = self.sweepWidthSlider.value()        
        self.sweepWidthLineEdit.setText(str(sweepWidth) + "Hz")

    def dutyChanged(self):
        dutyCycle = self.dutyCycleSlider.value()        
        self.dutyLineEdit.setText(str(dutyCycle) + "%")
#        print "get scope shot"
#        returnString = self.startStopButton.text()
#        if returnString.find("Start Test") != -1:
#            QMessageBox.about(self, "Test Not Started","Click the Start Test Button Before Capturing Scope Shot")
#        else:
#            self.dutyCycle_Signal.emit('Changing duty cycle to' + str(dutyCycle) + "%", dutyCycle)
        self.dutyCycle_Signal.emit('Changing duty cycle to' + str(dutyCycle) + "%", dutyCycle)
      
    def edgeTimeChanged(self):
        edgeTime = self.edgeTimeSlider.value()        
        self.edgeTimeLineEdit.setText(str(edgeTime) + "ns")
#        returnString = self.startStopButton.text()
#        if returnString.find("Start Test") != -1:
#            QMessageBox.about(self, "Test Not Started","Click the Start Test Button Before Capturing Scope Shot")
#        else:
#            self.edgeTime_Signal.emit('Changing edge time to' + str(edgeTime) + "s", edgeTime)
        self.edgeTime_Signal.emit('Changing edge time to' + str(edgeTime) + "s", edgeTime)
        
    def extraFeatures(self):
        print ("enable/disable extra features")
        if self.enableExtraFeatures.isChecked():
            self.dutyCycleSlider.setEnabled(True)
            self.edgeTimeSlider.setEnabled(True)
            self.singleFreqCheckBox.setEnabled(True)
            self.useChromaCheckBox.setEnabled(True)
            self.frequencySweepCheckBox.setEnabled(True)
            self.frequencySweepCheckBox.setChecked(False)

        else:
            self.dutyCycleSlider.setEnabled(False)
            self.edgeTimeSlider.setEnabled(False)
            self.dutyCycleSlider.setValue(50)
            self.edgeTimeSlider.setValue(200)
            self.dutyLineEdit.setText("50%")
            self.edgeTimeLineEdit.setText("200ns")
            self.singleFreqCheckBox.setEnabled(False)
            self.singleFreqCheckBox.setChecked(False)
            self.stopFreqLineEdit.setEnabled(True)
            self.useChromaCheckBox.setEnabled(False)
            self.useChromaCheckBox.setChecked(False)
            self.frequencySweepCheckBox.setEnabled(False)
            self.frequencySweepCheckBox.setChecked(False)
            self.chromaStartLabel.setEnabled(False)
            self.chromaStartComboBox.setEnabled(False)

    def runLoop(self, stepCount, fileName, frequency, pktopk, maximum, minimum, overshoot, undershoot):
        pixmap = QPixmap(fileName)
        self.pictureLabel.setPixmap(pixmap)
        self.progressBar.setValue(int(stepCount))
        self.stepLabel.setText  ("Step:\t\t" + str(stepCount))
        self.freqLabel.setText  ("Frequency:\t" + str(frequency))
        self.pktopkLabel.setText("Peak to Peak:\t" + str(pktopk))
        self.maxLabel.setText   ("Maximum:\t" + str(maximum))
        self.minLabel.setText   ("Minimum:\t\t" + str(minimum))
        self.overLabel.setText  ("Overshoot:\t" + str(overshoot))
        self.underLabel.setText ("Undershoot:\t" + str(undershoot))

        if self.singleFreqCheckBox.isChecked():
            self.scopeShotButton.setEnabled(True)
            self.scopeShotButton.setStyleSheet("background-color: yellow")

    def quitLoop(self):
        
        self.progressBar.setValue(0)
        pixmap = QPixmap("xbox_icon.ico")
        self.pictureLabel.setPixmap(pixmap)
        self.stepLabel.setText  ("Step:")
        self.freqLabel.setText  ("Frequency:")
        self.pktopkLabel.setText("Peak to Peak:")
        self.maxLabel.setText   ("Maximum:")
        self.minLabel.setText   ("Minimum:")
        self.overLabel.setText  ("Overshoot:")
        self.underLabel.setText ("Undershoot:")

#        chromaLib.setLoadOff(self.Load, 1)
#        chromaLib.setLoadOff(self.Load, 5)
#        chromaLib.setLoadOff(self.Load, 9)
#        waveFormLib.pulseGen_Set_OutputOff(self.Waveform)
        
        self.startStopButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.startStopButton.setText("Start Test")
        
        self.thread.quit()
        print("Got quit signal")
        while self.thread.isFinished():
            print ("thread still here after quit")

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False   
        
    def configureScope(self):
                
        returnString = self.Scope.query("*IDN?")
        if returnString.find("4104") != -1:
            mSO58 = False
            mSO4104 = True
            mSO3014 = False
            self.messageXpos = 650
            self.messageYpos = 720
        elif returnString.find("3014") != -1:
            mSO58 = False
            mSO4104 = False
            mSO3014 = True
            self.messageXpos = 20
            self.messageYpos = 20
        elif returnString.find("MSO58") != -1:
            mSO58 = True
            mSO4104 = False
            mSO3014 = False
            self.messageXpos = 20
            self.messageYpos = 20

        self.vregText = self.vregComboBox.currentText()
        tekScopeLib.scope_SetAnnotation(self.Scope, self.vregText, self.messageXpos, self.messageYpos)
#        tekScopeLib.scope_SetChannel_Label(self.Scope, "CH1", self.vregText)
        tekScopeLib.scope_SetChannel_OnOff(self.Scope, "CH1", "ON")
        if mSO4104 or mSO3014:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH1", "1")
        elif mSO58:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH1", "0")
            
#        tekScopeLib.scope_SetChannel_Label(self.Scope, "CH2", "V_12PO_GFXCPU_SW1 @ C185")
        tekScopeLib.scope_SetChannel_OnOff(self.Scope, "CH2", "ON")
        if mSO4104 or mSO3014:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH2", "-3")
        elif mSO58:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH2", "0")
#        tekScopeLib.scope_SetChannel_Label(self.Scope, "CH3", "Slam_Sense")
        tekScopeLib.scope_SetChannel_OnOff(self.Scope, "CH3", "ON")
        if mSO4104 or mSO3014:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH3", "-2")
        elif mSO58:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH3", "0")
#        tekScopeLib.scope_SetChannel_Label(self.Scope, "CH4", "Sig Gen")
        tekScopeLib.scope_SetChannel_OnOff(self.Scope, "CH4", "ON")
        if mSO4104 or mSO3014:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH4", "-4")
        elif mSO58:
            tekScopeLib.scope_SetChannel_Position(self.Scope, "CH4", "0")
         
        tekScopeLib.scope_SetChannel_Bandwidth(self.Scope, "CH1", "TWEnty")
        tekScopeLib.scope_SetChannel_Bandwidth(self.Scope, "CH2", "TWEnty")
        tekScopeLib.scope_SetChannel_Bandwidth(self.Scope, "CH3", "TWEnty")
        tekScopeLib.scope_SetChannel_Bandwidth(self.Scope, "CH4", "TWEnty")
        
        if mSO58:
            tekScopeLib.scope_List_Measurements(self.Scope)
            tekScopeLib.scope_Delete_Measurements(self.Scope)
        
        # Channel Measurements
        # tekScopeLib.scope_Set_Measurement(scopeObject, measNumber, channel, measurement)
        tekScopeLib.scope_Set_Measurement(self.Scope, 1, 1, "MINIMUM")  #Ch1 Vreg Out
        tekScopeLib.scope_Set_Measurement(self.Scope, 2, 1, "MAXIMUM")  #
        tekScopeLib.scope_Set_Measurement(self.Scope, 3, 1, "MEAN")     #
        tekScopeLib.scope_Set_Measurement(self.Scope, 4, 1, "pk2pk")    #
        tekScopeLib.scope_Set_Measurement(self.Scope, 5, 2, "MAXIMUM")  #Ch2 Input 1
        tekScopeLib.scope_Set_Measurement(self.Scope, 6, 2, "MINIMUM")  #
        tekScopeLib.scope_Set_Measurement(self.Scope, 7, 2, "MEAN")     #
        tekScopeLib.scope_Set_Measurement(self.Scope, 8, 2, "pk2pk")    #
        tekScopeLib.scope_Set_Measurement(self.Scope, 9, 3, "MAXIMUM")  #Ch3 Slam Sense
        tekScopeLib.scope_Set_Measurement(self.Scope, 10, 3, "pk2pk")   #
        tekScopeLib.scope_Set_Measurement(self.Scope, 11, 3, "TOP")     #
        tekScopeLib.scope_Set_Measurement(self.Scope, 12, 3, "BASE")    #
        tekScopeLib.scope_Set_Measurement(self.Scope, 13, 3, "RISETIME")#
        tekScopeLib.scope_Set_Measurement(self.Scope, 14, 3, "FALLTIME")#
        tekScopeLib.scope_Set_Measurement(self.Scope, 15, 4, "RISETIME")#
        tekScopeLib.scope_Set_Measurement(self.Scope, 16, 4, "FALLTIME")#
#        tekScopeLib.scope_Set_Measurement(self.Scope, 17, 5, "MAXIMUM") #Ch5 Input 2
#        tekScopeLib.scope_Set_Measurement(self.Scope, 18, 5, "MINIMUM") #
#        tekScopeLib.scope_Set_Measurement(self.Scope, 19, 5, "MEAN")    #
#        tekScopeLib.scope_Set_Measurement(self.Scope, 20, 5, "pk2pk")   #
#        tekScopeLib.scope_Set_Measurement(self.Scope, 27, 6, "MAXIMUM") #Ch6 Input 3
#        tekScopeLib.scope_Set_Measurement(self.Scope, 28, 6, "MINIMUM") #
#        tekScopeLib.scope_Set_Measurement(self.Scope, 29, 6, "MEAN")    #
#        tekScopeLib.scope_Set_Measurement(self.Scope, 30, 6, "pk2pk")   #    
#        tekScopeLib.scope_Set_Measurement(self.Scope, 31, 7, "MAXIMUM") #Ch7 Input 4
#        tekScopeLib.scope_Set_Measurement(self.Scope, 32, 7, "MINIMUM") #
#        tekScopeLib.scope_Set_Measurement(self.Scope, 33, 7, "MEAN")    #
#        tekScopeLib.scope_Set_Measurement(self.Scope, 37, 7, "pk2pk")   #
        
        
        tekScopeLib.scope_Set_Statistics_Off(self.Scope)
        
    def startStopTest(self):
        returnString = self.startStopButton.text()
        if returnString.find("Start Test") != -1:
        
            dialog = dutInfoDialog.DutInfoDialog()
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()
            self.configID, self.pcbaSN, self.productSN, self.scopeType, self.probeType, self.runNotes, self.sense_Resistor = dialog.returnInfo()
 
            print ("Test Started")

            self.startStopButton.setStyleSheet('QPushButton {background-color: #FF2000; color: black;}')
            self.startStopButton.font()
            self.startStopButton.setText("Abort Test")
            
            self.limitsGood = False
            if self.checkFreqLimits() == True:
                self.limitsGood = True
                print("limits Ok")
                
                self.vregText = self.vregComboBox.currentText()
                self.vregSelection = self.vregComboBox.currentIndex()
        
#                self.duty = 50
                self.amplitude = 0.1
                self.slamLoad = self.slamComboBox.currentText()
                self.chromaLoad = self.chromaComboBox.currentText()
                
                self.startThread()
            else:
                print("limits bad")
                #Recursive call seems to work for now
                self.startStopTest()
        else:
            print ("Test Aborted")
            self.startStopButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
            self.startStopButton.setText("Start Test")

            if self.limitsGood:
                self.thread.quit()
                self.work.stopTimer()
#               self.work.startStop = False

    def startThread(self):

        if self.singleFreqCheckBox.isChecked():
            self.StopFreq = 0
            self.Steps = 0
        
        self.duty = self.dutyCycleSlider.value()
        self.edgeTimes = self.edgeTimeSlider.value()
        self.sweepWidth = self.sweepWidthSlider.value()
        
        parameterArray = [self.Scope, self.Load, self.Waveform, self.StartFreq, self.StopFreq, self.Steps, self.vregSelection,
                          self.vregText, self.configID, self.pcbaSN, self.productSN, self.scopeType, self.probeType, self.runNotes,
                          self.duty, self.edgeTimes, self.amplitude, self.slammer, self.sense_Resistor, self.slamLoad, self.chromaLoad,
                          self.frequencySweep, self.sweepWidth, self.chromaStartLoad, self.chromaStopLoad, self.useChromaSlam, self.logSweep]
#        self.work = TimerThread(self.Scope, self.Load, self.Waveform, self.StartFreq, self.StopFreq, self.Steps, self.vregSelection) 
        self.work = timerThread.TimerThread(parameterArray) 
        self.work.timerSignal.connect(self.runLoop)
        self.work.quitSignal.connect(self.quitLoop)
        self.scopeShot_Signal.connect(self.work.scopeShot_Slot)
        self.dutyCycle_Signal.connect(self.work.dutyCycle_Slot)
        self.edgeTime_Signal.connect(self.work.edgeTime_Slot)
        self.thread = QThread()

        self.work.moveToThread(self.thread)
        self.thread.started.connect(self.work.run)
        self.thread.start()

    def checkFreqLimits(self):
        returnString = self.startFreqLineEdit.text()
        if self.is_number(returnString): 
            self.StartFreq = float(returnString)
            if self.StartFreq < 1000 or self.StartFreq > 500000:
                QMessageBox.about(self, "Start Frequency Error","Start frequency must be between 1000 and 500000")
                return False
            print (self.StartFreq)
        else:
            QMessageBox.about(self, "Start Frequency Error","Start frequency entry is not a number")
            return False
                
        if self.singleFreqCheckBox.isChecked() == False:
            returnString = self.stopFreqLineEdit.text()
            if self.is_number(returnString): 
                self.StopFreq = float(returnString)
                if self.StopFreq < 1000 or self.StopFreq > 500000:
                    QMessageBox.about(self, "Stop Frequency Error","Stop frequency must be between 1000 and 500000")
                    return False
                print (self.StopFreq)
            else:
                QMessageBox.about(self, "Stop Frequency Error","Stop frequency entry is not a number")
                return False
             
            if self.StopFreq < self.StartFreq:
                QMessageBox.about(self, "Frequency Error","Stop frequency must be greater than start frequency")
                return False
               
            returnString = self.stepsLineEdit.text()
            if self.is_number(returnString): 
                self.Steps = float(returnString)
                if self.Steps < 0 or self.Steps > 300:
                    QMessageBox.about(self, "Step Count Error","Step count must be between 1 and 300")
                    return False
                print (int(self.Steps))
            else:
                QMessageBox.about(self, "Step Count Error","Step count entry is not a number")
                return False
            
        progressMax = int(self.Steps)
        print ("steps " + str(self.Steps))
        self.progressBar.setMaximum(progressMax)
        self.progressBar.setMinimum(0)

        return True

    def vregSelectionChange(self,index):
        print ("Vreg index",index,"selection changed ",self.vregComboBox.currentText())
        if index == 7:
            # V_GFX Slammer Loads
            self.slamComboBox.clear()  
            self.slamComboBox.addItem("254")
            self.slamComboBox.addItem("191")
            self.slamComboBox.addItem("180")
            self.slamComboBox.addItem("170")
            self.slamComboBox.addItem("160")
            self.slamComboBox.addItem("150")
            self.slamComboBox.addItem("140")
            self.slamComboBox.addItem("130")
            self.slamComboBox.addItem("127")
            self.slamComboBox.addItem("110")
            self.slamComboBox.addItem("100")
            self.slamComboBox.addItem("90")
            self.slamComboBox.addItem("80")
            self.slamComboBox.addItem("70")
            self.slamComboBox.addItem("64")
            self.slamComboBox.addItem("60")
            self.slamComboBox.addItem("50")
            self.slamComboBox.addItem("40")
            self.slamComboBox.addItem("25")
            self.slamComboBox.addItem("20")
            self.slamComboBox.addItem("10")
        
        # V_CPU Slammer Loads
        elif index == 8:
            self.slamComboBox.clear()  
            self.slamComboBox.addItem("86")
            self.slamComboBox.addItem("65")
            self.slamComboBox.addItem("43")
            self.slamComboBox.addItem("25")
            self.slamComboBox.addItem("22")
            self.slamComboBox.addItem("20")
            self.slamComboBox.addItem("15")
            self.slamComboBox.addItem("10")
            self.slamComboBox.addItem("5")
            
        # V_SOC Slammer Loads
        elif index == 6:
            self.slamComboBox.clear()  
            self.slamComboBox.addItem("50")
            self.slamComboBox.addItem("40")
            self.slamComboBox.addItem("30")
            self.slamComboBox.addItem("25")
            self.slamComboBox.addItem("20")
            self.slamComboBox.addItem("10")
        
        # V_MEMPHY
        elif index == 0:
            self.slamComboBox.clear()  
            self.slamComboBox.addItem("35")
            self.slamComboBox.addItem("30")
            self.slamComboBox.addItem("25")
            self.slamComboBox.addItem("20")
            self.slamComboBox.addItem("15")
            self.slamComboBox.addItem("10")

        # V_MEMIO
        elif index == 1:
            self.slamComboBox.clear()  
            self.slamComboBox.addItem("25")
            self.slamComboBox.addItem("20")
            self.slamComboBox.addItem("15")
            self.slamComboBox.addItem("10")
            self.slamComboBox.addItem("5")            
        else:
            self.slamComboBox.clear()  
            self.slamComboBox.addItem("20")
            self.slamComboBox.addItem("15")
            self.slamComboBox.addItem("10")
            self.slamComboBox.addItem("5")
            
            
      
    def slamSelectionChange(self,index):
        self.slamLoad = self.slamComboBox.currentText()
        print ("Slam index",index,"selection changed. Slam Load ",self.slamLoad)
        
        vregIndex = self.vregComboBox.currentIndex()
        if vregIndex == 7:
            if index == 0:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
            elif index == 1:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
            elif index == 2:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
                self.chromaComboBox.addItem("15")
            else:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
                self.chromaComboBox.addItem("15")
                self.chromaComboBox.addItem("20")
        elif vregIndex == 8:
            if index == 0:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
            elif index == 1:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
            elif index == 2:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
            elif index == 3:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
                self.chromaComboBox.addItem("15")
            else:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
                self.chromaComboBox.addItem("15")
                self.chromaComboBox.addItem("20")
        else:
            if index == 0:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
            elif index == 1:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
            elif index == 2:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
            elif index == 3:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
                self.chromaComboBox.addItem("15")
            else:
                self.chromaComboBox.clear()  
                self.chromaComboBox.addItem("0")
                self.chromaComboBox.addItem("1")
                self.chromaComboBox.addItem("5")
                self.chromaComboBox.addItem("10")
                self.chromaComboBox.addItem("15")
                self.chromaComboBox.addItem("20")
            

      
    def chromaSelectionChange(self,index):
        self.chromaLoad = self.chromaComboBox.currentText()
        print ("Chroma index",index,"selection changed. Chroma Load ",self.chromaLoad)

    def chromaStartSelectionChange(self,index):
        self.chromaStartLoad = self.chromaStartComboBox.currentText()
        print ("Chroma index",index,"selection changed. Chroma Start Load ",self.chromaStartLoad)
      
    def chromaStopSelectionChange(self,index):
        self.chromaStopLoad = self.chromaStopComboBox.currentText()
        print ("Chroma index",index,"selection changed. Chroma Stop Load ",self.chromaStopLoad)
      
    def paintEvent(self, e):
        pen = QPen(Qt.blue, 2, Qt.SolidLine)
        painter = QPainter(self)
#        painter.begin(self)
        painter.setPen(pen)
        painter.drawLine(5, 60, 995, 60)
        painter.drawLine(5, 130, 995, 130)
#        painter.end()
        
    def openInstruments(self):
        rm = visa.ResourceManager()
        instrumentList = rm.list_resources()
        print (instrumentList)
        for loopIndex in range(0, len(instrumentList)):
#        for loopIndex in range(0, 3):
            inst = rm.open_resource(instrumentList[loopIndex])
#            print(inst)
            returnString = inst.query("*IDN?")
            if returnString.find("MSO4104B") != -1:
                print("found scope")
                self.Scope = inst
#                self.scopeInstr.setText(instrumentList[loopIndex]) 
                countComma = 0
                for i, c in enumerate(returnString):
                    if "," == c:
                        countComma = countComma + 1
#                        print "comma found in scope string at " + str(i)
                    if countComma == 1:
                        endOfString = i + 1
                self.scopeIDN.setText(returnString[0:endOfString]) 
            if returnString.find("MSO58") != -1:
                print("found scope Series 5")
                self.Scope = inst
#                self.scopeInstr.setText(instrumentList[loopIndex]) 
                countComma = 0
                for i, c in enumerate(returnString):
                    if "," == c:
                        countComma = countComma + 1
#                        print "comma found in scope string at " + str(i)
                    if countComma == 1:
                        endOfString = i + 1
                self.scopeIDN.setText(returnString[0:endOfString]) 
#            if returnString.find("CHROMA") != -1:
#                print("found chroma")
#                self.Load = inst
##                self.loadInstr.setText(instrumentList[loopIndex]) 
#                countComma = 0
#                for i, c in enumerate(returnString):
#                    if "," == c:
#                        countComma = countComma + 1
#                    if countComma == 1:
#                        endOfString = i + 1
#                self.loadIDN.setText(returnString[0:endOfString]) 
            if returnString.find("33621A") != -1:
                print("found waveform gen")
                self.Waveform = inst
#                self.waveformInstr.setText(instrumentList[loopIndex]) 
                countComma = 0
                for i, c in enumerate(returnString):
                    if "," == c:
                        countComma = countComma + 1
                    if countComma == 1:
                        endOfString = i + 1
                self.waveformIDN.setText(returnString[0:endOfString]) 
      
    def createRadioButtonGroup(self):
        
        slammerRevA = QRadioButton("Quad Slammer")
        slammerRevB = QRadioButton("Dual slammer")

        slammerRevB.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(slammerRevA)
        vbox.addWidget(slammerRevB)
        vbox.addStretch(1)
        self.slammerGroupBox.setLayout(vbox)
        
        slammerRevA.clicked.connect(self.onSlammerRevA)
        slammerRevB.clicked.connect(self.onSlammerRevB)

    def onSlammerRevA(self, value):
        self.slammer = 1
        print("Got to here Slam A")

    def onSlammerRevB(self, value):
        self.slammer = 2
        print("Got to here Slam B")  
        
if __name__ == '__main__':
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = MainWindow()
    app.exec_()  
#    sys.exit(app.exec_())  
