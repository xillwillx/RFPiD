#!/usr/bin/env python          
import serial, time, sys
import sqlite3 as lite
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

TRANSISTOR = 11
BLUE_LED = 21
GREEN_LED = 19
RED_LED = 23
GPIO.setup(TRANSISTOR, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

con = lite.connect('/home/pi/raspi_gtalk_robot/DoorDatabase.db')
thetime = time.strftime("%H:%M:%S", time.localtime())

rfid_reader = "/dev/ttyUSB0"
ser = serial.Serial(rfid_reader, timeout=1)
print "Connected to RFID reader on:", rfid_reader

GPIO.output(BLUE_LED, True)                     # Turn on Blue light special
try:
 while 1:                                    # loop forever until a tag is read
  ser.flushInput()                    # flush any extra data from the serial port
  rfid_data = ser.readline().strip()  # read the rfid data
			
  if len(rfid_data) > 0:                      # check for incoming card data
   rfid_data = rfid_data[1:11]         # strip off all data but the tag number
   print "Card Scanned. Tag ID:", rfid_data          # print the tag number
   cur = con.cursor()                  # connect to the DB query the table
   cur.execute("select name from rfid where card = ?", [rfid_data])
   result = cur.fetchone()
            
   if not result:                               #if card found do this
    GPIO.output(BLUE_LED, False)   #turn off blue light
    GPIO.output(RED_LED, True)     #turn on red led
    time.sleep(2);                 #take a nap for 2 seconds
    GPIO.output(RED_LED, False)    #turn off red led
    GPIO.output(BLUE_LED, True)    #turn on blue light
    print "Card not found in DB."
    print "UNAUTHORIZED CARD! [",rfid_data,"] scanned at front door @ ",thetime              # print "Card not found in DB."
    continue
   else:
    GPIO.output(TRANSISTOR, True)  # Trigger the Transistor to open the doorstrike
    GPIO.output(BLUE_LED, False)   #turn off blue light
    GPIO.output(GREEN_LED, True)   #turn on green led
    time.sleep(2);                 #take a nap for 2 seconds
    GPIO.output(GREEN_LED, False)  #turn off green led
    GPIO.output(BLUE_LED, True)    #turn on blue light
    GPIO.output(TRANSISTOR, False) # Trigger the Transistor to close the doorstrike
    print "Username:", result[0]
    print result[0],"entered front door @",thetime
	
except KeyboardInterrupt:                      # if ctrl-c'd , cleanup your mess and exit
        GPIO.cleanup()
        ser.close()