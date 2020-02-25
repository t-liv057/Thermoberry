#!/usr/bin/python


import RPi.GPIO as GPIO
import time
#Relay Board Mapping Ch1 fan(GPIO: 25), Ch2 cool(GPIO: 28), ch3 heat(GPIO: 29)
controls = {"fan": 26, "cool": 21, "heat": 20}

GPIO.setmode(GPIO.BCM)
GPIO.setup(controls["fan"], GPIO.OUT)
GPIO.setup(controls["cool"], GPIO.OUT)
GPIO.setup(controls["heat"], GPIO.OUT)


try:
    while True:
        GPIO.output(controls["fan"], True)
        time.sleep(1)
        GPIO.output(controls["fan"], False)
        GPIO.output(controls["cool"], True)
        time.sleep(1)
        GPIO.output(controls["cool"], False)
        GPIO.output(controls["heat"], True)
        time.sleep(1)
        GPIO.output(controls["heat"], False)

finally:
    GPIO.cleanup()