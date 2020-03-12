import time


def scope_SetAnnotation(scopeObject, text):
    tempString = "MESSage:CLEAR"
    scopeObject.write(tempString)
    tempString = "MESSage:SHOW \"" + str(text) + "\""
    scopeObject.write(tempString)
    tempString = "MESSage:STATE ON"
    scopeObject.write(tempString)
    tempString = "MESSAGE:BOX 650,720"
    scopeObject.write(tempString)
    
def scope_SetChannel_Label(scopeObject, channel, text):
    tempString = str(channel) + ":LABel \"" + str(text) + "\""
    scopeObject.write(tempString)

def scope_SetChannel_OnOff(scopeObject, channel, text):
    tempString = "SELect:" + str(channel) + " " + str(text)
    scopeObject.write(tempString)

def scope_SetChannel_Position(scopeObject, channel, text):
    tempString = str(channel) + ":POSition " + str(text) 
    scopeObject.write(tempString)
    
def scope_SetAcquisitionHiRes(scopeObject):
    tempString = "ACQuire:MODE HIRes"
    scopeObject.write(tempString)

def scope_SetAcquisitionEnvelope(scopeObject):
    tempString = "ACQuire:MODE ENVelope"
    scopeObject.write(tempString)
    tempString = "ACQuire:NUMEnv INFInite"
    scopeObject.write(tempString)

def scope_Setuprecordlength(scopeObject, value):
    tempString = "HORIZONTAL:RECORDLENGTH " + str(value)
    scopeObject.write(tempString)

def scope_SetTimescale(scopeObject, value):
    tempString = "HORizontal:MAIn:SCAle " + str(value)
    scopeObject.write(tempString)
    
def scope_Set_Trigger_Auto(scopeObject):
    tempString = "TRIGGER:A:MODE AUTO"
    scopeObject.write(tempString)
    
def scope_Set_Trigger_Normal(scopeObject):
    tempString = "TRIGGER:A:MODE NORMAL"
    scopeObject.write(tempString)
    
def scope_Clear_Statistics(scopeObject):
    tempString = "MEASUREMENT:STATISTICS RESET"
    scopeObject.write(tempString)
    
def scope_Stop(scopeObject):
    tempString = "ACQuire:STATE OFF"
    scopeObject.write(tempString)

def scope_Start(scopeObject):
    tempString = "ACQuire:STATE ON"
    scopeObject.write(tempString)
    
def scope_Clear_Persist(scopeObject):
    tempString = "DISplay:PERSistence CLEAR"
    scopeObject.write(tempString)
    
def scope_Force_Trigger(scopeObject):
    tempString = "TRIGger FORCe"
    scopeObject.write(tempString)
    
def scope_Set_Single_Capture(scopeObject):
    tempString = "ACQuire:STOPAfter SEQUENCE"
    scopeObject.write(tempString)
    
def scope_Set_Multiple_Capture(scopeObject):
    tempString = "ACQuire:STOPAfter RUNStop"
    scopeObject.write(tempString)
    
def scope_Reset_Persistance(scopeObject):
    tempString = "DISplay:PERSistence:RESET"
    scopeObject.write(tempString)
    tempString = "DISplay:PERSistence INFInite"
    scopeObject.write(tempString)
 
def scope_SetChannel_Bandwidth(scopeObject, channel, text):
    tempString = str(channel) + ":BANdwidth " + str(text)
    scopeObject.write(tempString)

def scope_Set_Measurement(scopeObject, measNumber, channel, measurement):
#    tempString = "MEASUrement:MEAS" + str(measNumber) + ":SOURCE1 " + str(channel)
    tempString = "MEASUrement:MEAS" + str(measNumber) + ":SOURCE1 " + channel
    scopeObject.write(tempString)
#    tempString = "MEASUrement:MEAS" + str(measNumber) + ":TYPe " + str(measurement)
    tempString = "MEASUrement:MEAS" + str(measNumber) + ":TYPe " + measurement
    scopeObject.write(tempString)
    tempString = "MEASUrement:MEAS" + str(measNumber) + ":STATE ON"
    scopeObject.write(tempString)

def scope_Get_Measurement(scopeObject, measNumber, meanMinOrMax):
    if meanMinOrMax == "VAL":
        tempString = "MEASUrement:MEAS" +str(measNumber) + ":VALue?"
        return scopeObject.query(tempString)
    else:
        tempString = "MEASUrement:MEAS" + str(measNumber) + ":" + str(meanMinOrMax) + "?"
        return scopeObject.query(tempString)

def scope_SetUp_Trigger(scopeObject, channel, level, edge, position):
    tempString = "HORizontal:DELay:MODe OFF"
    scopeObject.write(tempString)
    tempString = "TRIGger:A:LEVel -" + str(level)
    scopeObject.write(tempString)
    tempString = "TRIGGER:A:EDGE:SOURCE " + str(channel)
    scopeObject.write(tempString)
    tempString = "TRIGger:A:EDGE:SLOpe " + str(edge)
    scopeObject.write(tempString)
    tempString = "HORizontal:MAIn:POSition " + str(position)
    scopeObject.write(tempString)

def scope_ScreenShot_Copy(scopeObject, fileName):
    tempString = "*CLS"
    scopeObject.write(tempString)
#    time.sleep(0.1)
    tempString = "SAVe:ASSIgn:TYPe IMAGe"
    scopeObject.write(tempString)
#    time.sleep(0.1)
    tempString = "SAVe:IMAGe:FILEFormat PNG"
    scopeObject.write(tempString)
#    time.sleep(0.1)
    tempString = "HARDCOPY START"
    scopeObject.write(tempString)
    time.sleep(2)

    raw_data = scopeObject.read_raw()

    fid = open(fileName, 'wb')
    fid.write(raw_data)
    fid.close()    
    
def scope_Set_Offset(scopeObject, channel, offset):
    tempString = str(channel) + ":OFFSet " + str(offset)
    scopeObject.write(tempString)
    
def scope_Set_Channel_Voltage(scopeObject, channel, voltage):
    tempString = str(channel) + ":SCAle " + str(voltage)
    scopeObject.write(tempString)
    
def scope_Set_Statistics_Off(scopeObject):
    tempString = "MEASUrement:STATIstics:MODe OFF"
    scopeObject.write(tempString)
    
def scope_Set_Statistics_On(scopeObject):
    tempString = "MEASUrement:STATIstics:MODe ON"
    scopeObject.write(tempString)
    
def scope_Set_HCursor(scopeObject, valA, valB):
    tempString = "CURSor:HBArs:POSITION1 " + str(valA)
    scopeObject.write(tempString)
    tempString = "CURSor:HBArs:POSITION2 " + str(valB)
    scopeObject.write(tempString)
    tempString = "CURSor:VBArs:POSITION1 -20"
    scopeObject.write(tempString)
    tempString = "CURSor:VBArs:POSITION2 -20"
    scopeObject.write(tempString)

def scope_Set_CursorOn(scopeObject, channel):
    tempString = "CURSor:SOUrce " + str(channel)
    scopeObject.write(tempString)
    tempString = "CURSor:FUNCtion SCREEN"
    scopeObject.write(tempString)
    tempString = "CURSor:STATE ON"
    scopeObject.write(tempString)
    tempString = "CURSor:VBArs:UNIts SECOnds"
    scopeObject.write(tempString)
    
def scope_Get_HCursor_Delta(scopeObject):
    tempString = "CURSor:HBArs:DELTa?"
    return scopeObject.query(tempString)
    

    
