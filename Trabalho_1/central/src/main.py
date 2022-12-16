import socket
import json
import sys
import threading
from time import sleep
import time
from menu import Menu
import curses
from curses import wrapper

from router import Router
from messager import Messager

def start(stdscr):
    PORT_CENTRAL = sys.argv[1]
    IP = sys.argv[2]
    ADDR = (IP, int(PORT_CENTRAL))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(ADDR)

    stdscr.clear()
    stdscr.addstr(0, 0, "Socket created!", curses.A_BOLD)
    stdscr.addstr(1, 0, "Waiting for connection...", curses.A_BOLD)
    stdscr.refresh()

    s.listen()

    messager = Messager()
    while (True):
        conn, addr = s.accept()
        msg = conn.recv(2024).decode('utf-8')
        data = json.loads(msg)
        router = Router(data, stdscr, conn, addr)

        thread = threading.Thread(target=router.filterRequest, args=(messager, messager.connections,))
        thread.start()

        map_connection = {
            "conn": conn,
            "addr": addr,
            "name": router.dist_server.nome,
            "dist_server": router.dist_server
        }
        messager.connections.append(map_connection)

        thread = threading.Thread(target=messager.collect_input, args=(stdscr, ))
        thread.start()

if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print("Faltou passar todos os argumentos. Exemplo: python3 main.py 10422 '127.0.0.1'")
    else:
        wrapper(start)