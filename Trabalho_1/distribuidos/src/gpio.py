import time
from gpiozero import MotionSensor, LED, Buzzer
from time import sleep
from signal import pause
import RPi.GPIO as GPIO

from messager import Messager
from counter import Counter

class Gpio:
    def __init__(self, messager: Messager):
        self.gpio_map = {}
        self.messager = messager
        self.map_leds = {}

    def setup(self, json_config: list):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        # outputs
        self.gpio_map["light1"] = int(json_config["outputs"][0]["gpio"])
        self.gpio_map["light2"] = int(json_config["outputs"][1]["gpio"])
        self.gpio_map["air-conditioning"] = int(json_config["outputs"][3]["gpio"])
        # self.gpio_map["sprinkler"] = int(json_config["outputs"][3]["gpio"])
        self.gpio_map["alarm"] = int(json_config["outputs"][4]["gpio"])
        self.gpio_map["projector"] = int(json_config["outputs"][2]["gpio"])

        # inputs
        self.gpio_map["presence"] = int(json_config["inputs"][0]["gpio"])
        self.gpio_map["smoke"] = int(json_config["inputs"][1]["gpio"])
        self.gpio_map["window1"] = int(json_config["inputs"][2]["gpio"])
        # self.gpio_map["window2"] = int(json_config["inputs"][3]["gpio"])
        self.gpio_map["people_counter1"] = int(json_config["inputs"][4]["gpio"])
        self.gpio_map["people_counter2"] = int(json_config["inputs"][5]["gpio"])
        self.gpio_map["door"] = int(json_config["inputs"][3]["gpio"])

        # temperatures
        self.gpio_map["temperature"] = int(json_config["sensor_temperatura"][0]["gpio"])

        self.map_leds["light1"] = LED(self.gpio_map["light1"])
        self.map_leds["light2"] = LED(self.gpio_map["light2"])
        self.map_leds["air-conditioning"] = LED(self.gpio_map["air-conditioning"])
        self.map_leds["projector"] = LED(self.gpio_map["projector"])
        self.map_leds["alarm"] = LED(self.gpio_map["alarm"])

    def switch_pin_value(self, type: str):
        led = self.map_leds[type]

        led.toggle()

        if self.map_leds[type].is_lit:
            self.messager.send_message(type, 1)
        else:
            self.messager.send_message(type, 0)


    def check_signals(self):
        self.check_signals_input()
        pause()

    def check_signals_input(self):
        types = ["window1",  "presence",  "door",  "smoke"]

        for type in types:
            self._check_signal_input(type)

        time.sleep(0.5)
        
        counter = Counter()
        counter.count_people(self.gpio_map, self.messager)

    def _check_signal_input(self, type: str):
        def on_motion(msg):
            self.messager.send_message(type, 1)

        def no_motion(msg):
            self.messager.send_message(type, 0)

        pir = MotionSensor(self.gpio_map[type])
        pir.when_motion = on_motion
        pir.when_no_motion = no_motion

    def turn_all_lights(self):
        leds = [self.map_leds["light1"], self.map_leds["light2"]]

        for led in leds:
            led.on()

        time.sleep(15)

        for led in leds:
            led.off()

    def turn_off_alarm(self):
        led = self.map_leds["alarm"]

        led.off()
        self.messager.send_message("alarm", 0)