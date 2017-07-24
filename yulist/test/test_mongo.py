import pymongo


def test_stores_and_search_docs():
    client = pymongo.MongoClient()
    db = client.yulist
    items = db.items
    items.drop()
    items.create_index(
        [
            ("title", pymongo.TEXT),
            ("artist", pymongo.TEXT),
        ]
    )
    items.insert_one(
        {
            "type": "song",
            "title": "Lâche l'affaire",
            "artist": "Renaud",
        }
    )
    items.insert_one(
        {
            "type": "song",
            "title": "I Will Survive",
            "artist": "Gloria Gaynor",
        }
    )

    cursor = items.find(
        {
            "$text": {"$search": "renaud"},
        }
    )

    assert len(list(cursor)) == 1

    cursor = items.find(
        {
            "$text": {"$search": "lâche"},
        }
    )
    assert len(list(cursor)) == 1
