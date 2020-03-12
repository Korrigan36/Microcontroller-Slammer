import utime, ustruct, pyb
import math
from array import array
from pyb import USB_VCP
usb = USB_VCP()
usb.setinterrupt(-1)
dac1 = pyb.DAC(pyb.Pin('X5'), bits=12)
dac2 = pyb.DAC(pyb.Pin('X6'), bits=12)
pwmGain = pyb.Pin('X1')
pwmSlew = pyb.Pin('X2')
pwmBias = pyb.Pin('X3')
tim2 = pyb.Timer(2, freq=10000)
tim5 = pyb.Timer(5, freq=1000000)
pwmBiasCh = tim5.channel(3, pyb.Timer.PWM, pin=pwmBias)
pwmGainCh = tim5.channel(1, pyb.Timer.PWM, pin=pwmGain)
pwmBiasCh.pulse_width_percent(50)
pwmSlewCh = tim2.channel(2, pyb.Timer.PWM, pin=pwmSlew)
amplitude, Stop = 999, True
frequency = 10000
duty = 10

while Stop:
	cmd = usb.recv(4, timeout=5000)
	usb.write(cmd)
	if (cmd == b'strt'):
        	pyb.LED(1).on()
        	pyb.LED(2).off()
        	pyb.LED(3).off()
        	utime.sleep(1)
        	tim2 = pyb.Timer(2, freq=10000)
        	pwmSlewCh.pulse_width_percent(duty)
	elif (cmd == b'ampl'):
		data1 = bytes(8)
		cmd = usb.recv(4, timeout=5000)
		data1 = ustruct.unpack('L', cmd)
		dataList1 = list(data1)
        	dataStr1 = [str(i) for i in dataList1]
		percent = int("".join(dataStr1)) 
		usb.write(ustruct.pack('L', percent))
	elif (cmd == b'slew'):
		pyb.LED(1).off()
		pyb.LED(2).on()
		pyb.LED(3).off()
		data = bytes(8)
		cmd = usb.recv(4, timeout=5000)
		data = ustruct.unpack('L', cmd)
		dataList = list(data)
		dataStr = [str(i) for i in dataList]
		amplitude = int("".join(dataStr)) 
		usb.write(ustruct.pack('L', amplitude))
		pwmGainCh.pulse_width_percent(amplitude)
	elif (cmd == b'onTm'):
		pyb.LED(1).off()
		pyb.LED(2).on()
		pyb.LED(3).on()
		data = bytes(8)
		cmd = usb.recv(4, timeout=5000)
		data = ustruct.unpack('L', cmd)
		dataList = list(data)
		dataStr = [str(i) for i in dataList]
		onTime = int("".join(dataStr)) 
		usb.write(ustruct.pack('L', onTime))
	elif (cmd == b'duty'):
		pyb.LED(1).on()
		pyb.LED(2).on()
		pyb.LED(3).off()
		data = bytes(8)
		cmd = usb.recv(4, timeout=5000)
		data = ustruct.unpack('L', cmd)
		dataList = list(data)
		dataStr = [str(i) for i in dataList]
		duty = int("".join(dataStr)) 
		usb.write(ustruct.pack('L', duty))
        	tim2 = pyb.Timer(2, freq=10000)
        	pwmSlewCh.pulse_width_percent(duty)
		
	elif (cmd == b'quit'):
		pyb.LED(1).off()
		pyb.LED(2).off()
		pyb.LED(3).on()
		utime.sleep(1)
		#pyb.LED(3).off()
		Stop = False
	else:
		pyb.LED(1).on()
		pyb.LED(2).on()
		pyb.LED(3).on()
utime.sleep(2)
pyb.LED(3).off()