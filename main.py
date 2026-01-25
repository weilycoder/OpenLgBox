import argparse

import rich

import config

from luogu import LuoguAPI
from oierdb import oierdb


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find matching OIER records based on Luogu user achievements.")
    parser.add_argument("user", type=str, help="Luogu user (name or uid)")
    parser.add_argument("-s", "--strict", action="store_true", help="Enable strict matching (all records must match)")
    parser.add_argument("-u", "--uid", type=int, default=None, help="Luogu API UID")
    parser.add_argument("-c", "--client_id", type=str, default=None, help="Luogu API Client ID")
    parser.add_argument("-i", "--initials", type=str, default=None, help="Filter by guessed initials (use `,` to separate multiple)")
    parser.add_argument("--only-search", action="store_true", help="Only search for user info without filtering OIERDB")

    args = parser.parse_args()
    initials = None if args.initials is None else args.initials.split(",")
    if args.uid is not None:
        if args.uid is not None:
            rich.print("[yellow][i]Warning: Overriding config.uid with command line argument.[/i][/yellow]")
        config.uid = args.uid
    if args.client_id is not None:
        if args.client_id is not None:
            rich.print("[yellow][i]Warning: Overriding config.client_id with command line argument.[/i][/yellow]")
        config.client_id = args.client_id

    api = LuoguAPI(
        uid=config.uid,
        client_id=config.client_id,
    )
    user_id, user_name = api.search_user(args.user)
    ccfLevel, xcpcLevel, prizes = api.get_user_achievements(user_id)

    rich.print(f"User ID: {user_id}")
    rich.print(f"User Name: {user_name}")
    rich.print(f"ccfLevel: {ccfLevel}")
    rich.print(f"xcpcLevel: {xcpcLevel}")
    rich.print(f"prizes: {prizes}")

    if not args.only_search:
        rich.print("Removing contest which are not in OIERDB...")
        prizes = [prize for prize in prizes if prize[0] in oierdb.contest_names]
        rich.print(f"Remaining prizes: {prizes}")

        rich.print("Filtering OIERDB records...")
        leave = list(
            filter(
                lambda oier: oier.ccf_level >= ccfLevel
                and (initials is None or oier.initials in initials)
                and (not args.strict or len(oier.records) == len(prizes))
                and all(any(record.check(*prize) for record in oier.records) for prize in prizes),
                oierdb.oiers,
            )
        )
        leave.sort(key=lambda oier: (len(oier.records), -oier.oierdb_score))
        rich.print(f"Found {len(leave)} matching records:")
        for oier in leave:
            rich.print("*", oier.uid, oier.initials, oier.name, oier.ccf_level)
