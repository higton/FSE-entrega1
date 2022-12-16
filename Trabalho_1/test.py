import time
from gpiozero import MotionSensor
from signal import pause

class Counter:
    def __init__(self):
        self.total = 0

    def count_people(self):
        def add_person(msg):
            self.total += 1
            print(self.total)

        def remove_person(msg):
            self.total -= 1
            print(self.total)

        pir_enter = MotionSensor(20)
        pir_exit = MotionSensor(21)
        pir_enter.when_motion = add_person
        pir_exit.when_no_motion = remove_person
        time.sleep(0.1)
        pause()

test = Counter()
test.count_people()