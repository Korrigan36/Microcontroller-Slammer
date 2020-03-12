# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 09:51:31 2017

@author: v-stpurc
"""
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QRadioButton, QVBoxLayout, QCheckBox, QProgressBar,
    QGroupBox, QComboBox, QLineEdit, QPushButton, QMessageBox, QInputDialog, QDialog, QDialogButtonBox, QSlider, QGridLayout, QHBoxLayout, QFileDialog, QListWidget)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore , QtGui

import timerThread
import microSlammer
import serial, struct
import time
        
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
    onTime = 0
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
    onTime_Signal = pyqtSignal(str, int)
    slamLoad_Signal = pyqtSignal(str, int)
            
    continueSlider = True
    
    slammer = 0
    comPort = "COM4"
    serialPort = 0
    amplitude = 400
    onTime = 50
    dutyCycle = 50
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.initUI()
        self.slammer = microSlammer.microSlammer()
#        self.openInstruments()
#        self.openFileNameDialog()
 
       
    def initUI(self):
        
        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('CFTAC')
        self.setWindowIcon(QIcon('xbox_icon.ico')) 
        
        instrumentGrid = QGridLayout()
        instrumentChoiceGroupBox  = QGroupBox()

        slammerLabel = QLabel(self)
        slammerLabel.setText("Slammer Port")
        instrumentGrid.addWidget(slammerLabel, 0, 0)
  
        self.slammerCOM = QLabel(self)
        self.slammerCOM.setText("Slammer")
        instrumentGrid.addWidget(self.slammerCOM, 0, 1)
        
        self.initBoardButton = QPushButton('Initialize Board', self)
        self.initBoardButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
        self.initBoardButton.setText("Initialize Board")
        self.initBoardButton.clicked[bool].connect(self.initBoard)
        instrumentGrid.addWidget(self.initBoardButton, 1, 0)

        instrumentChoiceGroupBox.setLayout(instrumentGrid)
        
        sliderGrid = QGridLayout()
        sliderGroupBox  = QGroupBox()

        self.sliderLabel = QLabel(self)
        self.sliderLabel.setText("Load Slam")
        sliderGrid.addWidget(self.sliderLabel, 0, 0)

        self.slamLoadSlider = QSlider(Qt.Horizontal, self)
        self.slamLoadSlider.setFocusPolicy(Qt.NoFocus)
        self.slamLoadSlider.setRange(1, 400)
        self.slamLoadSlider.setValue(50)
        self.slamLoadSlider.setGeometry(720, 150, 200, 20)
        self.slamLoadSlider.setEnabled(True)
        self.slamLoadSlider.sliderReleased.connect(self.slamLoadChanged)

        self.slamLoad = QLabel(self)
        self.slamLoad.setText(str(self.slamLoadSlider.value()) + "amps")
        sliderGrid.addWidget(self.slamLoad, 0, 1)

        sliderGrid.addWidget(self.slamLoadSlider, 1, 0)
        
        self.onTimeLabel = QLabel(self)
        self.onTimeLabel.setText("On Time")
        sliderGrid.addWidget(self.onTimeLabel, 2, 0)

        self.onTimeSlider = QSlider(Qt.Horizontal, self)
        self.onTimeSlider.setFocusPolicy(Qt.NoFocus)
        self.onTimeSlider.setRange(5, 50)
        self.onTimeSlider.setValue(50)
        self.onTimeSlider.setGeometry(720, 150, 200, 20)
        self.onTimeSlider.setEnabled(True)
        self.onTimeSlider.sliderReleased.connect(self.onTimeChanged)

        self.onTimeLabel = QLabel(self)
        self.onTimeLabel.setText(str(self.onTimeSlider.value()) + "us")
        sliderGrid.addWidget(self.onTimeLabel, 2, 1)

        sliderGrid.addWidget(self.onTimeSlider, 3, 0)
        
        self.dutyLabel = QLabel(self)
        self.dutyLabel.setText("Duty Cycle")
        sliderGrid.addWidget(self.dutyLabel, 4, 0)

        self.dutyCycleSlider = QSlider(Qt.Horizontal, self)
        self.dutyCycleSlider.setFocusPolicy(Qt.NoFocus)
        self.dutyCycleSlider.setRange(1, 50)
        self.dutyCycleSlider.setValue(50)
        self.dutyCycleSlider.setGeometry(720, 150, 200, 20)
        self.dutyCycleSlider.setEnabled(True)
        self.dutyCycleSlider.sliderReleased.connect(self.dutyCycleChanged)

        self.dutyCycleLabel = QLabel(self)
        self.dutyCycleLabel.setText(str(self.dutyCycleSlider.value()) + "%")
        sliderGrid.addWidget(self.dutyCycleLabel, 4, 1)

        sliderGrid.addWidget(self.dutyCycleSlider, 5, 0)
        
        sliderGroupBox.setLayout(sliderGrid)
         
        autoTestGroupBox  = QGroupBox()
        autoTestLayout    = QHBoxLayout()
        
        self.autoTest = QCheckBox("Automated Test")
        self.autoTest.setChecked(False)
        self.autoTest.stateChanged.connect(self.autoTestCheck)

        autoTestLayout.addWidget(self.autoTest)
        
        self.tdcLabel = QLabel(self)
        self.tdcLabel.setText("TDC")
        autoTestLayout.addWidget(self.tdcLabel)

        self.tdcList = QLineEdit(self)
        self.tdcList.setEnabled(True)
        autoTestLayout.addWidget(self.tdcList)
        
        self.edcLabel = QLabel(self)
        self.edcLabel.setText("EDC")
        autoTestLayout.addWidget(self.edcLabel)

        self.edcList = QLineEdit(self)
        self.edcList.setEnabled(True)
        autoTestLayout.addWidget(self.edcList)
        
        autoTestGroupBox.setLayout(autoTestLayout)
        
        self.vregComboBox = QComboBox(self)
        self.vregComboBox.addItem("V_3P3_CFX")
        self.vregComboBox.addItem("V_CPUCORE")
        self.vregComboBox.addItem("V_DRAM1P8")
        self.vregComboBox.addItem("V_GFXCORE")
        self.vregComboBox.addItem("V_MEMIO")
        self.vregComboBox.addItem("V_MEMPHY")
        self.vregComboBox.addItem("V_SOC")
        self.vregComboBox.addItem("V_SOC1P8")

        startButtonGroupBox  = QGroupBox()
        startButtonLayout    = QHBoxLayout()
        self.startStopButton = QPushButton('Start Slam', self)
        self.startStopButton.setGeometry(800, 70, 180, 50)

        self.font = QFont()
        self.font.setBold(True)
        self.font.setPointSize(16)
        self.startStopButton.setFont(self.font)
        self.startStopButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
#        self.startStopButton.setStyleSheet('QString::fromUtf8("QPushButton:disabled")')
        self.startStopButton.setText("Slam")
        self.startStopButton.setEnabled(False)
        self.startStopButton.clicked[bool].connect(self.startStopTest)
        startButtonLayout.addWidget(self.startStopButton)
        startButtonGroupBox.setLayout(startButtonLayout)
 
        quitButtonGroupBox  = QGroupBox()
        quitButtonLayout    = QHBoxLayout()
        self.font.setPointSize(12)
        self.quitButton = QPushButton('Quit', self)
        self.quitButton.setFont(self.font)
        self.quitButton.setGeometry(890, 260, 100, 30)
        self.quitButton.clicked[bool].connect(self.closeEventLocal)
        quitButtonLayout.addWidget(self.quitButton)
        quitButtonGroupBox.setLayout(quitButtonLayout)
        
        grid = QGridLayout()
        grid.setColumnStretch(0,5)
        grid.setColumnStretch(1,5)
        grid.addWidget(instrumentChoiceGroupBox, 0, 0)
        grid.addWidget(sliderGroupBox, 0, 1)
        grid.addWidget(self.vregComboBox, 1, 0)
        grid.addWidget(autoTestGroupBox, 1, 1)
        grid.addWidget(startButtonGroupBox, 2, 0)
        grid.addWidget(quitButtonGroupBox, 2, 1)
        self.setLayout(grid)

        self.show()
        
    def initBoard(self):
        
#        self.comPort = "COM4"
#            self.slammer = microSlammer.microSlammer()
            
            port = "COM4"
            self.serialPort = serial.Serial(port, baudrate=9600, interCharTimeout=1)
            self.serialPort.write(str.encode("quit"))
            self.serialPort.flush()
            img = self.serialPort.read_all()
            print(img)
            self.serialPort.close()
            time.sleep(1)
            
            return_Error = self.slammer.openSerialPort(self.comPort)
            print ("Return Error From Open Serial Port: " + str(return_Error))
            if return_Error:
                print ("Serial Port Connected")
                self.slammer.write_Main()
#                self.slammer.write_SigGen()
                self.slammer.test_InlineAssembler()
#                self.slammer.update_Variables(self.bits)
#                self.slammerCOM.setText(self.comPort)
                self.slammer.reset_Board()
                self.slammer.close_Serial()
##                self.slamLoadSlider.setEnabled(True)
##                self.initBoardButton.setStyleSheet('QString::fromUtf8("QPushButton:disabled")')
##                self.initBoardButton.setDisabled(True)
##                self.startStopButton.setEnabled(True)
                self.startStopButton.setStyleSheet('QPushButton {background-color: #FF2000; color: black;}')
                self.startStopButton.setEnabled(True)

 

        
    def autoTestCheck(self):
        if self.autoTest.isChecked() == True:
            self.dutyCycleSlider.setEnabled(False)
            self.onTimeSlider.setEnabled(False)
            self.slamLoadSlider.setEnabled(False)
            self.tdcList.setEnabled(True)
            self.edcList.setEnabled(True)
        else:
            self.dutyCycleSlider.setEnabled(True)
            self.onTimeSlider.setEnabled(True)
            self.slamLoadSlider.setEnabled(True)
            self.tdcList.setEnabled(False)
            self.edcList.setEnabled(False)
        

    def runLoop(self, port):
#        self.slammerCOM.setText(port)
        self.continueSlider = True

    def slamLoadChanged(self):
        print ("Change Slam Load")
        slamLoad = self.slamLoadSlider.value()        
        self.slamLoad.setText(str(self.slamLoadSlider.value()) + "amps")
        load = slamLoad / 4.0
        volts = load * 0.0025
        bitsPerVolt = 4095 / 0.25
        self.bits = int(bitsPerVolt * volts)


        port = "COM4"
        self.serialPort = serial.Serial(port, baudrate=9600, interCharTimeout=1)
        self.serialPort.write(str.encode("ampl"))
        self.serialPort.flush()
        img = self.serialPort.read_all()
        print(img)

        value = self.bits
        print ("bits are now: " + str(self.bits))
        self.serialPort.write(struct.pack('L', value))
        self.serialPort.flush()
        img = self.serialPort.read(80)
        print(struct.unpack('L', img))

        self.serialPort.close()

    def onTimeChanged(self):
        self.onTime = self.onTimeSlider.value() 
        counter = int(self.onTime /  0.046)
        print ("On Time Counter is: " + str(counter))
        self.onTimeLabel.setText(str(self.onTime) + "us")

        port = "COM4"
        self.serialPort = serial.Serial(port, baudrate=9600, interCharTimeout=1)
        self.serialPort.write(str.encode("onTm"))
        self.serialPort.flush()
        img = self.serialPort.read_all()
        print(img)
        
        value = counter

        print ("orig val " + str(value))
        self.serialPort.write(struct.pack('L', value))
        self.serialPort.flush()
#        time.sleep(1)
        img = self.serialPort.read_all()
        print("USB val " + str(img))
        print(struct.unpack('L', img))

        self.serialPort.write(str.encode("duty"))
        self.serialPort.flush()
        img = self.serialPort.read_all()
        print(img)
        
        value = (self.onTime / (self.dutyCycle / 100) - self.onTime)
        counter = int(value /  0.046)
        print ("Off Time Counter is: " + str(counter))

        print ("orig val " + str(value))
        self.serialPort.write(struct.pack('L', counter))
        self.serialPort.flush()
#        time.sleep(1)
        img = self.serialPort.read_all()
        print("USB val " + str(img))
        print(struct.unpack('L', img))
            
        self.serialPort.close()
           

    def dutyCycleChanged(self):
        self.dutyCycle = self.dutyCycleSlider.value()        
        self.dutyCycleLabel.setText(str(self.dutyCycle) + "%")
#        if  self.continueSlider:
#            self.dutyCycle_Signal.emit('Changing duty cycle to ' + str(dutyCycle) + "%", dutyCycle)
#            self.continueSlider = False
      
        port = "COM4"
        self.serialPort = serial.Serial(port, baudrate=9600, interCharTimeout=1)
        self.serialPort.write(str.encode("duty"))
        self.serialPort.flush()
        img = self.serialPort.read_all()
        print(img)
        
        value = (self.onTime / (self.dutyCycle / 100) - self.onTime)
        counter = int(value /  0.046)
        print ("Off Time Counter is: " + str(counter))

        print ("orig val " + str(value))
        self.serialPort.write(struct.pack('L', counter))
        self.serialPort.flush()
#        time.sleep(1)
        img = self.serialPort.read_all()
        print("USB val " + str(img))
        print(struct.unpack('L', img))
            
        self.serialPort.close()

    def closeEventLocal(self, event):
#        try:
#            self.work.stopTimer()
#        except:
#            print ("Timer Thread Not Running")
            
        port = "COM4"
        self.serialPort = serial.Serial(port, baudrate=9600, interCharTimeout=1)
        self.serialPort.write(str.encode("quit"))
        self.serialPort.flush()
        img = self.serialPort.read_all()
        print(img)
        self.serialPort.close()
        #With openpyxl you name the file when you save it.
        #We don't save it until the exit button is pushed and the gui quits
#        self.workBook.save(self.excelFileName)

        print("Got quit signal")
        self.close()


    def quitLoop(self):
        self.thread.quit()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False   
        
    def startStopTest(self):
        returnString = self.startStopButton.text()
        if returnString.find("Slam") != -1:
        
            print ("Slam Started")

            self.startStopButton.setStyleSheet('QPushButton {background-color: #FF2000; color: black;}')
            self.startStopButton.font()
            self.startStopButton.setText("Abort Slam")
                
            slamLoad = self.slamLoadSlider.value()        
            self.slamLoad.setText(str(self.slamLoadSlider.value()) + "amps")
            load = slamLoad / 4.0
            volts = load * 0.0025
            bitsPerVolt = 255 / 0.25
            self.bits = int(bitsPerVolt * volts)

#            self.slamLoadSlider.setEnabled(True)

            port = "COM4"
            self.serialPort = serial.Serial(port, baudrate=9600, interCharTimeout=1)

            self.serialPort.write(str.encode("strt"))
            self.serialPort.flush()
            time.sleep(1)
            img = self.serialPort.read_all()

            print(img)
            if img == b'strt':
                print ("Slam Finished")
                self.startStopButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
                self.startStopButton.setText("Slam")

            self.serialPort.close()

        else:
            print ("Slam Aborted")
            self.startStopButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
            self.startStopButton.setText("Slam")

            return_Error = self.slammer.openSerialPort(self.comPort)
            if return_Error:
                print ("Serial Port Connected")
                self.slamLoadSlider.setEnabled(False)

            self.serialPort.close()
                
                
    def startThread(self):

        parameterArray = [self.slamLoadSlider.value(), self.dutyCycleSlider.value(), self.onTimeSlider.value()]
        self.work = timerThread.TimerThread(parameterArray) 
        self.work.timerSignal.connect(self.runLoop)
        self.work.quitSignal.connect(self.quitLoop)
        self.scopeShot_Signal.connect(self.work.scopeShot_Slot)
        self.dutyCycle_Signal.connect(self.work.dutyCycle_Slot)
        self.onTime_Signal.connect(self.work.onTime_Slot)
        self.slamLoad_Signal.connect(self.work.slamLoad_Slot)
        self.thread = QThread()

        self.work.moveToThread(self.thread)
        self.thread.started.connect(self.work.run)
        self.thread.start()
        
    def openFileNameDialog(self):    

        self.configFileName = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\Users\\v-stpur\\Documents\\XBoxScripts\\SlammerFrequencySweepAllRails',"Excel files (*.xlsx)")
        print ("Filename is: " + str(self.configFileName[0]))

        # Open the Config file
        self.config_workbook = load_workbook(self.configFileName[0], data_only=True)
        self.config_sheet = self.config_workbook.get_sheet_by_name(name = 'AC Matrix') 
        vregName = self.config_sheet.cell(1, 1).value
        print ("first name in config file: " + vregName)


if __name__ == '__main__':
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = MainWindow()
    app.exec_()  
#    sys.exit(app.exec_())  
