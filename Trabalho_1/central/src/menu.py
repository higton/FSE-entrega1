import curses

from dist_server import DistServer
from utils import define_on_off, define_open_closed, define_detected

class Menu:
    @staticmethod
    def clear_menu_information(stdscr, start: int, end: int):
        for i in range(start, end):
            stdscr.addstr(i,0, f"                                                   ")

    @staticmethod
    def render_menu_information(stdscr, distServer: DistServer, messager) -> None:
        Menu.clear_menu_information(stdscr, 6, 25)
        stdscr.addstr(6,0, f"ANDAR: {distServer.nome}", curses.A_BOLD)

        stdscr.addstr(8,0, f"Sistema de Alarme: {define_on_off(messager.isAlarmActive)}")
        stdscr.addstr(9,0, f"Buzzer alarme: {define_on_off(distServer.alarme)}")
        stdscr.addstr(10,0, f"Temperatura: {distServer.temperatura}")
        stdscr.addstr(11,0, f"Umidade: {distServer.umidade}")
        stdscr.addstr(12,0, f"Quantidade de pessoas no andar: {distServer.quantidade_de_pessoas}")
        stdscr.addstr(13,0, f"Lampada 1: {define_on_off(distServer.lampadas[0])}")
        stdscr.addstr(14,0, f"Lampada 2: {define_on_off(distServer.lampadas[1])}")
        stdscr.addstr(15,0, f"Janela 1: {define_open_closed(distServer.janelas[0])}")
        stdscr.addstr(16,0, f"Janela 2: {define_open_closed(distServer.janelas[1])}")
        stdscr.addstr(17,0, f"Ar-condicionado: {define_on_off(distServer.arcondicionado)}")
        stdscr.addstr(18,0, f"Aspersor: {define_on_off(distServer.aspersor)}")
        stdscr.addstr(19,0, f"Porta: {define_open_closed(distServer.porta)}")
        stdscr.addstr(20,0, f"Fumaça: {define_detected(distServer.fumaca)}")
        stdscr.addstr(21,0, f"Quantidade total de pessoas no prédio: {messager.total}")
        stdscr.addstr(22,0, f"Projetor multimídia: {define_on_off(distServer.projector)}")
        stdscr.addstr(23,0, f"Presença: {define_on_off(distServer.presence)}")

        stdscr.noutrefresh()
        curses.doupdate()

    @staticmethod
    def render_menu_input(stdscr, connections: list, state: int) -> None:
        Menu.clear_menu_information(stdscr, 0, 6)

        if state == 0:
            stdscr.addstr(0,0, f"----------- [INPUTS] -----------", curses.A_BOLD)
            stdscr.addstr(1,0, f"Escolha o serviço distribuído:")

            start = 2
            for i in range(start, len(connections)+start):
                stdscr.addstr(i,0, f"[{i-start+1}]: {connections[i-start]['name']}")
            stdscr.addstr(len(connections)+start,0, f"--------------------------------")
        elif state == 1:
            stdscr.addstr(0,0, f"----------- [INPUTS] -----------", curses.A_BOLD)
            stdscr.addstr(1,0, f"[1] Lampada 1 [2] Lampada 2")
            stdscr.addstr(2,0, f"[3] Ar-condicionado [4] Projetor [5] Alarme")
            stdscr.addstr(3,0, f"[BACKSPACE] Escolher outro serviço distribuído", curses.A_BOLD)
            stdscr.addstr(4,0, f"--------------------------------")
        elif state == 2:
            stdscr.addstr(0,0, f"[Não é possível acionar o alarme]", curses.A_BOLD)
            stdscr.addstr(1,0, f"Não é permitido o acionamento do alarme até ")
            stdscr.addstr(2,0, f"que todos os itens que o acionam estejam desativados.")
            stdscr.addstr(3,0, f"[BACKSPACE] Voltar para o menu.", curses.A_BOLD)
            stdscr.addstr(4,0, f"--------------------------------")

        stdscr.noutrefresh()
        curses.doupdate()