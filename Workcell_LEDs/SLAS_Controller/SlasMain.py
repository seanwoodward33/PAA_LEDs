# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:39:07 2019

@author: Sean_Woodward

Main.py - Program to run to control whole system
"""

#Import libraries
import threading
import queue
import time
import logging
import board
import neopixel
import numpy as np

#Import other code
import SlasAnimations

#Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(asctime)s - (%(threadName)-10s) %(message)s')

#Define workcell class
class Workcell():
    def __init__(self):
        pass
    
    def LedSetup(self, ledGpioPin, ledCount, ledBrightness, ledOrder = neopixel.GRB):
        self.ledPin = ledGpioPin
        self.ledCount = ledCount
        self.ledBrightness = ledBrightness
        self.ledOrder = ledOrder
        self.ledArray = np.zeros((ledCount,4))
        self.ledArray = 1.0
        self.animationRun = True
        self.newRun = True
    
    def LedInitialise(self):
        self.ledStrip = neopixel.NeoPixel(self.ledPin, self.ledCount, brightness = self.ledBrightness, pixel_order=self.ledOrder, auto_write=False)
    
    def LedSections(self, sections = [[0,98]]):
        self.ledSections = sections
    
    def LedSectionAnimations(self, animations = ["RunComplete"]): #default runcomplete rainbow used
        self.ledSectionAnimations = animations
    
    def AnimationCall(self, input, section):
            method = getattr(self,input)
            return method(section)
    
    def PrintLedSections(self):
        print (self.ledSections)
    
    def UpdateBySection(self):
        for i in len(self.ledSections):
            section = self.ledSections[i]
            self.AnimationCall(self.ledSectionAnimations[i],section)
        if self.newRun == True:
            self.newRun = False
    
    def OutputLeds(self):
        for i in range(len(self.ledCount)):
            self.ledStrip[i] = np.rint(self.ledArray[i,0:3]*self.ledArray[i,3]).dtype(int)
        self.ledStrip.show()        
    
    def RunComplete(self, section):
        SlasAnimations.RunComplete(self, section)



if __name__ == '__main__':
    logging.debug("Main SLAS control program running")
    
    logging.debug("Create SLAS workcell object")
    SLAS = Workcell()
    
    logging.debug("Create SLAS Workcell object")
    SLAS.LedSetup(board.D18, 98, 0.2)
    
    logging.debug("Initialise LEDs")
    SLAS.LedInitialise()
    
    logging.debug("Setting up LED sections")
    SLAS.LedSections([[0,50],[51,98]])
    
    logging.debug("Setting animation for each section")
    SLAS.LedSectionAnimations(["RunComplete", "TeachMode"])
    
    logging.debug("Printing LED sections")
    SLAS.PrintLedSections()
    
    logging.debug("Testing RunComplete animation")
    SLAS.RunComplete(SLAS.ledSections[0])