import pymongo


def test_stores_and_search_docs():
    client = pymongo.MongoClient()
    db = client.test_yulist
    pages = db.pages
    pages.drop()
    page1 = pages.insert_one(
        {
            "name": "songs"
        }
    ).inserted_id
    items = db.items
    items.drop()
    items.create_index(
        [
            ("title", pymongo.TEXT),
            ("artist", pymongo.TEXT),
        ]
    )
    id1 = items.insert_one(
        {
            "type": "song",
            "title": "Lâche l'affaire",
            "artist": "Renaud",
            "page_id": page1
        }
    )
    id2 = items.insert_one(
        {
            "type": "song",
            "title": "I Will Survive",
            "artist": "Gloria Gaynor",
            "page_id": page1
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

    cursor = pages.find({"_id": page1})
    print(list(cursor))

    cursor = items.find({"page_id": page1})
    print(list(cursor))
