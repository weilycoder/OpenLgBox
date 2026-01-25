import config

from luogu import LuoguAPI
from oierdb import oierdb


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
    print(f"prizes: {prizes}")

    print("\nRemoving contest which are not in OIERDB...")
    prizes = [prize for prize in prizes if prize[0] in oierdb.contest_names]
    print(f"Remaining prizes: {prizes}")

    print("\nFiltering OIERDB records...")
    leave = list(
        filter(
            lambda oier: oier.ccf_level >= ccfLevel
            and (not config.strict or len(oier.records) == len(prizes))
            and all(any(record.check(*prize) for record in oier.records) for prize in prizes),
            oierdb.oiers,
        )
    )
    leave.sort(key=lambda oier: (len(oier.records), -oier.oierdb_score))
    print(f"Found {len(leave)} matching records:")
    for oier in leave:
        print("*", oier.uid, oier.initials, oier.name, oier.ccf_level, sep=" ")
