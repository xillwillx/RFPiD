This is code to read data from a ID-20 RFID reader connected to a sparkfun USB breakout board
https://www.sparkfun.com/products/11505 for the ID-12 + USB board Kit $49.99

Once the data is read, it checks a SQLite DB for a valid RFID tag number. If a valid card is 
found it'll turn the RGB LED green and trigger a TIP31A transistor to unlock a 12v door strike. 
You can get one from eBay for about $25 http://www.ebay.com/sch/i.html?_nkw=Electric+Strike+v5

If invalid card is found, it will turn the RGB LED red.

Items you will need:
(1) TIP31A transistor (radio shack/local electronics store $1.50)
(1) RGB LED
(3) 100 Ohm 1/4 watt resistors
A breadboard, wires, and 12v power adapter.
