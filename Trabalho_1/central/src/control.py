def can_turn_on_alarm_building(connections):
    for connection in connections:
        if not can_turn_on_alarm(connection["dist_server"]):
            return False

    return True
        
def can_turn_on_alarm(dist_server):
    if dist_server.janelas[0] or dist_server.janelas[1]: return False
    elif dist_server.porta: return False
    elif dist_server.presence: return False
    elif dist_server.fumaca: return False
    
    return True