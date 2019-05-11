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

def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup() 
	sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)  
  
angle = 0
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

v=0
s=0
map = []

while True: 
       # set Trigger to HIGH
    GPIO.output(pinTrigger, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)

    startTime = time.time()
    stopTime = time.time()

    # save start time
    while 0 == GPIO.input(pinEcho):
     startTime = time.time()

    # save time of arrival
    while 1 == GPIO.input(pinEcho):
     stopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    print ("Distance: %.1f cm" % distance)
    
    gyro_xout = read_word_2c(0x43)/131
    gyro_yout = read_word_2c(0x45)/131
    gyro_zout = read_word_2c(0x47)/131
    
    print ("gyroz: %.3f cm" % gyro_zout)

    angle = angle + 0.1*gyro_zout
    
    print ("angl: %3f" % angle)

    acc_xout = read_word_2c(0x3b)
    acc_yout = read_word_2c(0x3d)
    acc_zout = read_word_2c(0x3f)
    
    accx = acc_xout / 16384.0
    accy = acc_yout / 16384.0
    accz = acc_zout / 16384.0
    
    print("acx: %.3f" % accx)
    print("acy: %.3f" % accy)
    print("acz: %.3f" % accz)
    
    v = v + accx * 0.1
    s = s + v* 0.1
    
    print("v: %.3f" % v)
    print("s: %.3f" %s)
    sleep(0.1)
