# hb_bme680 - Indoor Air Sensor Streaming

### Project Summary
* Made some sort of zombie code that is a combination of 2 examples from the pimoroni examples code for the bme680.
* Streaming data to a power bi interface for easy viewing outside of home network

## What is the BME680?
The BME680 is a sensor from Bosch Sensortec that measures temperature, pressue, relative humidity, and VOCs (Volitile Organic Compounds). Combined with the realtive humidity reading, the VOC measurement will give an air quality in a percentage (high the better). 

It's an awesome, tiny, little sensor, and on the PCB it's footprint still isn't that big! 

## The Process
	
1. Wire the sensor to the raspberry pi following [this](https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/arduino-wiring-test) tutorial. 

2. Install the BME680 python library following the instrucitons in their [github repo](https://github.com/pimoroni/bme680). 

6. Enable i2c in the Raspberry Pi by going to raspberry-pi config and enabling it. 

7. Combine code from the "indoor-air-quality.py" and the "read-all.py" examples from pimoroni, and then add an HTTP post request to a Microsoft Power Bi dataset following [this](https://powerbi.microsoft.com/en-us/blog/using-power-bi-real-time-dashboards-to-display-iot-sensor-data-a-step-by-step-tutorial/) tutorial. 

If you're going to use this code, make sure you use your own specific power bi REST API url at the beginning. 



To use this code: 

``` git clone https://github.com/cloolis/hb_bme680 ``` 


#### Next Steps: 
* Adding smtp to send an email if any of the parameters get out of hand
* Design/Build a case for it.
	* Maybe add some LEDs to the mix for air quality
	* Maybe add an LCD display for quick view
* To either run off battery or house power.
* Run Script on boot (pretty easy I bet)
* maybe make a stand alone andorid app that views graphical data and pushes notifications for out of bounds parameters
