import time
from gpiozero import MotionSensor
from signal import pause

class Counter:
    def __init__(self):
        self.total = 0

    def count_people(self, gpio_map, messager):
        pin_enter = gpio_map["people_counter1"]
        pin_exit = gpio_map["people_counter2"]

        def add_person(msg):
            self.total += 1
            print(self.total)
            messager.send_message("people_counter1", 1)

        def remove_person(msg):
            self.total -= 1
            print(self.total)
            messager.send_message("people_counter2", -1)

        pir_enter = MotionSensor(pin_enter)
        pir_exit = MotionSensor(pin_exit)
        pir_enter.when_motion = add_person
        pir_exit.when_no_motion = remove_person
        time.sleep(0.1)
        pause()