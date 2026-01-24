import config

from luogu import LuoguAPI


if __name__ == "__main__":
    user = input("Enter user (name or uid): ")
    api = LuoguAPI(
        uid=config.uid,
        client_id=config.client_id,
    )
    user_id, user_name = api.search_user(user)
    ccfLevel, xcpcLevel, prizes = api.get_user_achievements(user_id)

    print(f"User ID: {user_id}")
    print(f"User Name: {user_name}")
    print(f"ccfLevel: {ccfLevel}")
    print(f"xcpcLevel: {xcpcLevel}")
    print(prizes)
