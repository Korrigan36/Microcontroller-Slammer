def pulseGen_Set_Volt_High_Low(waveFormObject, amplitude, slammer):

    offset = amplitude / 2.0 + 0.003
#        tempString = "SOURCE1:VOLTAGE +" + str(amplitude)
#    waveFormObject.write("SOURCE1:VOLTAGE +" + str(amplitude))
                
    if slammer == 1:
#            print("doing slammer 1")
        tempString = "SOURCE1:VOLTAGE:OFFSET +" + str(offset)
        waveFormObject.write(tempString)
        tempString = "OUTPUT1:POLarity NORMal"
        waveFormObject.write(tempString)
    else:
#            print("doing slammer 2")
#            tempString = "SOURCE1:VOLTAGE:OFFSET -" + str(offset)
        waveFormObject.write("SOURCE1:VOLTAGE:OFFSET -" + str(offset))
#            tempString = "OUTPUT1:POLarity INVerted"
        waveFormObject.write("OUTPUT1:POLarity INVerted")
        
    waveFormObject.write("SOURCE1:VOLTAGE +" + str(amplitude))
              
def pulseGen_Set_Freq(waveFormObject, freq):
    tempString = "SOURce1:FREQuency:MODE FIXED"
    waveFormObject.write(tempString)
    tempString = "SOURCE1:FREQUENCY " + str(freq)
    waveFormObject.write(tempString)
        
def pulseGen_Set_Duty(waveFormObject, duty):
    tempString = "SOURce1:FUNCTION:PULSe:DCYCLE " + str(duty)
    waveFormObject.write(tempString)
      
def pulseGen_Check_OutputOn(waveFormObject):
    tempString = "OUTPUT1?"
    return waveFormObject.query(tempString)
    
def pulseGen_Set_OutputOn(waveFormObject):
    tempString = "OUTPUT1 ON"
    waveFormObject.write(tempString)
        
def pulseGen_Set_OutputOff(waveFormObject):
    tempString = "OUTPUT1 OFF"
    waveFormObject.write(tempString)
        
def pulseGen_Set_Mode_Pulse(waveFormObject):
    tempString = "SOURCE1:FUNCTION PULSE"
    waveFormObject.write(tempString)
    tempString = "SOURCE1:FUNCTION:PULSE:HOLD DCYCLE"
    waveFormObject.write(tempString)
       
def pulseGen_Zero_Output(waveFormObject):
    tempString = "SOURCE1:VOLTAGE MINIMUM"
    waveFormObject.write(tempString)
    tempString = "SOURCE1:VOLTAGE:OFFSET 0"
    waveFormObject.write(tempString)
      
def pulseGen_Set_Burst_Mode_Trig(waveFormObject):
    tempString = "SOURCE1:BURST:MODE TRIGGERED"
    waveFormObject.write(tempString)
         
def pulseGen_Set_Burst_NCycles(waveFormObject, numCycles):
    tempString = "SOURCE1:BURST:NCYCLES " + str(numCycles)
    waveFormObject.write(tempString)
         
def pulseGen_Set_Burst_Period(waveFormObject, burstPeriod):
    tempString = "SOURCE1:BURST:INTERNAL:PERIOD " + str(burstPeriod)
    waveFormObject.write(tempString)
         
def pulseGen_Set_Burst_On(waveFormObject):
    tempString = "SOURCE1:BURST:STATE ON "
    waveFormObject.write(tempString)
         
def pulseGen_Set_Burst_Off(waveFormObject):
    tempString = "SOURCE1:BURST:STATE OFF "
    waveFormObject.write(tempString)
         
def pulseGen_Set_Both_Edge(waveFormObject, time_ns):
    tempString = "SOURCE1:FUNCTION:PULSE:TRANSITION:BOTH " + str(time_ns) + " ns"
    waveFormObject.write(tempString)
