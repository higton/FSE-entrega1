import json
import socket
from datetime import datetime
from datetime import date

from dist_server import DistServer
from menu import Menu
from utils import define_on_off, define_open_closed, append_log_file, define_detected
from messager import Messager
from control import can_turn_on_alarm

class Router:
    def __init__(self, request: dict, stdscr, conn: socket, addr):
        self.request = request
        self.stdscr = stdscr
        self.conn = conn
        self.addr = addr
        self.dist_server = None

    def createNewDistServer(self) -> DistServer:
        distServer = DistServer()

        distServer.nome = self.request["nome"]

        self.dist_server = distServer

        return distServer

    def data(self, distServer: DistServer, messager: Messager, connections: list):
        while(True):
            request_json = self.conn.recv(1024).decode('utf-8')

            request = json.loads(request_json)
            data = request["data"]
            type = data["type"]

            if type == "temperature":
                distServer.temperatura = data["degree"]
                distServer.umidade = data["humidity"]
            elif type == "alarm":
                distServer.alarme = data["value"]
                append_log_file(f"O alarme foi {define_on_off(distServer.alarme)}. [date: {date.today()}, time: {datetime.now().time()}]")
            elif type == "people":
                distServer.quantidade_de_pessoas += data["value"]
                messager.total += data["value"]
            elif type == "window":
                number = data["number"]
                distServer.janelas[number] = data["value"]
                append_log_file(f"A janela foi '{define_open_closed(distServer.janelas[number])}'. [date: {date.today()}, time: {datetime.now().time()}]")
            elif type == "light":
                number = data["number"]
                distServer.lampadas[number] = data["value"]
                append_log_file(f"A lampada foi '{define_on_off(distServer.lampadas[number])}'. [date: {date.today()}, time: {datetime.now().time()}]")
            elif type == "door":
                distServer.porta = data["value"]
                append_log_file(f"A porta foi '{define_open_closed(distServer.porta)}'. [date: {date.today()}, time: {datetime.now().time()}]")
            elif type == "smoke":
                distServer.fumaca = data["value"]
                append_log_file(f"A fumaça foi '{define_detected(distServer.fumaca)}'. [date: {date.today()}, time: {datetime.now().time()}]")
            elif type == "presence":
                distServer.presence = data["value"]
                append_log_file(f"A presença foi '{define_detected(distServer.presence)}'. [date: {date.today()}, time: {datetime.now().time()}]")
            elif type == "projector":
                distServer.projector = data["value"]
                append_log_file(f"O projetor foi '{define_on_off(distServer.projector)}'. [date: {date.today()}, time: {datetime.now().time()}]")
            elif type == "air-conditioning":
                distServer.arcondicionado = data["value"]
                append_log_file(f"O ar-condicionado foi '{define_on_off(distServer.arcondicionado)}'. [date: {date.today()}, time: {datetime.now().time()}]")

            if not distServer.alarme and not can_turn_on_alarm(distServer) and messager.isAlarmActive:
                messager.send_alarm_to_all_floors()

            if type == "presence" and not messager.isAlarmActive and distServer.presence:
                messager.send_turn_on_all_lights_room(self.conn)

            if distServer == messager.choosen_dist_server:
                Menu.render_menu_information(self.stdscr, distServer, messager)

    def filterRequest(self, messager: Messager, connections: list):
        type = self.request["type"]
        
        if type == "init":
            distServer = self.createNewDistServer()
            if not messager.choosen_dist_server:
                messager.choosen_dist_server = self.dist_server

            Menu.render_menu_information(self.stdscr, distServer, messager)
            self.data(distServer, messager, connections)