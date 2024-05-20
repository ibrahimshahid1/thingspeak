import time
import Adafruit_DHT
import Adafruit_BMP.BMP280 as BMP280
import requests
import serial

# ThingSpeak settings
THINGSPEAK_API_KEY = '84GV346GE1BNUND9'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Serial settings for Arduino
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_RATE = 9600
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)

# DHT22 settings
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin connected to DHT22 data pin

# BMP280 settings
bmp280 = BMP280.BMP280()

def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        return None, None

def read_bmp280():
    pressure = bmp280.read_pressure()
    if pressure is not None:
        return pressure / 100.0  # Convert to hPa
    else:
        return None

def read_soil_moisture():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        return int(line)
    return None

def log_to_thingspeak(temperature, humidity, pressure, soil_moisture):
    payload = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': temperature,
        'field2': humidity,
        'field3': pressure,
        'field4': soil_moisture
    }
    response = requests.post(THINGSPEAK_URL, data=payload)
    return response.status_code

while True:
    temperature, humidity = read_dht22()
    pressure = read_bmp280()
    soil_moisture = read_soil_moisture()
    
    if temperature is not None and humidity is not None and pressure is not None and soil_moisture is not None:
        status_code = log_to_thingspeak(temperature, humidity, pressure, soil_moisture)
        if status_code == 200:
            print(f'Successfully logged data: Temp={temperature:.2f}C, Humidity={humidity:.2f}%, Pressure={pressure:.2f}hPa, SoilMoisture={soil_moisture}')
        else:
            print(f'Failed to log data. HTTP status code: {status_code}')
    else:
        print('Failed to read from sensors.')

    time.sleep(20)  # Wait for 20 seconds before the next reading
