import json

def json_config_parse(path: str) -> dict:
    file = open(path)
    return json.load(file)