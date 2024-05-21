import adafruit_dht
import board

dht_device = adafruit_dht.DHT22(board.D4)

try:
    temperature = dht_device.temperature
    humidity = dht_device.humidity
    print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
except RuntimeError as error:
    print("Error reading from DHT22:", error)
