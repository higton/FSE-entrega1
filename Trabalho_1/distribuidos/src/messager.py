import json

class Messager:
    def __init__(self, s):
        self.s = s

    def send_message_dht22(self, temperature: int, humidity: int):
        message = {
            "type": "data",
            "data": {
                "type": "temperature",
                "degree": temperature,
                "humidity": humidity,
            }
        }
        
        data = json.dumps(message)
        print("data: ", data)
        self.s.sendall(bytes(data,encoding="utf-8"))

    def send_message(self, type: str, value: int):
        message = {
            "type": "data",
            "data": {
                "type": type,
                "value": value,
            }
        }

        if type == "window1":
            message["data"]["type"] = "window"
            message["data"]["number"] = 0
        elif type == "light1":
            message["data"]["type"] = "light"
            message["data"]["number"] = 0
        elif type == "light2":
            message["data"]["type"] = "light"
            message["data"]["number"] = 1
        elif type == "people_counter1":
            message["data"]["type"] = "people"
        elif type == "people_counter2":
            message["data"]["type"] = "people"

        data = json.dumps(message)
        print("message to central: ", data)
        self.s.sendall(bytes(data,encoding="utf-8"))
