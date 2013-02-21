#!/usr/bin/env python
# RFPiD.py - Scan RFID Tags with Your Pi - will@nesit.org
# CREATE YOUR DATABASE AFTER YOU SCAN YOUR CARD AND GET YOUR TAG ID
# pi@raspberrypi: sudo apt-get install sqlite3
# pi@raspberrypi: sqlite3 DoorDatabase.db
# sqlite>CREATE TABLE RFID( name TEXT, card TEXT, date NUMERIC, lastentry TEXT);
# sqlite>CREATE TABLE Rejects( rejectedcard TEXT, whenrejected TEXT);  
# sqlite>INSERT INTO RFID values("illwill", "1212121212", date(), "0");
# sqlite>.exit
####################################################################          
import serial, time, sys
import sqlite3 as lite
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

TRANSISTOR = 11
GREEN_LED = 19
BLUE_LED = 21
RED_LED = 23
GPIO.setup(TRANSISTOR, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

con = lite.connect('DoorDatabase.db')


rfid_reader = "/dev/ttyUSB0"
ser = serial.Serial(rfid_reader, timeout=1)
print "Connected to RFID reader on:", rfid_reader

GPIO.output(BLUE_LED, True)           # Turn on Blue light special
try:
 while 1:                             # loop forever until a tag is read
  thetime = time.strftime("%Y-%m-%d %a %H:%M:%S", time.localtime()) # get current time
  ser.flushInput()                    # flush any extra data from the serial port
  rfid_data = ser.readline().strip()  # read the rfid data
			
  if len(rfid_data) > 0:              # check for incoming card data
   rfid_data = rfid_data[1:11]        # strip off all data but the tag number
   print "Card Scanned. Tag ID:", rfid_data          # print the tag number
   cur = con.cursor()                 # connect to the DB query the table
   cur.execute("select name from rfid where card = ?", [rfid_data])
   result = cur.fetchone()            # see if card exists and their name
            
   if not result:                     #if card found do this
    GPIO.output(BLUE_LED, False)      #turn off blue light
    GPIO.output(RED_LED, True)        #turn on red led
    time.sleep(2);                    #take a nap for 2 seconds
    GPIO.output(RED_LED, False)       #turn off red led
    GPIO.output(BLUE_LED, True)       #turn on blue light
    print "Card not found in DB."
    print "UNAUTHORIZED CARD! [",rfid_data,"] scanned at front door @ ",thetime
    cur.execute("INSERT INTO Rejects (rejectedcard, whenrejected) VALUES(?,?)", (rfid_data, thetime))
    con.commit()
    cur.close() 
    continue
   else:
    GPIO.output(TRANSISTOR, True)     #trigger the Transistor to open the door strike
    GPIO.output(BLUE_LED, False)      #turn off blue light
    GPIO.output(GREEN_LED, True)      #turn on green led
    time.sleep(2);                    #take a nap for 2 seconds
    GPIO.output(GREEN_LED, False)     #turn off green led
    GPIO.output(BLUE_LED, True)       #turn on blue light
    GPIO.output(TRANSISTOR, False)    #trigger the Transistor to close the doorstrike
    print "Card found in DB."
    print result[0],"entered front door @",thetime
    cur.execute("UPDATE RFID SET lastentry=(?) WHERE card=(?)",  (thetime, rfid_data))
    con.commit()
    cur.close() 

	
except KeyboardInterrupt:             # if ctrl-c'd , cleanup your mess and exit
        GPIO.cleanup()
        ser.close()
