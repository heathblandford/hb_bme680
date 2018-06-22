# okay so
# here's the deal
# this thing sloppy code is put together from 2 examples from 
# the pimoroni BME680 example code and pimoroni's python lib for this


import urllib, urllib2, time
import bme680

REST_API_URL = ' *** power bi rest api url here *** '

print("""Estimate indoor air quality
Runs the sensor for a burn-in period, then uses a 
combination of relative humidity and gas resistance
to estimate indoor air quality as a percentage.
Press Ctrl+C to exit
""")

sensor = bme680.BME680(i2c_addr=0x77)

# These oversampling settings can be tweaked to 
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# start_time and curr_time ensure that the 
# burn_in_time (in seconds) is kept track of.

start_time = time.time()
curr_time = time.time()

# change this based on how long you want the gas sensor burn in time to be (duh)
burn_in_time = 300

burn_in_data = []

try:
    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.
    print("Collecting gas resistance burn-in data for an indeterminate amount of time\n")
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            burn_in_data.append(gas)
            print("Gas: {0} Ohms".format(gas))
            time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0

    # Set the humidity baseline to 40%, an optimal indoor humidity.
    hum_baseline = 40.0

    # This sets the balance between humidity and gas reading in the
    # calculation of air_quality_score (25:75, humidity:gas)
    hum_weighting = 0.25

    print("Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n".format(
        gas_baseline, hum_baseline))

    while True:
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            gas = sensor.data.gas_resistance
            gas_offset = gas_baseline - gas

            hum = sensor.data.humidity
            hum_offset = hum - hum_baseline

            # Calculate hum_score as the distance from the hum_baseline.
            if hum_offset > 0:
                hum_score = (100 - hum_baseline - hum_offset) / \
                    (100 - hum_baseline) * (hum_weighting * 100)

            else:
                hum_score = (hum_baseline + hum_offset) / \
                    hum_baseline * (hum_weighting * 100)

            # Calculate gas_score as the distance from the gas_baseline.
            if gas_offset > 0:
                gas_score = (gas / gas_baseline) * \
                    (100 - (hum_weighting * 100))

            else:
                gas_score = 100 - (hum_weighting * 100)

            # Calculate air_quality_score.
            air_quality_score = hum_score + gas_score
            
            print("{0:.2f} C,{1:.2f} hPa,{2:.3f} %RH, {3:.2f}".format(
                  sensor.data.temperature, sensor.data.pressure, hum, air_quality_score))

            # ensure that timestamp string is formatted properly
            now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")

            # data that we're sending to Power BI REST API
            data = '[{{ "timestamp": "{0}", "temperature": "{1:0.1f}", "humidity": "{2:0.1f}", "pressure": "{2:0.1f}", "airQuality": "{2:0.1f}" }}]'.format(
                now, sensor.data.temperature, hum, sensor.data.pressure, air_quality_score)

            # make http post request to power bi
            req = urllib2.Request(REST_API_URL, data)
            res = urllib2.urlopen(req)

            time.sleep(1)

except KeyboardInterrupt:
    pass
