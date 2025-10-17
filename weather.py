import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "wokwi-weather"

sensor = dht.DHT22(Pin(15))

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    time.sleep(0.1)

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

prev_weather = ""

# MODIFICACIÓN:contador de publicaciones
contador = 0

while True:
    sensor.measure()
    message = ujson.dumps({
        "temp": sensor.temperature(),
        "humidity": sensor.humidity(),
    })
    if message != prev_weather:
        client.publish(MQTT_TOPIC, message)
        prev_weather = message

        #MODIFICACIÓN:imprimir contador
        contador += 1
        print("Publicado:", contador)
    time.sleep(1)
