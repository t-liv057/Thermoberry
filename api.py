#!/usr/bin/python
'''
    Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Relay Board Mapping Ch1 fan(GPIO: 25), Ch2 cool(GPIO: 28), ch3 heat(GPIO: 29)
controls = {"fan": 26, "cool": 20, "heat": 21}

#initialize GPIO status variables
fan_status = 0
cool_status = 0
heat_status = 0

# Define led pins as output
for value in controls.values():
    GPIO.setup(value, GPIO.OUT)   

# turn leds OFF 
#GPIO.output(ledRed, GPIO.LOW)
#GPIO.output(ledYlw, GPIO.LOW)
#GPIO.output(ledGrn, GPIO.LOW)
    
@app.route("/")
def index():
    # Read Sensors Status
    fan_status = GPIO.input(controls["fan"])
    cool_status = GPIO.input(controls["cool"])
    heat_status = GPIO.input(controls["heat"])

    templateData = {
              'title' : 'GPIO output Status!',
              'fan'   : fan_status,
              'cool'  : cool_status,
              'heat'  : heat_status,
        }
    return render_template('index.html', **templateData)
    
@app.route("/<mode>/<action>")
def action(mode, action):

    if mode in controls.keys():
        control = controls[mode]
    else:
        return False
    if action == "on":
        GPIO.output(control, True)
    if action == "off":
        GPIO.output(control, False)
             
    fan_status = GPIO.input(controls["fan"])
    cool_status = GPIO.input(controls["cool"])
    heat_status = GPIO.input(controls["heat"])
   
    templateData = {
              'title' : 'GPIO output Status!',
              'fan'   : fan_status,
              'cool'  : cool_status,
              'heat'  : heat_status,
        }
    return render_template('index.html', **templateData)

@app.route("/status")
def status():
             
    fan_status = GPIO.input(controls["fan"])
    cool_status = GPIO.input(controls["cool"])
    heat_status = GPIO.input(controls["heat"])
   
    templateData = {
              'title' : 'GPIO output Status!',
              'fan'   : fan_status,
              'cool'  : cool_status,
              'heat'  : heat_status,
        }
    return render_template('index.html', **templateData)
if __name__ == "__main__":
   #app.run(host='192.168.1.69', port=80, debug=True)
   app.run(host='192.168.1.69', port=80, debug=True)