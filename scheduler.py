'''
    Author: Taylor Livingston(t-liv057 GIT)
'''
import schedule
import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import datetime as dt

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Relay Board Mapping Ch1 fan(GPIO: 26), Ch2 cool(GPIO: 20), ch3 heat(GPIO: 21)
controls = {"fan": 26, "cool": 20, "heat": 21}
control_mode = "COOL" # "HEAT"

# Sensor Mapping
sensor = Adafruit_DHT.AM2302
sensor_pin = 4

# Initialize relays
for value in controls.values():
    GPIO.setup(value, GPIO.OUT)
    GPIO.output(value, GPIO.HIGH)

# Fairly basic temperature schedule, to alter the schedule change values here.
# 0 is Monday, 6 is Sunday
temp_sched = {0 : {0:68,1:68,2:68,3:68,4:68,5:68,6:68,7:68,8:68,9:67,10:67,11:67,12:67,13:67,14:67,15:67,16:67,17:67,18:69,19:69,20:69,21:67,22:67,23:67,24:67}
            ,1 : {0:67,1:67,2:67,3:67,4:67,5:67,6:67,7:67,8:68,9:67,10:67,11:67,12:67,13:67,14:67,15:67,16:67,17:67,18:69,19:69,20:69,21:67,22:67,23:67,24:67}
            ,2 : {0:67,1:67,2:67,3:67,4:67,5:67,6:67,7:67,8:68,9:67,10:67,11:67,12:67,13:67,14:67,15:67,16:67,17:67,18:69,19:69,20:69,21:67,22:67,23:67,24:67}
            ,3 : {0:67,1:67,2:67,3:67,4:67,5:67,6:67,7:67,8:68,9:67,10:67,11:67,12:67,13:67,14:67,15:67,16:67,17:67,18:69,19:69,20:69,21:67,22:67,23:67,24:67}
            ,4 : {0:67,1:67,2:67,3:67,4:67,5:67,6:67,7:67,8:68,9:67,10:67,11:67,12:67,13:67,14:67,15:67,16:67,17:67,18:69,19:69,20:69,21:67,22:67,23:67,24:67}
            ,5 : {0:67,1:67,2:67,3:67,4:67,5:67,6:67,7:67,8:67,9:67,10:67,11:69,12:69,13:69,14:67,15:67,16:67,17:67,18:67,19:70,20:70,21:70,22:68,23:68,24:68}
            ,6 : {0:67,1:67,2:67,3:67,4:67,5:67,6:67,7:67,8:67,9:67,10:67,11:69,12:69,13:69,14:67,15:67,16:67,17:67,18:67,19:70,20:70,21:70,22:68,23:68,24:68}
}
# Shout out Warren G
# This is the method called by the schedule module.  It handles GPIO contol depending on it's return from the call to regulate.
def regulators(mode):
    print('inside')
    # Current Date
    todays_date = dt.datetime.today()
    weekday_int = todays_date.weekday()
    current_hour = dt.datetime.now().hour
    print(current_hour)
    sched = temp_sched[weekday_int]
    # print(sched, '\n', current_hour, ' ' ,sched[current_hour])
    
    # Same sensor read from api.py, unit conversion as well
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
    temp_f = round((temperature*1.8) + 32.0,2)
    humidity = round(float(humidity),2)
    temperature = round(float(temperature),2)
    
    # Here we grab what the desired temperature is and calculate how far away from it we are.
    target = float(sched[current_hour])
    temp_diff = target-temperature
    diff_mag = temp_diff/target
    decision = regulate(mode, diff_mag)
    print(decision)
    if decision:
        GPIO.output(decision, GPIO.LOW)

        # When relay activates, deactivate other relays
        for cont in controls.keys():
            if controls[cont] != decision:
               GPIO.output(controls[cont], GPIO.HIGH)
    else:
        # If no decision, all relays should be deactivated
        for cont in controls.keys():
               GPIO.output(controls[cont], GPIO.HIGH)

# Regulate returns an action based off the temperature schedule and control mode.  It is called whenever Regulators is called.
def regulate(mode, delta):
    # A gradient threshold of 4% is used to decide if an action should be performed.  If the gradient is outside the range 
    # In the direction of control mode the appropriate action is returned.  
    # Fans are turned on when an excess amount of heat or cold are present in the home.  This is the reverse of the 4% threshold.
    # 4% is an arbitrary threshold which turns out to be 2-4 degress in most of the temperature range of the midwest
    if mode == "COOL":
        if delta <= -(.04):
            # turn on cooling
            return controls['cool']
        elif delta >= .04:
            # turn on fan
            return controls['fan']
        else:
            return None
    
    elif mode == "HEAT":
        if delta <= -(.04):
            # turn on fan
            return controls['fan']
        elif delta >= .04:
            # turn on heating
            return controls['heat']
        else:
            return None
    else:
        print("No mode set in file")

# Every 1 minute run regulators and check for a new action, if the action is redundant then no issue.  Logic in Regulators prevents two actions from occuring simultaneously.
schedule.every(1).minutes.do(regulators, mode=control_mode)
while(True):
    schedule.run_pending()
    time.sleep(1)




