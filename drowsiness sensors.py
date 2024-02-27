#python drowniness_yawn.py --webcam webcam_index

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os
import serial
import RPi.GPIO as  GPIO

import smbus
import time
from time import sleep
import sys
import sys
import urllib.request

bus = smbus.SMBus(1)

bus.write_byte_data(0x53, 0x2C, 0x0B)
value = bus.read_byte_data(0x53, 0x31)
value &= ~0x0F;
value |= 0x0B;  
value |= 0x08;
bus.write_byte_data(0x53, 0x31, value)
bus.write_byte_data(0x53, 0x2D, 0x08)
#wp = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=MW6ESOWJ00JZVEC3&field1=0" + "&field2=" +str(0) + "&field3=" +str(0))
     

def getAxes():
    bytes = bus.read_i2c_block_data(0x53, 0x32, 6)
        
    x = bytes[0] | (bytes[1] << 8)
    if(x & (1 << 16 - 1)):
        x = x - (1<<16)

    y = bytes[2] | (bytes[3] << 8)
    if(y & (1 << 16 - 1)):
        y = y - (1<<16)

    z = bytes[4] | (bytes[5] << 8)
    if(z & (1 << 16 - 1)):
        z = z - (1<<16)

    x = x * 0.004 
    y = y * 0.004
    z = z * 0.004

    x = x * 9.80665
    y = y * 9.80665
    z = z * 9.80665

    x = round(x, 1)
    y = round(y, 1)
    z = round(z, 1)

##    print("   x = %.3f ms2" %x)
##    print("   y = %.3f ms2" %y)
##    print("   z = %.3f ms2" %z)
##    print("\n\n")
    
    return {x, y}




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

als = 20
m1  = 26
m2 = 19
m3 = 13
m4 = 6
sb=21
buz=17
GPIO.setup(buz, GPIO.OUT) 
GPIO.setup(m1, GPIO.OUT)
GPIO.setup(m2, GPIO.OUT) 
GPIO.setup(m3, GPIO.OUT) 
GPIO.setup(m4, GPIO.OUT) 
GPIO.setup(als, GPIO.IN)
GPIO.setup(sb, GPIO.IN) 
GPIO.output(buz,0)

kk=0
def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    #print("NMEA Time: ", nmea_time,'\n')
    #print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    try:
        lat = float(nmea_latitude)                  #convert string into float for calculation
        longi = float(nmea_longitude)               #convertr string into float for calculation
    except:
        lat=0
        longi=0
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position


gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0


time.sleep(1.0)
GPIO.output(m1,1)
GPIO.output(m2,0)
GPIO.output(m3,1)
GPIO.output(m4,0)
ii=0

while True:

    
   
    received_data = (str)(ser.readline())                   #read NMEA string received
    GPGGA_data_available = received_data.find(gpgga_info) 
    if(kk==0):
        lat_in_degrees=0
        lat_in_degrees=0
    if (GPGGA_data_available>0):
        kk=1
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
        GPS_Info()                                          #get time, latitude, longitude
        map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map
            
    map_link = 'http://maps.google.com/?q=' + str(16.4963) + ',' + str(80.5007)    #create link to plot location on Google map
    print(map_link)
    print()

    x,y=getAxes()
    print("X:"+ str(x))
    print("Y:"+ str(y))
    #time.sleep(3)

    aval=1-GPIO.input(als)
    print("ALCOHOLIC:"+ str(aval))

    sval=1-GPIO.input(sb)
    print("SB:"+ str(sval))
    if(sval==1):
        GPIO.output(buz,1)
        time.sleep(0.5)
        GPIO.output(buz,0)
        time.sleep(0.5)    

    if(aval==1):
        GPIO.output(buz,1)
        GPIO.output(m1,0)
        GPIO.output(m2,0)
        GPIO.output(m3,0)
        GPIO.output(m4,0)

    if(x<-6.5 or y<-6.5 or x>6.5 or y>6.5):
        print('Accident...')
        GPIO.output(buz,1)
        GPIO.output(m1,0)
        GPIO.output(m2,0)
        GPIO.output(m3,0)
        GPIO.output(m4,0)
        wp = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=5JXYCST9SUCAJQS4&field1=1" + "&field2=" +str(16.4963) + "&field3=" +str(80.5007))
        
        while(1):
            time.sleep(1)
             
  
