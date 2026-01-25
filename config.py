import json

try:
    with open("./config/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}

uid = config.get("uid")
client_id = config.get("client_id")
oierdb_result = config.get("oierdb_result")
oierdb_contests = config.get("oierdb_contests")
