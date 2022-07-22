import time

import badger2040
import pimoroni_i2c
import breakout_scd41

NUMBER_OF_READINGS = 10
I2C_PINS_BADGER_2040 = {"sda": 4, "scl": 5}
SLEEP_BETWEEN_READINGS = 10

badger = badger2040.Badger2040()

# RP2040 CPU speed
# badger.system_speed(0)

# Screen update speed
# badger.update_speed(2)

badger.pen(0)
badger.text("RP2040", 20, 20)
badger.text("CO2 monitor", 20, 60)
badger.update()

time.sleep(3)

i2c = pimoroni_i2c.PimoroniI2C(**I2C_PINS_BADGER_2040)
breakout_scd41.init(i2c)
breakout_scd41.start()

reading = 0

while reading < NUMBER_OF_READINGS:
	badger.led(100)
	if breakout_scd41.ready():
		co2, temperature, humidity = breakout_scd41.measure()
		message = "{co2:.0f}ppm, {temperature:.1f}°C, {humidity:.1f}%"
		co2Message = "{co2:.0f}ppm CO2"
		temperatureMessage = "{temperature:.1f}°C"
		humidityMessage = "{humidity:.1f}%"
		readingMessage = "Reading {reading:.0f}"
		print(message.format(co2 = co2, temperature = temperature, humidity = humidity))
		badger.pen(15)
		badger.clear()
		badger.pen(0)
		badger.text(co2Message.format(co2 = co2), 20, 20)
		badger.text(temperatureMessage.format(temperature = temperature), 20, 60)
		badger.text(humidityMessage.format(humidity = humidity), 20, 100)
		badger.text(readingMessage.format(reading = reading + 1), 200, 100, 0.5)
		badger.update()
		reading += 1
		time.sleep(SLEEP_BETWEEN_READINGS)

badger.led(0)
badger.halt()
