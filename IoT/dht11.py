import Adafruit_DHT

def read_dht11_data():
    DHT_sensor = Adafruit_DHT.DHT11
    DHT_PIN = 23
    humidity, temperature = Adafruit_DHT.read(DHT_sensor, DHT_PIN)
    if humidity is not None and temperature is not None:
        return humidity, temperature
    else:
        return None, None
humidity, temperature = read_dht11_data()
#print("Temperature: {:.1f}°C".format(temperature), "Humidity: {:.1f}%".format(humidity))

# Display the values
if humidity is not None and temperature is not None:
    print("Temperature: {:.1f}°C".format(temperature))
    print("Humidity: {:.1f}%".format(humidity))
else:
    humidity = 0
    temperature = 0
    print("Temperature: {:.1f}°C".format(temperature))
    print("Humidity: {:.1f}%".format(humidity))