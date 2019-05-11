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

angle = 0
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

while True: 
    
    gyro_xout = read_word_2c(0x43)/131
    gyro_yout = read_word_2c(0x45)/131
    gyro_zout = read_word_2c(0x47)/131

    angle = angle + 0.1*gyro_xout*math.pi/180

    acc_xout = read_word_2c(0x3b)
    acc_yout = read_word_2c(0x3d)
    acc_zout = read_word_2c(0x3f)

    accx = acc_xout / 16384.0
    accy = acc_yout / 16384.0
    accz = acc_zout / 16384.0

    print("gx " + str(gyro_xout) + "acx " + str(accx) + "acy " + str(accy) + "acz " + str(accz) + "ang " str(angle))

    sleep(0.1)
