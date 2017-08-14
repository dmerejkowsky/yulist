import argparse
import sys

import bcrypt
import pymongo


def set_password(db, username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users = db.users
    users.create_index("user_id", unique=True)
    query_filter = {"user_id": username}
    query_update = query_filter.copy()
    query_update.update({"hashed_password": hashed_password})
    users.update(query_filter, query_update, upsert=True)


def main_set_password(args):
    username = args.username
    password = args.password
    client = pymongo.MongoClient()
    db = client.yulist
    set_password(db, username, password)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="action", dest="action")
    set_pw_parser = subparsers.add_parser("set_pw")
    set_pw_parser.add_argument("-u", "--username", required=True)
    set_pw_parser.add_argument("-p", "--password", required=True)
    args = parser.parse_args()
    if args.action == "set_pw":
        main_set_password(args)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
