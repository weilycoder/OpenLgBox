import json

from luogu import LuoguAPI


if __name__ == "__main__":
    try:
        with open("./config/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    user = input("Enter user name: ")
    api = LuoguAPI(
        uid=config.get("uid"),
        client_id=config.get("client_id"),
    )
    user_id, user_name = api.search_user(user)
    data = api.get_user_achievements(user_id)

    print(f"User ID: {user_id}")
    print(f"User Name: {user_name}")
    print(f"ccfLevel: {data['ccfLevel']}")
    print(f"xcpcLevel: {data['xcpcLevel']}")
    print(json.dumps(data["prizes"], indent=4, ensure_ascii=False))
