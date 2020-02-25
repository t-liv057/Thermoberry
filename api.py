#!/usr/bin/python

import flask
from flask import request
import RPi.GPIO as GPIO
import time

#Relay Board Mapping Ch1 fan(GPIO: 25), Ch2 cool(GPIO: 28), ch3 heat(GPIO: 29)
controls = {"fan": 26, "cool": 20, "heat": 21}



app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Bullshit Relay Site</h1><p>This site is complete bullshit</p>"

@app.route('/fan', methods=['GET'])
def fan():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(controls["fan"], GPIO.OUT)
        GPIO.output(controls["fan"], True)
        time.sleep(3)
        GPIO.output(controls["fan"], False)

        return "<h1>Switching Fan Relay On</h1><p>This site is complete bullshit</p>"
    except Exception as e:
        GPIO.cleanup()
        return(e)

@app.route('/cool', methods=['GET'])
def cool():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(controls["cool"], GPIO.OUT)
        GPIO.output(controls["cool"], True)
        time.sleep(3)
        GPIO.output(controls["cool"], False)
        return "<h1>Switching Cool Relay On</h1><p>This site is complete bullshit</p>"
    except Exception as e:
        GPIO.cleanup()
        return(e)

@app.route('/heat', methods=['GET'])
def heat():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(controls["heat"], GPIO.OUT)
        GPIO.output(controls["heat"], True)
        time.sleep(3)
        GPIO.output(controls["heat"], False)

        return "<h1>Switching Heat Relay On</h1><p>This site is complete bullshit</p>"
    except Exception as e:
        GPIO.cleanup()
        return(e)


app.run(host='0.0.0.0')