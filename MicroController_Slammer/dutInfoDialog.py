#import sys
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QDialog)
from PyQt5.QtGui import QIcon, QPainter, QPen, QFont
#from PyQt5.QtCore import Qt
#from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot



class DutInfoDialog(QDialog):
    def __init__(self):
        super(DutInfoDialog, self).__init__()

        self.initUI()

    def initUI(self):
         
        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle('DUT Info')
        self.setWindowIcon(QIcon('xbox_icon.ico')) 
        
        self.okButton = QPushButton('Ok', self)
        self.okButton.setGeometry(210, 160, 80, 30)
        self.okButton.clicked[bool].connect(self.returnInfo)

        configId = QLabel(self)
        configId.setGeometry(10, 10, 80, 20)
        configId.setText("Config ID")
        
        self.configIdLineEdit = QLineEdit(self)
        self.configIdLineEdit.setGeometry(10, 30, 80, 20)
        self.configIdLineEdit.setText("Blank Config")

        pcbaSN = QLabel(self)
        pcbaSN.setGeometry(100, 10, 140, 20)
        pcbaSN.setText("PCBA Serial #")
        
        self.pcbaSNLineEdit = QLineEdit(self)
        self.pcbaSNLineEdit.setGeometry(100, 30, 140, 20)
        self.pcbaSNLineEdit.setText("0085602J1000863044")

        productSN = QLabel(self)
        productSN.setGeometry(250, 10, 120, 20)
        productSN.setText("Product Serial #")
        
        self.productSNLineEdit = QLineEdit(self)
        self.productSNLineEdit.setGeometry(250, 30, 120, 20)
        self.productSNLineEdit.setText("n/a")

        scopeType = QLabel(self)
        scopeType.setGeometry(10, 55, 80, 20)
        scopeType.setText("Scope Type")
        
        self.scopeTypeLineEdit = QLineEdit(self)
        self.scopeTypeLineEdit.setGeometry(10, 75, 80, 20)
        self.scopeTypeLineEdit.setText("Tek MSO4104B")

        probeType = QLabel(self)
        probeType.setGeometry(100, 55, 100, 20)
        probeType.setText("Scope Probe Type")
        
        self.probeTypeLineEdit = QLineEdit(self)
        self.probeTypeLineEdit.setGeometry(100, 75, 80, 20)
        self.probeTypeLineEdit.setText("Tek TDP1500")

        runNotes = QLabel(self)
        runNotes.setGeometry(200, 55, 150, 20)
        runNotes.setText("Run Notes")
        
        self.runNotesLineEdit = QLineEdit(self)
        self.runNotesLineEdit.setGeometry(200, 75, 150, 20)
        self.runNotesLineEdit.setText("Blank Note")

        senseRes = QLabel(self)
        senseRes.setGeometry(10, 100, 80, 20)
        senseRes.setText("Sense Resistor")
        
        self.senseResLineEdit = QLineEdit(self)
        self.senseResLineEdit.setGeometry(10, 120, 50, 20)
        self.senseResLineEdit.setText("0.001")


#        self.show()
       
    def returnInfo(self):
        self.close()
        return (self.configIdLineEdit.text(), self.pcbaSNLineEdit.text(), self.productSNLineEdit.text(),  
                self.scopeTypeLineEdit.text(), self.probeTypeLineEdit.text(), self.runNotesLineEdit.text(), self.senseResLineEdit.text())

   
