# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:41:28 2019

@author: v-stpur
"""
import pySerial_Big as serial 
import serial as pySerial
import sys
import time

class microSlammer():

    def __init__(self):
        print ("Initiate Slammer Class")
        
    def openSerialPort_noRepl(self, port):
        try:
            self.pyb = serial.Pyboard(port, 9600, 'micro', 'python', 0)
            return True
        except serial.PyboardError as er:
            print(er)
            return False
    

    def openSerialPort(self, port):
        print ("got to here 1")
        time.sleep(2)
        buf = {}
        try:
            self.pyb = serial.Pyboard(port, 9600, 'micro', 'python', 0)
        except serial.PyboardError as er:
            print ("error")
            print(er)
            sys.exit(1)
    
        try:
            print ("enter repl")
            self.pyb.enter_raw_repl()
            return True
        except serial.PyboardError as er:
            print(er)
            self.pyb.close()
            return False
#            sys.exit(1)
#        buf[0] = "pyb.LED(1).on()"
#        buf[1] = "pyb.LED(2).on()"
#        for index in range(0,2):
#            try:
##                print (buf[index])
#                ret, ret_err = self.pyb.exec_raw(buf[index], timeout=None)
#                return ret_err
#            except serial.PyboardError as er:
#                print(er)
#                self.pyb.close()
#                sys.exit(1)
#            except KeyboardInterrupt:
#                sys.exit(1)
#            if ret_err:
#                self.pyb.exit_raw_repl()
#                self.pyb.close()
#                print(ret_err)
#                sys.exit(1)

    def write_Command_to_Micro(self, buf):
        
        for index in range(0,len(buf)):
            try:
#                print (buf[index])
#                ret, ret_err = self.pyb.exec_raw_no_wait(buf[index], timeout=None)
                #We're downloading code with an endless loop so no response possible from serial port
                #Just assume it works
                self.pyb.exec_raw_no_wait(buf[index], timeout=None)
            except serial.PyboardError as er:
                print(er)
                self.pyb.close()
#                sys.exit(1)
        print ("done with write command")

    def re_Enter_Repl(self):
        self.pyb.exit_raw_repl()
#                self.pyb.close()
#                try:
#                    print ("here first")
#                    self.pyb = serial.Pyboard('COM4', 9600, 'micro', 'python', 0)
#                    print ("now here")
#                except serial.PyboardError as er:
#                    print(er)
#                    sys.exit(1)
            
        try:
            print ("enter repl because of slider or first time")
            self.pyb.enter_raw_repl()
        except serial.PyboardError as er:
            print(er)
            self.pyb.close()
            sys.exit(1)
                
    def reset_Board(self):
        buf = {}
        buf[0] = "import machine"
        buf[1] = "machine.reset()"

        self.write_Command_to_Micro(buf)

    def soft_Reset(self):
        self.pyb.soft_reset() # ctrl-D: soft reset

    def hard_Reset(self):
        self.pyb.hard_reset() # ctrl-D: soft reset

    def close_Serial(self):
        self.pyb.close() # ctrl-D: soft reset

    def check_presence(self, correct_port, interval=0.1):
        self.pyb.check_Presence(correct_port)

    def exit_Repl(self):
        self.pyb.exit_raw_repl()
        
    def write_Main(self):
        
        buf = {}

        buf[0] = "f = open('main.py', 'w')"
        buf[1] = "f.write('from pyb import Pin, Timer')"
        buf[2] = "f.write('\\n')"
#        buf[3] = 'f.write("p = Pin(\'X1\') # X1 has TIM2, CH1")'
#        buf[4] = "f.write('\\n')"
#        buf[5] = "f.write('tim = Timer(2, freq=1000)')"
#        buf[6] = "f.write('\\n')"
#        buf[7] = "f.write('ch = tim.channel(1, Timer.PWM, pin=p)')"
#        buf[8] = "f.write('\\n')"
#        buf[9] = "f.write('ch.pulse_width_percent(50)')"
#        buf[10] = "f.write('\\n')"
        buf[3] = 'f.write("pyb.LED(1).off()")'
        buf[4] = "f.write('\\n')"
        buf[5] = 'f.write("pyb.LED(2).on()")'
        buf[6] = "f.write('\\n')"
        buf[7] = 'f.write("pyb.LED(3).off()")'
        buf[8] = "f.write('\\n)"

#        buf[17] = "f.close()"
        buf[9] = "f.close()"

        self.write_Command_to_Micro(buf)

    def write_Main_back(self):
        
        buf = {}

        buf[0] = "f = open('main.py', 'w')"
        buf[1] = "f.write('import utime, ustruct, pyb')"
        buf[2] = "f.write('\\n')"
        buf[3] = "f.write('from pyb import USB_VCP')"
        buf[4] = "f.write('\\n')"
        buf[5] = "f.write('import assembly')"
        buf[6] = "f.write('\\n')"
        buf[7] = "f.write('usb = USB_VCP()')"
        buf[8] = "f.write('\\n')"
        buf[9] = "f.write('usb.setinterrupt(-1)')"
        
        buf[10] = "f.write('\\n')"
        buf[11] = 'f.write("dac1 = pyb.DAC(pyb.Pin(\'X5\'))")'
        buf[12] = "f.write('\\n')"
        buf[13] = 'f.write("dac2 = pyb.DAC(pyb.Pin(\'X6\'))")'
        
        buf[14] = "f.write('\\n')"
        buf[15] = 'f.write("pwmDc = pyb.Pin(\'X1\')")'
        buf[16] = "f.write('\\n')"
        buf[17] = 'f.write("tim = pyb.Timer(6, freq=10000)")'
        buf[18] = "f.write('\\n')"
        buf[19] = 'f.write("#pwmCh = tim.channel(1, pyb.Timer.PWM, pin=pwmDc)")'
#        buf[17] = 'f.write("pwmCh = tim.callback(lambda t:pyb.Pin(\'X5\'))")'

        buf[20] = "f.write('\\n')"
        buf[21] = 'f.write("amplitude, Stop = 999, True")'
        buf[22] = "f.write('\\n')"
        buf[23] = 'f.write("onTime = 900")'
        buf[24] = "f.write('\\n')"
        buf[25] = 'f.write("offTime = 900")'
        buf[26] = "f.write('\\n')"

        buf[27] = "f.write('while Stop:')"
        buf[28] = "f.write('\\n\\t')"

        buf[29] = "f.write('cmd = usb.recv(4, timeout=5000)')"
        buf[30] = "f.write('\\n\\t')"
        buf[31] = 'f.write("usb.write(cmd)")'
        buf[32] = "f.write('\\n\\t')"
        #Start
        buf[33] = 'f.write("if (cmd == b\'strt\'):")'
        buf[34] = "f.write('\\n\\t\\t')"
        buf[35] = 'f.write("pyb.LED(1).on()")'
        buf[36] = "f.write('\\n\\t\\t')"
        buf[37] = 'f.write("pyb.LED(2).off()")'
        buf[38] = "f.write('\\n\\t\\t')"
        buf[39] = 'f.write("pyb.LED(3).off()")'
        buf[40] = "f.write('\\n\\t\\t')"
#        buf[41] = "f.write('assembly.flash_led(15625, amplitude, onTime, offTime)')"
#        buf[41] = "f.write('assembly.flash_led(7625, amplitude, onTime, offTime)')"
        buf[41] = "f.write('assembly.flash_led(7625, amplitude, onTime, offTime)')"
        buf[42] = "f.write('\\n\\t')"
        #Amplitude
        buf[43] = 'f.write("elif (cmd == b\'ampl\'):")'

        buf[44] = "f.write('\\n\\t\\t')"
        buf[45] = 'f.write("data1 = bytes(8)")'
        buf[46] = "f.write('\\n\\t\\t')"
        buf[47] = "f.write('cmd = usb.recv(4, timeout=5000)')"
        buf[48] = "f.write('\\n\\t\\t')"
        buf[49] = 'f.write("data1 = ustruct.unpack(\'L\', cmd)")'
        buf[50] = "f.write('\\n\\t\\t')"
        buf[51] = 'f.write("dataList1 = list(data1)")'
        buf[52] = "f.write('\\n\\t\\t')"
        buf[53] = "f.write('\\n\\t\\t')"
        buf[54] = 'f.write("dataStr1 = [str(i) for i in dataList1]")'
        buf[55] = "f.write('\\n\\t\\t')"
        buf[56] = "f.write('percent = int(\"\".join(dataStr1)) ')"
        buf[57] = "f.write('\\n\\t\\t')"
        buf[58] = 'f.write("usb.write(ustruct.pack(\'L\', percent))")'

        buf[59] = "f.write('\\n\\t\\t')"
        buf[60] = 'f.write("pwmCh.pulse_width_percent(percent)")'
        
        #Slew Rate
        buf[61] = "f.write('\\n\\t')"
        buf[62] = 'f.write("elif (cmd == b\'slew\'):")'
        buf[63] = "f.write('\\n\\t\\t')"
        buf[64] = "f.write('\\n\\t\\t')"

        buf[37 + 28] = 'f.write("pyb.LED(1).off()")'
        buf[38 + 28] = "f.write('\\n\\t\\t')"
        buf[39 + 28] = 'f.write("pyb.LED(2).on()")'
        buf[40 + 28] = "f.write('\\n\\t\\t')"
        buf[41 + 28] = 'f.write("pyb.LED(3).off()")'
        buf[42 + 28] = "f.write('\\n\\t\\t')"
        
        buf[43 + 28] = 'f.write("data = bytes(8)")'
        buf[44 + 28] = "f.write('\\n\\t\\t')"
        buf[45 + 28] = "f.write('cmd = usb.recv(4, timeout=5000)')"
        buf[46 + 28] = "f.write('\\n\\t\\t')"
        buf[47 + 28] = 'f.write("data = ustruct.unpack(\'L\', cmd)")'
        buf[48 + 28] = "f.write('\\n\\t\\t')"
        buf[49 + 28] = 'f.write("dataList = list(data)")'
        buf[50 + 28] = "f.write('\\n\\t\\t')"
        buf[51 + 28] = 'f.write("dataStr = [str(i) for i in dataList]")'
        buf[52 + 28] = "f.write('\\n\\t\\t')"
        buf[53 + 28] = "f.write('amplitude = int(\"\".join(dataStr)) ')"
        buf[54 + 28] = "f.write('\\n\\t\\t')"
        buf[55 + 28] = 'f.write("usb.write(ustruct.pack(\'L\', amplitude))")'
        #On Time
        buf[56 + 28] = "f.write('\\n\\t')"
        buf[57 + 28] = 'f.write("elif (cmd == b\'onTm\'):")'
        
        buf[58 + 28] = "f.write('\\n\\t\\t')"
        buf[59 + 28] = 'f.write("pyb.LED(1).off()")'
        buf[60 + 28] = "f.write('\\n\\t\\t')"
        buf[61 + 28] = 'f.write("pyb.LED(2).on()")'
        buf[62 + 28] = "f.write('\\n\\t\\t')"
        buf[63 + 28] = 'f.write("pyb.LED(3).on()")'
        buf[64 + 28] = "f.write('\\n\\t\\t')"
        
        buf[65 + 28] = 'f.write("data = bytes(8)")'
        buf[66 + 28] = "f.write('\\n\\t\\t')"
        buf[67 + 28] = "f.write('cmd = usb.recv(4, timeout=5000)')"
        buf[68 + 28] = "f.write('\\n\\t\\t')"
        buf[69 + 28] = 'f.write("data = ustruct.unpack(\'L\', cmd)")'
        buf[70 + 28] = "f.write('\\n\\t\\t')"
        buf[71 + 28] = 'f.write("dataList = list(data)")'
        buf[72 + 28] = "f.write('\\n\\t\\t')"
        buf[73 + 28] = 'f.write("dataStr = [str(i) for i in dataList]")'
        buf[74 + 28] = "f.write('\\n\\t\\t')"
        buf[75 + 28] = "f.write('onTime = int(\"\".join(dataStr)) ')"
        buf[76 + 28] = "f.write('\\n\\t\\t')"
        buf[77 + 28] = 'f.write("usb.write(ustruct.pack(\'L\', onTime))")'
        
        #Duty Cylce
        buf[78 + 28] = "f.write('\\n\\t')"
        buf[79 + 28] = 'f.write("elif (cmd == b\'duty\'):")'
        
        buf[80 + 28] = "f.write('\\n\\t\\t')"
        buf[81 + 28] = 'f.write("pyb.LED(1).on()")'
        buf[82 + 28] = "f.write('\\n\\t\\t')"
        buf[83 + 28] = 'f.write("pyb.LED(2).on()")'
        buf[84 + 28] = "f.write('\\n\\t\\t')"
        buf[85 + 28] = 'f.write("pyb.LED(3).off()")'
        buf[86 + 28] = "f.write('\\n\\t\\t')"
        
        buf[87 + 28] = 'f.write("data = bytes(8)")'
        buf[88 + 28] = "f.write('\\n\\t\\t')"
        buf[89 + 28] = "f.write('cmd = usb.recv(4, timeout=5000)')"
        buf[90 + 28] = "f.write('\\n\\t\\t')"
        buf[91 + 28] = 'f.write("data = ustruct.unpack(\'L\', cmd)")'
        buf[92 + 28] = "f.write('\\n\\t\\t')"
        buf[93 + 28] = 'f.write("dataList = list(data)")'
        buf[94 + 28] = "f.write('\\n\\t\\t')"
        buf[95 + 28] = 'f.write("dataStr = [str(i) for i in dataList]")'
        buf[96 + 28] = "f.write('\\n\\t\\t')"
        buf[97 + 28] = "f.write('offTime = int(\"\".join(dataStr)) ')"
        buf[98 + 28] = "f.write('\\n\\t\\t')"
        buf[99 + 28] = 'f.write("usb.write(ustruct.pack(\'L\', offTime))")'
        buf[100 + 28] = "f.write('\\n\\t\\t')"
        
        
        #Quit
        buf[101 + 28] = "f.write('\\n\\t')"
        buf[102 + 28] = 'f.write("elif (cmd == b\'quit\'):")'

        buf[103 + 28] = "f.write('\\n\\t\\t')"
        buf[104 + 28] = 'f.write("pyb.LED(1).off()")'
        buf[105 + 28] = "f.write('\\n\\t\\t')"
        buf[106 + 28] = 'f.write("pyb.LED(2).off()")'
        buf[107 + 28] = "f.write('\\n\\t\\t')"
        buf[108 + 28] = 'f.write("pyb.LED(3).on()")'
        buf[109 + 28] = "f.write('\\n\\t\\t')"
        buf[110 + 28] = "f.write('utime.sleep(1)')"
        buf[111 + 28] = "f.write('\\n\\t\\t')"
        buf[112 + 28] = 'f.write("#pyb.LED(3).off()")'
        buf[113 + 28] = "f.write('\\n\\t\\t')"
        buf[114 + 28] = "f.write('Stop = False')"
        buf[115 + 28] = "f.write('\\n\\t')"
        
        buf[116 + 28] = 'f.write("else:")'
        buf[117 + 28] = "f.write('\\n\\t\\t')"
        buf[118 + 28] = 'f.write("pyb.LED(1).on()")'
        buf[119 + 28] = "f.write('\\n\\t\\t')"
        buf[120 + 28] = 'f.write("pyb.LED(2).on()")'
        buf[121 + 28] = "f.write('\\n\\t\\t')"
        buf[122 + 28] = 'f.write("pyb.LED(3).on()")'

        buf[123 + 28] = "f.write('\\n')"
        buf[124 + 28] = "f.write('utime.sleep(2)')"
        buf[125 + 28] = "f.write('\\n')"
        buf[126 + 28] = 'f.write("pyb.LED(3).off()")'

        buf[127 + 28] = "f.close()"

        self.write_Command_to_Micro(buf)

    def write_SigGen(self):

        buf = {}
        
        buf[0]  = "f = open('sigGen.py', 'w')"
        buf[1]  = "f.write('import pyb')"
        buf[2]  = "f.write('\\n')"
        buf[3]  = "f.write('import time')"
        buf[4]  = "f.write('\\n')"
        buf[5]  = "f.write('import variables')"
        buf[6]  = "f.write('\\n')"
        buf[7]  = "f.write('from pyb import Pin, DAC')"
        buf[8]  = "f.write('\\n')"
        #Define toggleLED
#        buf[5]  = "f.write('def toggleLED():')"
#        buf[6]  = "f.write('\\n\\t')"
#        buf[7]  = "f.write('while True:')"
#        buf[8]  = "f.write('\\n\\t\\t')"
#        buf[9]  = "f.write('pyb.LED(1).off()')"
#        buf[10] = "f.write('\\n\\t\\t')"
#        buf[11] = "f.write('pyb.LED(2).on()')"
#        buf[12] = "f.write('\\n\\t\\t')"
#        buf[13] = "f.write('time.sleep(3)')"
#        buf[14] = "f.write('\\n\\t\\t')"
#        buf[15] = "f.write('pyb.LED(1).on()')"
#        buf[16] = "f.write('\\n\\t\\t')"
#        buf[17] = "f.write('pyb.LED(2).off()')"
#        buf[18] = "f.write('\\n\\t\\t')"
#        buf[19] = "f.write('time.sleep(3)')"
#        buf[20] = "f.close()"
        #Define squareWave
        buf[9] = "f.write('def squareWave():')"
        buf[10] = "f.write('\\n\\t')"
        buf[11]  = 'f.write("dAPort = \'X5\'")'
        buf[12]  = "f.write('\\n\\t')"
        buf[13] = "f.write('pyb.LED(3).on()')"
        buf[14] = "f.write('\\n\\t')"
        buf[15] = "f.write('pyb.LED(1).off()')"
        buf[16] = "f.write('\\n\\t')"
        buf[17] = "f.write('pyb.LED(2).off()')"
        buf[18] = "f.write('\\n\\t')"
        buf[19] = "f.write('time.sleep(0.01)')"
        buf[20] = "f.write('\\n\\t')"
        buf[21] = 'f.write("dac = DAC(Pin(\'X5\'))")'
        buf[22] = "f.write('\\n\\t')"
        buf[23] = "f.write('while True:')"
        buf[24] = "f.write('\\n\\t\\t')"
        buf[25] = "f.write('dac.write(variables.amplitude)')"
        buf[26] = "f.write('\\n\\t\\t')"
        buf[27] = "f.write('pyb.udelay(variables.onTime)')"
        buf[28] = "f.write('\\n\\t\\t')"
        buf[29] = "f.write('dac.write(0)')"
        buf[30] = "f.write('\\n\\t\\t')"
        buf[31] = "f.write('pyb.udelay(10000)')"
        buf[32] = "f.close()"

        self.write_Command_to_Micro(buf)
                
    def write_DefaultVariables(self):

        buf = {}
        
        buf[0]  = "f = open('variables.py', 'w')"
        buf[1]  = "f.write('\\n')"
        buf[2]  = "f.write('amplitude = 4095')"
        buf[3]  = "f.write('onTime = 50')"
        buf[4] = "f.close()"

        self.write_Command_to_Micro(buf)
        
    def update_Variables(self, amplitude):

        buf = {}
        
        buf[0]  = "f = open('variables.py', 'w')"
        buf[1]  = "f.write('\\n')"
        buf[2]  = "f.write('amplitude = " + str(amplitude) + "')"
        buf[2]  = "f.write('onTime = 100')"
        buf[3]  = "f.close()"

        self.write_Command_to_Micro(buf)

    def test_InlineAssembler_Back(self):

        buf = {}

        buf[0]  = "f = open('assembly.py', 'w')"
        buf[1]  = "f.write('@micropython.asm_thumb')"
        buf[2]  = "f.write('\\n')"
        #Recieve all available arguments
        buf[3]  = "f.write('def flash_led(r0, r1, r2, r3):')"
        buf[4]  = "f.write('\\n\\t')"
        #Save TIM6 offset into r5 
        buf[5]  = "f.write('movwt(r5, stm.TIM6)')"
        buf[6]  = "f.write('\\n\\t')"
        buf[7]  = "f.write('movwt(r4, 1)')"
        buf[8]  = "f.write('\\n\\t')"
        buf[9]  = "f.write('str(r4, [r5, stm.TIM_CR1])')"
        buf[10]  = "f.write('\\n\\t')"
        buf[11]  = "f.write('movwt(r4, 0x20)')"
        buf[12]  = "f.write('\\n\\t')"
        buf[13]  = "f.write('str(r4, [r5, stm.TIM_CR2])')"
        buf[14]  = "f.write('\\n\\t')"
        #Save DAC offset into r5 dont touch r5 after this
        buf[15]  = "f.write('movwt(r5, stm.DAC)')"
        buf[16]  = "f.write('\\n\\t')"
        #Enable both DACs
#        buf[17]  = "f.write('movwt(r4, 0x10071007)')"
        buf[17]  = "f.write('movwt(r4, 0x70007)')"
        buf[18]  = "f.write('\\n\\t')"
        buf[19]  = "f.write('str(r4, [r5, stm.DAC_CR])')"
        buf[20]  = "f.write('\\n\\t')"
        #Saver1 into r6. Probably don't need to do this
        buf[21]  = "f.write('movw(r6, 2)')"
        buf[22]  = "f.write('\\n\\t')"
        #Divie r1 by two for half amplitude output.
#        buf[14]  = "f.write('mov(r4, r6)')"
        buf[23]  = "f.write('udiv(r4, r1, r6)')"
        buf[24]  = "f.write('\\n\\t')"
        buf[25]  = "f.write('str(r4, [r5, stm.DAC_DHR12R2])')"
        buf[26]  = "f.write('\\n\\t')"
        #Enter square wave loop
        buf[27]  = "f.write('b(loop_entry)')"
        buf[28]  = "f.write('\\n\\t')"
        buf[29]  = "f.write('label(loop1)')"
        
        buf[30]  = "f.write('\\n\\t')"

        buf[31]  = "f.write('movw(r4, 0x0)')"
        buf[32]  = "f.write('\\n\\t')"
        buf[33]  = "f.write('str(r4, [r5, stm.DAC_DHR12R1])')"
        buf[34]  = "f.write('\\n\\t')"

        buf[35]  = "f.write('mov(r4, r2)')"
        buf[36]  = "f.write('\\n\\t')"
        buf[37]  = "f.write('label(delay_on)')"
        buf[38]  = "f.write('\\n\\t')"
        buf[39]  = "f.write('sub(r4, r4, 1)')"
        buf[40]  = "f.write('\\n\\t')"
        buf[41]  = "f.write('cmp(r4, 0)')"
        buf[42]  = "f.write('\\n\\t')"
        buf[43]  = "f.write('bgt(delay_on)')"
        buf[44]  = "f.write('\\n\\t')"
        
        buf[45]  = "f.write('mov(r4, r1)')"
        buf[46]  = "f.write('\\n\\t')"
        buf[47]  = "f.write('str(r4, [r5, stm.DAC_DHR12R1])')"

        buf[48]  = "f.write('\\n\\t')"
        buf[49]  = "f.write('mov(r4, r3)')"
        buf[50]  = "f.write('\\n\\t')"
        buf[51]  = "f.write('label(delay_off)')"
        buf[52]  = "f.write('\\n\\t')"
        buf[53]  = "f.write('sub(r4, r4, 1)')"
        buf[54]  = "f.write('\\n\\t')"
        buf[55]  = "f.write('cmp(r4, 0)')"
        buf[56]  = "f.write('\\n\\t')"
        buf[57]  = "f.write('bgt(delay_off)')"
        buf[58] = "f.write('\\n\\t')"
        buf[59]  = "f.write('sub(r0, r0, 1)')"
        buf[60]  = "f.write('\\n\\t')"
        buf[61]  = "f.write('label(loop_entry)')"
        buf[62]  = "f.write('\\n\\t')"
        buf[63]  = "f.write('cmp(r0, 0)')"
        buf[64]  = "f.write('\\n\\t')"
        buf[65]  = "f.write('bgt(loop1)')"
        buf[66] = "f.close()"

        self.write_Command_to_Micro(buf)

    def test_InlineAssembler(self):

        buf = {}

        buf[0]  = "f = open('assembly.py', 'w')"
        buf[1]  = "f.write('@micropython.asm_thumb')"
        buf[2]  = "f.write('\\n')"
        #Recieve all available arguments
        buf[3]  = "f.write('def flash_led(r0, r1, r2, r3):')"
        buf[4]  = "f.write('\\n\\t')"
        #Save TIM6 offset into r5 
        buf[5]  = "f.write('movwt(r5, stm.TIM6)')"
        buf[6]  = "f.write('\\n\\t')"
        buf[7]  = "f.write('movwt(r4, 4000)')"
        buf[8]  = "f.write('\\n\\t')"
        buf[9]  = "f.write('str(r4, [r5, stm.TIM_ARR])')"
        buf[10]  = "f.write('\\n\\t')"
        buf[11]  = "f.write('movwt(r4, 0x81)')"
        buf[12]  = "f.write('\\n\\t')"
        buf[13]  = "f.write('str(r4, [r5, stm.TIM_CR1])')"
        buf[14]  = "f.write('\\n\\t')"
        buf[15]  = "f.write('movwt(r4, 0x20)')"
        buf[16]  = "f.write('\\n\\t')"
        buf[17]  = "f.write('str(r4, [r5, stm.TIM_CR2])')"
        buf[18]  = "f.write('\\n\\t')"
        #Save DAC offset into r5 dont touch r5 after this
        buf[19]  = "f.write('movwt(r5, stm.DAC)')"
        buf[20]  = "f.write('\\n\\t')"
        #Enable both DACs
        buf[21]  = "f.write('movwt(r4, 0x10071007)')"
#        buf[21]  = "f.write('movwt(r4, 0x70007)')"
        buf[22]  = "f.write('\\n\\t')"
        buf[23]  = "f.write('str(r4, [r5, stm.DAC_CR])')"
        buf[24]  = "f.write('\\n\\t')"
        #Sav1 into r6. Probably don't need to do this
        buf[25]  = "f.write('movw(r6, 2)')"
        buf[26]  = "f.write('\\n\\t')"
        #Divi r1 by two for half amplitude output.
        buf[27]  = "f.write('udiv(r4, r1, r6)')"
        buf[28]  = "f.write('\\n\\t')"
        buf[29]  = "f.write('str(r4, [r5, stm.DAC_DHR12R2])')"
        buf[30]  = "f.write('\\n\\t')"
        #Enter square wave loop
        buf[31]  = "f.write('b(loop_entry)')"
        buf[32]  = "f.write('\\n\\t')"
        buf[33]  = "f.write('label(loop1)')"
        buf[34]  = "f.write('\\n\\t')"
        buf[35]  = "f.write('movw(r4, 0x0)')"
        buf[36]  = "f.write('\\n\\t')"
        buf[37]  = "f.write('str(r4, [r5, stm.DAC_DHR12R1])')"
        buf[38]  = "f.write('\\n\\t')"
        buf[39]  = "f.write('movwt(r4, stm.TIM6)')"
        buf[40]  = "f.write('\\n\\t')"
        buf[41]  = "f.write('label(delay_on)')"
        buf[42]  = "f.write('\\n\\t')"
        buf[43]  = "f.write('ldr(r4, [r4, stm.TIM_SR])')"
        buf[44]  = "f.write('\\n\\t')"
        buf[45]  = "f.write('cmp(r4, 1)')"
        buf[46]  = "f.write('\\n\\t')"
        buf[47]  = "f.write('blt(delay_on)')"
        buf[48]  = "f.write('\\n\\t')"
        buf[49]  = "f.write('mov(r4, r1)')"
        buf[50]  = "f.write('\\n\\t')"
        buf[51]  = "f.write('str(r4, [r5, stm.DAC_DHR12R1])')"
        buf[52]  = "f.write('\\n\\t')"
        buf[53]  = "f.write('movwt(r4, stm.TIM6)')"
        buf[54]  = "f.write('\\n\\t')"
        buf[55]  = "f.write('label(delay_off)')"
        buf[56]  = "f.write('\\n\\t')"
        buf[57]  = "f.write('ldr(r4, [r4, stm.TIM_SR])')"
        buf[58]  = "f.write('\\n\\t')"
        buf[59]  = "f.write('cmp(r4, 1)')"
        buf[60]  = "f.write('\\n\\t')"
        buf[61]  = "f.write('blt(delay_off)')"
        buf[62] = "f.write('\\n\\t')"
        buf[63]  = "f.write('sub(r0, r0, 1)')"
        buf[64]  = "f.write('\\n\\t')"
        buf[65]  = "f.write('label(loop_entry)')"
        buf[66]  = "f.write('\\n\\t')"
        buf[67]  = "f.write('cmp(r0, 0)')"
        buf[68]  = "f.write('\\n\\t')"
        buf[69]  = "f.write('b(loop1)')"
        buf[70] = "f.close()"

        self.write_Command_to_Micro(buf)

    def update_InlineAssembler(self):

        buf = {}

        buf[0]  = "@micropython.asm_thumb"
        buf[1]  = "movw(r6, 0x3FF)"

        self.write_Command_to_Micro(buf)

    def test_SerialComs(self):

        self.pyb.write_Line("go\n")
        time.sleep(0.51)
        print (self.pyb.read_Line)
#        port = "COM4"
##            sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)
#        sp = pySerial.Serial(port, baudrate=9600, interCharTimeout=1)
##            sp.setDTR(True) # dsrdtr is ignored on Windows.
#        sp.write(str.encode('B\n'))
#        sp.flush()
#        value = 0
##            size = struct.unpack('<L', sp.read(4))[0]
##            img = sp.read(size)
#        while True:
#            value += 1
#            img = sp.readline()
#            time.sleep(0.1)
#            print(img)
#            sp.write(str.encode(str(value) + '\n'))
#        sp.close()
