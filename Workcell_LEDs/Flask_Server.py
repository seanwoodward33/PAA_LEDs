# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:03:32 2019

@author: sean_woodward
"""

#Import libraries
import threading
import queue

#Import libraries for Flask server
from flask import Flask, request
from flask_restful import Resource, Api
#from json import dumps
#from flask.ext.jsonpify import jsonify

#Import Pi_LED_Controller from seperate file
import Pi_LED_Controller as PiCont
import animations

#Setup flask server
app = Flask(__name__)
api = Api(app)

#Define classes for flask
class Rainbow(Resource):
    def get(self):
        #t.start()
        #t.Animation("Rainbow")
        animations.Rainbow(ledStrip, numOfLoops = 10)

class ColourWipe(Resource):
    def get(self):
        #t.start()
        #t.Animation("ColourWipe")
        animations.ColourWipe(ledStrip,(255,0,255))

class Shutdown(Resource):
    def get(self):
        #t.start()
        #t.Animation("Shutdown")
        animations.ColourWipe(ledStrip, (0,0,0), int(1000/len(ledStrip)))
        
        
#Add functions to web address
api.add_resource(Rainbow, '/rainbow')
api.add_resource(ColourWipe, '/colourwipe')
api.add_resource(Shutdown, '/shutdown')

#Define functions for threading
def flaskThread():
    app.run(host = '0.0.0.0', port = '5002')

class animationThread():
    def __init__(self):
        self.Animation(animationNameQ.get())
    
    def Animation(self, input):
        method = getattr(self,input)
        return method()

    def Rainbow(self):
        animations.Rainbow(ledStrip, numOfLoops = 10)
    
    def ColourWipe(self):
        animations.ColourWipe(ledStrip, (0xFF,0x00,0xFF), int(1000/len(ledStrip)))
    
    def Shutdown(self):
        animations.ColourWipe(ledStrip, (0,0,0), int(1000/len(ledStrip)))

#Default run program
if __name__ == '__main__':
    #Set up LED strip
    ledStrip = PiCont.LedSetup()
    
    #Set up queues for passing between threads
    runQ = queue.Queue()
    animationNameQ = queue.Queue()
    animationArgsQ = queue.Queue()

    #Start Flask thread
    threading.Thread(target = flaskThread).start()

    #Set up default run
    animationNameQ.put("Rainbow")
    
    #Start animation thread
    t = threading.Thread(target = animationThread)
    t.start()