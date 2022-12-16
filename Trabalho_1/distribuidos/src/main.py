
import socket
import json
import sys
import threading
import time

from read_config import json_config_parse
from gpio import Gpio
from messager import Messager
from dth22 import analyze_dth22

def handle_connection(server, gpio: Gpio):
    while(True):
        msg = server.recv(1024).decode("utf-8")
        if not msg: 
            print("no response from central")
            break

        msg = json.loads(msg)

        print("message from central: ", msg)
        data = msg["data"]
        
        if data == "light-all":
            gpio.turn_all_lights()
            continue

        if data == "alarm-off":
            gpio.turn_off_alarm()
            continue

        gpio.switch_pin_value(data)
        

def connect_with_central(s, ip: str, port: int):
    while True:
        try:
            s.connect((ip, port))
            break
        except socket.error:
            print("Connection Failed, Retrying...")
            time.sleep(2)

def start(path: str):
    json_config = json_config_parse(path)

    CENTRAL_PORT = json_config["porta_servidor_central"]
    CENTRAL_IP = json_config["ip_servidor_central"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect with central's socket
    connect_with_central(s, CENTRAL_IP, CENTRAL_PORT)
    # s.connect((CENTRAL_IP, CENTRAL_PORT))

    test = open(path)
    print("test: ", test)
    # just send the configuration json to the central service
    json_config["type"] = "init"

    data = json.dumps(json_config)
    s.sendall(bytes(data,encoding="utf-8"))

    messager = Messager(s)
    gpio = Gpio(messager)
    
    gpio.setup(json_config)
    thread = threading.Thread(target=gpio.check_signals)
    thread.start()

    thread = threading.Thread(target=analyze_dth22, args=(messager,gpio.gpio_map["temperature"]))
    thread.start()

    thread = threading.Thread(target=handle_connection, args=(s, gpio))
    thread.start()

if __name__ == "__main__":
    if len(sys.argv) < 2: print("Você precisa passar o path do arquivo de configuração JSON")
    print(sys.argv)

    start(sys.argv[1])