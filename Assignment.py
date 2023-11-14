import network
import time
from umqtt.simple import MQTTClient
from machine import Pin
import dht
import json

SERVER = "mqtt.favoriot.com"
CLIENT_ID = "umqtt_client"
USERNAME = "9UPAuTWQ02F6Yk4bzF0k8V8TkNy0lkzn"
PASSWORD = "9UPAuTWQ02F6Yk4bzF0k8V8TkNy0lkzn"
WIFI_SSID = "MARKAS KOTAK"
WIFI_PASSWORD = "113333555555"

# Temperature and humidity thresholds
TEMP_THRESHOLD_OPTIMUM = 21  # in degrees Celsius
HUM_THRESHOLD_OPTIMUM = 60  # in percentage
TEMP_THRESHOLD_HIGH = 25  # in degrees Celsius
TEMP_THRESHOLD_LOW = 10  # in degrees Celsius
HUM_THRESHOLD_HIGH = 70  # in percentage
HUM_THRESHOLD_LOW = 50  # in percentage

# Connect to MQTT server
client = MQTTClient(CLIENT_ID, SERVER, user=USERNAME, password=PASSWORD)

# WLAN (Wi-Fi) initialization
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()

# Sensor initialization
sensor = dht.DHT11(Pin(14))
data = []

# Connect to Wi-Fi network
if not wlan.isconnected():
    print('Connecting to Wi-Fi network...')
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
    print('Network config:', wlan.ifconfig())

# Connect to MQTT server
client.connect()
print('MQTT client connected')

# Read and capture data five times
for _ in range(100):
    try:
        time.sleep(5)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9/5) + 32.0

        # Print temperature and humidity
        print('Temperature: %3.1f C' % temp)
        print('Humidity: %3.1f %%' % hum)

        # Check temperature and humidity conditions for optimum growth
        if temp == TEMP_THRESHOLD_OPTIMUM:
            print('Optimum Growth (Temperature)')

        if hum == HUM_THRESHOLD_OPTIMUM:
            print('Optimum Growth (Humid)')

        # Check temperature and humidity conditions for negative growth
        if temp > TEMP_THRESHOLD_HIGH:
            print('Negative Growth (Hot)')
        elif temp < TEMP_THRESHOLD_LOW:
            print('Negative Growth (Cold)')

        if hum > HUM_THRESHOLD_HIGH:
            print('Negative Growth (Too Humid)')
        elif hum < HUM_THRESHOLD_LOW:
            print('Negative Growth (Less Humid)')

        # Store data in Python format
        data.append({'temperature': temp, 'humidity': hum})

    except OSError as e:
        print('Failed to read sensor.')

# Display data in Python format
print('Data captured in Python format:')
print(data)

# Convert data to JSON format
json_data = json.dumps(data)

# Display data in JSON format
print('Data captured in JSON format:')
print(json_data)

# Publish data to MQTT topic
topic = '9UPAuTWQ02F6Yk4bzF0k8V8TkNy0lkzn/v2/streams'
payload = {
    'device_developer_id': 'TempandHumiditySensor@S63650',
    'data': {'Temperature': temp}
}
client.publish(topic, json.dumps(payload))

# Disconnect from MQTT server
client.disconnect()
print('MQTT client disconnected')


