#!/usr/bin/env python3
#
#Program to control LEDs from Raspberry Pi
#
#Author:	Sean Woodward
#Date:		30/10/2019
#
#For further information on AdaFruits NeoPixel Library, see: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
#Inspirtaion drawn from tutorial, see: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

#Import relevant libraries
import time
import neopixel
import board
import math
import threading
import colorsys

#Define LED strip configuration
def LedSetup(ledPin = board.D18, ledCount = 25, ledOrder = neopixel.GRB):
    ledPin = board.D18						                        #GPIO pin LEDs are connected to Pi
    ledCount = 98							                        #Number of LEDs in strip
    ledOrder = neopixel.GRB                                         #Set to *.GRB or *.RGB depending on how LEDs are wired
    ledStrip = neopixel.NeoPixel(ledPin, ledCount, brightness=0.2, auto_write=False, pixel_order=ledOrder)
    return ledStrip

#Define functions to control LEDs
#Wipe colour across pixel line, one pixel at a time
def ColourWipe(strip, colour, waitTime=10):                     #waitTime is in ms
    for i in range(len(strip)):
        strip[i] = colour
        strip.show()
        time.sleep(waitTime/1000.0)

#Wipe colour across pixel line, one pixel at a time
def ColourWipeTwo(strip, colour, waitTime=20):                  #waitTime is in ms
    for i in range(math.ceil(len(strip)/2)):
        strip[i] = colour
        strip[len(strip)-1-i] = colour
        strip.show()
        time.sleep(waitTime/1000.0)

#Single pixel progression
def SinglePixelWipe(strip, singleColour, backColour = (0,0,0), waitTime=10):
    strip.fill(backColour)
    for i in range(len(strip)):
        if (i > 0):
            strip[i-1] = backColour
        strip[i] = singleColour
        strip.show()
        time.sleep(waitTime/1000.0)

#Single pixel progression with retention
def SinglePixelWipeRetain(strip, singleColour, backColour = (0,0,0), waitTime=0):
    strip.fill(backColour)
    for i in range(len(strip)):
        for j in range(len(strip)-i):
            if (j > 0):
                strip[j-1] = backColour
            strip[j] = singleColour
            strip.show()
            time.sleep(waitTime/1000.0)


#Movie theatre light style chaser animation
def TheatreChase(strip, colour, waitTime=50, iterations=30):    #waitTime is in ms
    for i in range(iterations):
        for j in range(3):
            for k in range(0,len(strip),3):
                if(k+j < len(strip)):
                    strip[k+j] = colour
            strip.show()
            time.sleep(waitTime/1000.0)
            for k in range(0,len(strip),3):
                if(k+j < len(strip)):
                    strip[k+j] = 0

#Non-normalised HSV to RGB function
def HsvToRgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

#Draw a rainbow that fades across all the LEDs at once
def Rainbow(strip, waitTime=10, iterations = 500):
    ledCount = len(strip)
    for i in range(iterations):
        for j in range(len(strip)):
            strip[j] = HsvToRgb((((j+i)%ledCount)/ledCount),1.0,1.0)
        strip.show()

#Knightrider
def Knightrider(strip, waitTime, iterations = 500):
    pass
    


#Emergency Stop, Red lights
def ErrorState(strip):
    strip.fill((255,0,0))
    strip.show()

#Emergency Stop, Red lights
def RunState(strip):
    strip.fill((0,255,0))
    strip.show()

#Main program logic
if __name__ == '__main__':
    #Initialise LED strip
    ledStrip = LedSetup()
    
    #Testing Loop
    try:
        while True:
            #ColourWipe(ledStrip, (255,0,0), 0)
            #ColourWipe(ledStrip, (0,255,0), 0)
            #ColourWipe(ledStrip, (0,0,255), 0)
            #ColourWipeTwo(ledStrip, (0,255,0))
            #TheatreChase(ledStrip, (255,255,255))
            #SinglePixelWipe(ledStrip,(255,0,255))
            Rainbow(ledStrip)
            #SinglePixelWipeRetain(ledStrip,(255,0,255))
            #ErrorState(ledStrip)
            #time.sleep(1)
            #RunState(ledStrip)
            #time.sleep(1)
            ledStrip.fill((2,116,153))
            time.sleep(5)
            ledStrip.fill((53,177,203))
            time.sleep(5)
            ledStrip.fill((230,81,151))
            time.sleep(5)
            ledStrip.fill((151,19,75))
            time.sleep(5)
            #Rainbow(ledStrip,10)
            
    except KeyboardInterrupt:
        ColourWipe(ledStrip, (0,0,0), 10)
