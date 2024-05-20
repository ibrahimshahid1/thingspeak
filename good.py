import time
import board
import busio
import adafruit_dht
import adafruit_bmp280
import requests

# ThingSpeak settings
THINGSPEAK_API_KEY = '84GV346GE1BNUND9'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# DHT22 settings
dht_device = adafruit_dht.DHT22(board.D4)

# BMP280 settings
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

def read_dht22():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if humidity is not None and temperature is not None:
            return temperature, humidity
    except RuntimeError as error:
        print(f"Reading DHT22 failed: {error.args[0]}")
        return None, None

def read_bmp280():
    try:
        pressure = bmp280.pressure
        if pressure is not None:
            return pressure  # Pressure is already in hPa
    except Exception as error:
        print(f"Reading BMP280 failed: {error}")
        return None

def log_to_thingspeak(temperature, humidity, pressure):
    payload = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': temperature,
        'field2': humidity,
        'field3': pressure
    }
    response = requests.post(THINGSPEAK_URL, data=payload)
    return response.status_code

while True:
    temperature, humidity = read_dht22()
    pressure = read_bmp280()
    
    if temperature is not None and humidity is not None and pressure is not None:
        status_code = log_to_thingspeak(temperature, humidity, pressure)
        if status_code == 200:
            print(f'Successfully logged data: Temp={temperature:.2f}C, Humidity={humidity:.2f}%, Pressure={pressure:.2f}hPa')
        else:
            print(f'Failed to log data. HTTP status code: {status_code}')
    else:
        print('Failed to read from sensors.')

    time.sleep(20)  # Wait for 20 seconds before the next reading
