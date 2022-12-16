def define_on_off(value):
    if value:
        return "Ligado(a)"
    else:
        return "Desligado(a)"

def define_open_closed(value):
    if value:
        return "Aberto(a)"
    else:
        return "Fechado(a)"

def define_detected(value):
    if value:
        return "Detectada"
    else:
        return "Não detectada"

def append_log_file(value: str):
    with open("log.csv", "a") as f:
        f.write(value + "\n")