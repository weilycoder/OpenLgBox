import json

try:
    with open("./config/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}

uid = config.get("uid")
client_id = config.get("client_id")
