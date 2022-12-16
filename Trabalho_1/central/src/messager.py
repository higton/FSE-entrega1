import curses
from datetime import datetime
from datetime import date
import time

from menu import Menu
from utils import append_log_file
from control import can_turn_on_alarm_building

class Messager:
    def __init__(self):
        self.state = 0
        self.connections = []
        self.choosen_connection = 0
        self.total = 0
        self.keys = {
            "1": 49,
            "2": 50,
            "3": 51,
            "4": 52,
            "5": 53,
            "6": 54, 
        }
        self.choosen_dist_server = None
        self.isAlarmActive = 0
        self.setBuzzer = 0

    def collect_input(self, stdscr):
        stdscr.nodelay(True)
        Menu.render_menu_input(stdscr, self.connections, self.state)
        
        while True:
            key_pressed = stdscr.getch()
            if key_pressed != -1:
                self.handle_input(key_pressed, stdscr)
            time.sleep(1)

    def handle_input(self, key: int, stdscr):
        if key == curses.KEY_BACKSPACE:
            self.state = 0
            Menu.render_menu_input(stdscr, self.connections, self.state)
        elif self.state == 0:
            map_input_choice = {
                self.keys["1"]: 0,
                self.keys["2"]: 1,
                self.keys["3"]: 2,
                self.keys["4"]: 3,
                self.keys["5"]: 4,
                self.keys["6"]: 5,
            }
            
            if key not in map_input_choice: return

            self.choosen_connection = map_input_choice[key]
            self.state = 1
            Menu.render_menu_input(stdscr, self.connections, self.state)
            self.choosen_dist_server = self.connections[self.choosen_connection]["dist_server"]
            Menu.render_menu_information(stdscr, self.choosen_dist_server, self)
        elif self.state == 1:
            dist_server = self.connections[self.choosen_connection]["dist_server"]
            map_input_message = {
                self.keys["1"]: '{"data":"light1"}',
                self.keys["2"]: '{"data":"light2"}',
                self.keys["3"]: '{"data":"air-conditioning"}',
                self.keys["4"]: '{"data":"projector"}',
                self.keys["5"]: '{"data":"alarm"}',
            }
            map_input_log = {
                self.keys["1"]: "luz 1",
                self.keys["2"]: "luz 2",
                self.keys["3"]: "air-condicionado",
                self.keys["4"]: "projetor",
                self.keys["5"]: "alarme",
            }

            if not key in map_input_message or not key in map_input_log: return

            append_log_file(f"usuário pediu para acionar/desligar '{map_input_log[key]}'. [date: {date.today()}, time: {datetime.now().time()}]")
            
            # if any system that activates the alarm is on, we should not turn the system alarm on
            if map_input_log[key] == "alarme" and not can_turn_on_alarm_building(self.connections) and not self.isAlarmActive:
                return

            conn = self.connections[self.choosen_connection]["conn"]
            dist_server = self.connections[self.choosen_connection]["dist_server"]

            if map_input_log[key] == "alarme":
                self.isAlarmActive = not self.isAlarmActive

                if not self.isAlarmActive: self.turn_off_all_alarms()
                Menu.render_menu_information(stdscr, dist_server, self)
                return

            message = map_input_message[key]
            conn.send(f"{message}".encode("utf-8"))
            
            Menu.render_menu_input(stdscr, self.connections, self.state)
            Menu.render_menu_information(stdscr, dist_server, self)
            
    def send_alarm_to_all_floors(self):
        message = '{"data":"alarm"}'

        for connection in self.connections:
            connection["conn"].send(f"{message}".encode("utf-8"))

    def send_turn_on_all_lights_room(self, conn):
        message = '{"data":"light-all"}'

        conn.send(f"{message}".encode("utf-8"))

    def turn_off_all_alarms(self):
        message = '{"data":"alarm-off"}'

        for connection in self.connections:
            connection["conn"].send(f"{message}".encode("utf-8"))
