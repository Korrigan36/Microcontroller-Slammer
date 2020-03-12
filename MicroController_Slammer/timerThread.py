import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QRadioButton, QVBoxLayout, 
    QGroupBox, QComboBox, QLineEdit, QPushButton, QMessageBox, QInputDialog, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QIcon, QPainter, QPen, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot

sys.path.append("C:\\Users\\v-stpur\\Documents\\XBoxScripts\\instrument_Libraries")

#import visa
import time
import microSlammer
import pySerial_Big as serial 

version_Info = "Python PyQt5 Slammer Frequency Sweep V0.1"

class TimerThread(QObject):

#    countLoop = 0
#    countStep = 0
#    amplitude = 0
#    freqStep = 0
#    Scope = 0 
#    Load = 0 
#    Waveform = 0 
#    StartFreq = 0 
#    StopFreq = 0 
#    Steps = 0
#    VregSelection = 0
#    VregText = 0
#    currentLogFreq = 0
    
    timerSignal = pyqtSignal(str)
    quitSignal = pyqtSignal(object)
    startStop = True
    
    onTime = 15
    offTime = 15
    slamUpdated = False
    onTimeUpdated = False
    dutyUpdated = False
    firstTime = True
    bits = 100
    comPort = "COM4"
    
    #This list must match 1 to 1 with Vreg names drop down list
    vregVoltageList = [0.85, 1.35, 3.3, 0.8, 0.95, 1.8, 0.8, 0.8, 1.0]          #This list is used to "pre-bias" the CH1 offset
    vregLoadLineList = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0001, 0.00032]     # Load Line list for predicting slam levels
#    vregLoadLineList = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001, 0.002]
    

    def __init__(self, parameterArray):
        QThread.__init__(self)
        
        self.amplitude              = parameterArray[0]
        self.duty                   = parameterArray[1]
        self.edgeTimes              = parameterArray[2]

        self.slammer = microSlammer.microSlammer()
#        self.scope = scopeInstrument.MSO58(self.Scope)
        self.sense_Resistor = 0.0025
        
        self.voltOut = float(self.amplitude)/4.0*self.sense_Resistor
        print ("Waveform Amplitude for " + str(self.amplitude) + " is " + str(self.voltOut))
            
        #trigger is the same as offset value
        self.trigger = self.voltOut / -2.0
#        self.trigger = self.voltOut / +2.0
#        self.comPort = "COM4"
#        return_Error = self.slammer.openSerialPort(self.comPort)
#        print ("Return Error From Open Serial Port: " + str(return_Error))
#        if return_Error == b'':
#            print ("Serial Port Connected")
#            self.timerSignal.emit(self.comPort)
#            
##            self.slammer.write_Main()
##            self.slammer.write_SigGen()
##            self.slammer.write_DefaultVariables()
##
            
        
    def __del__(self):
        print("del")
#        self.wait()
            
    def startTimer(self):
        self.startStop = True

    def stopTimer(self):
#        self.slammer.close_Serial()
        self.startStop = False
        self.quitSignal.emit(self.quitSignal)
        self.waitScopeShot = False
        time.sleep(1)
        
    def testEnd(self):
                    
        print("Test Finished")
        self.stopTimer()

#    @pyqtSlot(str)
    def scopeShot_Slot(self, sentence):
        print(sentence)
        self.waitScopeShot = False
        
    def dutyCycle_Slot(self, sentence, duty):
        print(sentence)
        print (duty)
        self.offTime = (self.onTime / (duty / 100)) - self.onTime
        self.dutyUpdated = True
        
    def onTime_Slot(self, sentence, onTime):
        print(sentence)
        self.onTimeUpdated = True
        self.onTime = onTime 
                
        
    def slamLoad_Slot(self, sentence, slamLoad):
        #This slammer had four 5mOhm sense resistors in parallel
        load = slamLoad / 4.0
        volts = load * 0.0025
#        print ("Volts: " + str(volts))
        self.trigger = volts / -2.0

        bitsPerVolt = 255 / 0.25
        self.bits = int(bitsPerVolt * volts)
        print ("Bits: " + str(self.bits))
        self.slamUpdated = True
        
    def run(self):
        
        print ("In Run")
        
        while self.startStop == True:

#            if self.slamUpdated or self.firstTime or self.onTimeUpdated or self.dutyUpdated:
            if self.slamUpdated or self.onTimeUpdated or self.dutyUpdated:
                print ("We got into here....")
                time.sleep(1)
                
                return_Error = self.slammer.openSerialPort(self.comPort)
                print ("Return Error From Open Serial Port: " + str(return_Error))
                if return_Error == b'':
                    print ("Serial Port Connected")
                    self.slammer.write_Main()
                    self.slammer.write_SigGen()
                    self.slammer.update_Variables(self.bits)
                    self.slammer.reset_Board()
                    self.slammer.close_Serial()
                            
                    self.firstTime = False
                    self.slamUpdated = False
                    self.onTimeUpdated = False
                    self.dutyUpdated = False
                    self.timerSignal.emit(self.comPort)
#                
#                self.slammer.re_Enter_Repl()
                
#                buf = {}
#                
#                buf[0]  = "f = open('variables.py', 'w')"
#                buf[1]  = "f.write('\\n')"
#                buf[2]  = "f.write('amplitude = " + str(4096) + "')"
#                buf[3]  = "f.close()"
#
##                return_Error = self.slammer.openSerialPort(self.comPort)
##                print ("Return Error From Open Serial Port: " + str(return_Error))
##                if return_Error == b'':
##                    print ("Serial Port Connected")
#                self.slammer.write_Command_to_Micro(buf)
#                self.slammer.reset_Board()
                    
            else:
                time.sleep(0.1)
                
        print("Slam Stopped")
                
            
