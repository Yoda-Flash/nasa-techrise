import adafruit_bme680
import board

i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

print(f'Temperature: {sensor.temperature} degrees C')
print(f'Gas: {sensor.gas} ohms')
print(f'Humidity: {sensor.humidity}')
print(f'Pressure: {sensor.pressure}hPa')