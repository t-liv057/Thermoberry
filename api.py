#!/usr/bin/python
'''
    Raspberry Pi GPIO Server
     Status and Control
    Author: Taylor Livingston(t-liv057 GIT)
'''

import RPi.GPIO as GPIO
import os
from flask import Flask, flash, redirect, render_template, request, session, abort
import sys
import Adafruit_DHT
from subprocess import Popen


app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Schedule Status
scheduleon = False

# Relay Board Mapping Ch1 fan(GPIO: 25), Ch2 cool(GPIO: 28), ch3 heat(GPIO: 29)
controls = {"fan": 26, "cool": 20, "heat": 21}

# Sensor Mapping
sensor = Adafruit_DHT.AM2302
sensor_pin = 4

# initialize GPIO status variables
fan_status = 0
cool_status = 0
heat_status = 0

# Define led pins as output
for value in controls.values():
    GPIO.setup(value, GPIO.OUT)
    GPIO.output(value, GPIO.HIGH)

# turn leds OFF 
# GPIO.output(ledRed, GPIO.LOW)
# GPIO.output(ledYlw, GPIO.LOW)
# GPIO.output(ledGrn, GPIO.LOW)

# This is the endpoint which allows a user to login
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return home()
    else:
        flash('wrong password!')
        return home()

# This endpoint presents the user with a login option
@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # Read Relay Status
        fan_status = "ON" if GPIO.input(controls["fan"]) == 0 else "OFF"
        cool_status = "ON" if GPIO.input(controls["cool"]) == 0 else "OFF"
        heat_status = "ON" if GPIO.input(controls["heat"]) == 0 else "OFF"
        
        # Read sensor and unit convert
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
        temp_f = round((temperature*1.8) + 32.0,2)
        humidity = round(float(humidity),2)
        temperature = round(float(temperature),2)
        
        # Update template data
        templateData = {'title' : 'GPIO output Status!',
                        'fan'   : fan_status,
                        'cool'  : cool_status,
                        'heat'  : heat_status,
                        'humidity' : humidity,
                        'temperature' : temperature,
                        'tempf' : temp_f,
                        'schedule_status' : scheduleon

            }
        return render_template('index.html', **templateData)
# This dynamic endpoint allows a user to perform actions on the relay board via GPIO pins    
@app.route("/<mode>/<action>")
def action(mode, action):
    # ensure login
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if mode in controls.keys():
            control = controls[mode]
        else:
            return False
        if action == "on":
            GPIO.output(control, GPIO.LOW)
        if action == "off":
            GPIO.output(control, GPIO.HIGH)

        # When an action is performed, cease other relays
        for cont in controls.keys():
            if controls[cont] != control:
               GPIO.output(controls[cont], GPIO.HIGH)
        
        # Read Relay Status
        fan_status = "ON" if GPIO.input(controls["fan"]) == 0 else "OFF"
        cool_status = "ON" if GPIO.input(controls["cool"]) == 0 else "OFF"
        heat_status = "ON" if GPIO.input(controls["heat"]) == 0 else "OFF"
        
        # Read sensor and unit convert
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
        temp_f = round((temperature*1.8) + 32.0,2)
        humidity = round(float(humidity),2)
        temperature = round(float(temperature),2)

        # Update template data
        templateData = {'title' : 'GPIO output Status!',
                        'fan'   : fan_status,
                        'cool'  : cool_status,
                        'heat'  : heat_status,
                        'humidity' : humidity,
                        'temperature' : temperature,
                        'tempf' : temp_f,
                        'schedule_status' : scheduleon
                        

            }
    return render_template('index.html', **templateData)

# This endpoint allows the page to be refreshed with new data
@app.route("/status")
def status():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:             
        fan_status = "ON" if GPIO.input(controls["fan"]) == 0 else "OFF"
        cool_status = "ON" if GPIO.input(controls["cool"]) == 0 else "OFF"
        heat_status = "ON" if GPIO.input(controls["heat"]) == 0 else "OFF"
        
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
        temp_f = round((temperature*1.8) + 32.0,2)
        humidity = round(float(humidity),2)
        temperature = round(float(temperature),2)
        
        templateData = {'title' : 'GPIO output Status!',
                        'fan'   : fan_status,
                        'cool'  : cool_status,
                        'heat'  : heat_status,
                        'humidity' : humidity,
                        'temperature' : temperature,
                        'tempf' : temp_f,
                        'schedule_status' : scheduleon
            }
    return render_template('index.html', **templateData)

# This endpoint allows the user to run a subprocess which is the schedule, it also allows for a os call to kill any schedules that may or may not be running
@app.route("/schedule/<action>")
def schedule(action):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if action == "on":
            # kill any shceduler or schedule that is running before starting a new process
            os.system('kill $(pgrep -f \"schedule.sh\")')
            os.system('kill $(pgrep -f \"scheduler.py\")')
            Popen('/home/pi/project/Thermoberry/schedule.sh',shell=True)
            scheduleon = True
        elif action == "off":
            # kill any scheduler or schedule if it exists
            os.system('kill $(pgrep -f \"schedule.sh\")')
            os.system('kill $(pgrep -f \"scheduler.py\")')
            scheduleon = False
        
        fan_status = "ON" if GPIO.input(controls["fan"]) == 0 else "OFF"
        cool_status = "ON" if GPIO.input(controls["cool"]) == 0 else "OFF"
        heat_status = "ON" if GPIO.input(controls["heat"]) == 0 else "OFF"
            
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
        temp_f = round((temperature*1.8) + 32.0,2)
        humidity = round(float(humidity),2)
        temperature = round(float(temperature),2)
        
        templateData = {'title' : 'GPIO output Status!',
                        'fan'   : fan_status,
                        'cool'  : cool_status,
                        'heat'  : heat_status,
                        'humidity' : humidity,
                        'temperature' : temperature,
                        'tempf' : temp_f,
                        'schedule_status' : scheduleon

            }
    return render_template('index.html', **templateData)

# Run locally on 8080, an outside tunnel directs trafic to this port.
if __name__ == "__main__":
   app.secret_key = os.urandom(12)
   app.run(host='localhost', port=8080, debug=True)