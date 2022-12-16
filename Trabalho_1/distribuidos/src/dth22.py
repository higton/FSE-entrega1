import RPi.GPIO as GPIO
import dht11
import time

def analyze_dth22(messager, pin):
    instance = dht11.DHT11(pin = pin)
    result = instance.read()

    while True:
        if result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            messager.send_message_dht22(result.temperature, result.humidity)
        else:
            print("Error: %d" % result.error_code)

        time.sleep(2)
