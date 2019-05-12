#!/usr/bin/python

import smbus
import math
import RPi.GPIO as GPIO
import time
import signal
import sys 

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 18
pinEcho = 24
Trig2 = 23
Echo2 = 25
Trig3 = 8
Echo3 =7

west = 0
east = 0
north = 0
control = 16

def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	# f.close()
	with open("map.txt", "w") as f:
	 	for num in range (0, len(map)):
	 		f.write("map of %d\t" % num)
	 		f.write(str(map[num]))
	 		f.write("\n")
	GPIO.cleanup() 
	sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)  

GPIO.setup(Trig2, GPIO.OUT)
GPIO.setup(Echo2, GPIO.IN)  
  
GPIO.setup(Trig3, GPIO.OUT)
GPIO.setup(Echo3, GPIO.IN)  
 
  
angle = 0
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

i=0
direction = 16
index_1 = 135
index = index_1
position = 0
map = []
for num in range(0,255):
	map.append(0)
road = 0

# f = open('map.txt','w')

while True: 
	# set Trigger to HIGH
	if i == 0:
		GPIO.output(pinTrigger, True)
		time.sleep(0.00001)
		GPIO.output(pinTrigger, False)
		startTime = time.time()
		stopTime = time.time()
		while 0 == GPIO.input(pinEcho):
			startTime = time.time()
		while 1 == GPIO.input(pinEcho):
			stopTime = time.time()
		TimeElapsed = stopTime - startTime
		distance = (TimeElapsed * 34300) / 2
		print ("Distance: %.1f cm" % distance)
		
	if i ==1:
		GPIO.output(Trig2, True)
		time.sleep(0.00001)
		GPIO.output(Trig2, False)
		startTime2 = time.time()
		stopTime2 = time.time()
		while 0 == GPIO.input(Echo2):
			startTime2 = time.time()
		while 1 == GPIO.input(Echo2):
			stopTime2 = time.time()
		TimeElapsed2 = stopTime2 - startTime2
		distance2 = (TimeElapsed2 * 34300) / 2
		print ("Distance2: %.1f cm" % distance2)
		
	if i ==2:
		GPIO.output(Trig3, True)
		time.sleep(0.00001)
		GPIO.output(Trig3, False)
		startTime3 = time.time()
		stopTime3 = time.time()
		while 0 == GPIO.input(Echo3):
			startTime3 = time.time()
		while 1 == GPIO.input(Echo3):
			stopTime3 = time.time()
		TimeElapsed3 = stopTime3 - startTime3
		distance3 = (TimeElapsed3 * 34300) / 2
		print ("Distance3: %.1f cm" % distance3)
		if distance <100:
			west = 1
		else:
			west = 0
		if distance2 <100:
			north = 8
		else:
			north = 0
		if distance3<100:
			east = 4
		else:
			east  = 0
		position = west + north + east + control
		if map[index] == 0:
			map[index] = position
		i= -1
		# print("at index %d" % index)
		# print("is position %d" %position)
		# f.write("map of %d\t" % index)
		# f.write(str(map[index]))
		# f.write("\n")
	
	gyro_xout = read_word_2c(0x43)/131
	gyro_yout = read_word_2c(0x45)/131
	gyro_zout = read_word_2c(0x47)/131
	
	print ("gyroz: %.3f " % gyro_zout)
	
	angle = angle + 0.1*(gyro_zout-1)
	
	print ("angl: %3f" % angle)
	
	acc_xout = read_word_2c(0x3b)
	acc_yout = read_word_2c(0x3d)
	acc_zout = read_word_2c(0x3f)
	
	accx = - 0.02 + acc_xout / 16384.0
	accy = 0.015 +acc_yout / 16384.0
	accz = -0.94 + acc_zout / 16384.0
	
	i=i+1
	time.sleep(0.1)
	road = road + 0.118
	index= index_1 + direction*int(road)
	print("%f\n" % index)
