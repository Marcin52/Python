# //smigielko//

import smbus
import math
import RPi.GPIO as GPIO
import time
import signal
import sys 

# define gyro's registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
address = 0x68

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

#set Board pin mode
GPIO.setmode(GPIO.BCM)

#i2c reading functions
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

#program closing function
def close(signal, frame):
	print("\nTurning off and saving a map...\n")
	with open("map.txt", "w") as f:
	 	for num in range (0, len(map)):
	 		f.write("map of %d\t" % num)
	 		f.write(str(map[num]))
	 		f.write("\n")
	GPIO.cleanup() 
	sys.exit(0)

#pins setup	
signal.signal(signal.SIGINT, close)

GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)  

GPIO.setup(Trig2, GPIO.OUT)
GPIO.setup(Echo2, GPIO.IN)  
  
GPIO.setup(Trig3, GPIO.OUT)
GPIO.setup(Echo3, GPIO.IN)  
 
bus = smbus.SMBus(1)
 
#set on gyro's control register 
bus.write_byte_data(address, power_mgmt_1, 0)

#declaring global variables
i=0
direction = 16
index_1 = 135
index = index_1
walls = 0
map = []
for num in range(0,255):
	map.append(0)
road = 0
angle = 0

#main loop
while True: 
	
	#every three cycles one of three sonars makes measurment
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
		
		#chcek if there are walls
		if distance <100:
			west = 1 # binary 0000 0001
		else:
			west = 0
		if distance2 <100:
			north = 8 # binary 0000 0100
		else:
			north = 0
		if distance3<100:
			east = 4 # binary 0000 0010
		else:
			east  = 0
		# variable walls is a sum of checks on three directions
		walls = west + north + east + control
		#assign walls to actual position index
		if map[index] == 0:
			map[index] = walls
		i= -1
	#angular speed measurment
	gyro_zout = read_word_2c(0x47)/131
	print ("gyroz: %.3f " % gyro_zout)
	
	#actual angle as a sum of previous angle plus 0.1 times current angular speed
	#0.1 is a time period beetwen each loop
	angle = angle + 0.1*(gyro_zout-1)
	print ("angl: %3f" % angle)
	
	#change movement direction depending on angle
	if(angle < 90 and angle >-90):
		direction = 32
	elif (angle > 90 and angle <180):
		direction = -1
	elif (angle < -90 and angle >-180):
		direction = 1
	else:
		direction = -16
		
	#temporary variable
	i=i+1
	
	#time period
	time.sleep(0.1)
	
	#road update
	road = road + 0.118
	
	#index depending on road update and current movement direction
	index= index_1 + direction*int(road)
	print("%f\n" % index)
