import sys
import bcrypt
import pymongo


def main():
    username = sys.argv[1]
    password = sys.argv[2]
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    client = pymongo.MongoClient()
    users = client.yulist.users
    users.create_index("user_id", unique=True)
    query_filter = {"user_id": username}
    query_update = query_filter.copy()
    query_update.update({"hashed_password": hashed_password})
    users.update(query_filter, query_update, upsert=True)
    for user in users.find():
        print(user["user_id"])


if __name__ == "__main__":
    main()
