# Thermoberry

The Thermoberry is a homade IOT Thermostat.  It's built using a flask app and Raspberry pi 3b, with rpi relay hat mounted to the top.  Most HVAC units in households throughout the US use a fiarly standardized interface for control.  This lack of complexity allows for simle use of the Raspberry pi GPIO pins.  Configuring the relays, which act like a switch, to deliver current to the neccesary channel in an HVAC unit allows someone to make full use of it.
## Getting Started

This build is meant for my personal Raspberry pi, and a few parts and technical knowledge are required for setup.  Raspberry pi, relay board, and miscellaneous wires are easy to find and assemble for operation, and depending on how a HVAC unit is configured changes the process of integrating the Thermoberry.

### Prerequisites



```
A requirements.txt file is attatched showing some of the neccessary libraries.  Some are redundant for development of the device, and other more common libraries are left out, like the RPI GPIO.
```

### Installing



```
Generally once hardware is properly configred only the required modules and python need to be installed on the device to run the server.  Running this sever in a network where multiple routers are in series requires additional tunneling to be done to make the device accessible to the web.
```



