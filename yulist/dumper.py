import pathlib

import pymongo

import yulist.config
import yulist.parser


class Dumper:
    def __init__(self, parser, db):
        self.parser = parser
        self.db = db

    def dump(self):
        self.db.items.drop()
        self.db.pages.drop()
        self.db.items.create_index(
            [
                ("title", pymongo.TEXT),
                ("artist", pymongo.TEXT),
                ("text", pymongo.TEXT),
            ]
        )
        for page in self.parser.parse():
            self.dump_page(page)

    def dump_page(self, page):
        page_id = self.db.pages.insert_one(
            {
                "title": page["title"],
                "path": str(page["path"]),
                "intro": page.get("intro"),
                "outro": page.get("outro"),
                "toc": page.get("toc"),
                "private": page.get("private"),
            }
        ).inserted_id
        for item in page.get("items", list()):
            item_type = page.get("items_type")
            if not item_type:
                raise Exception("Page %s does not contain items_type" % page["path"])
            self.dump_item(item, page_id=page_id, item_type=item_type)

    def dump_item(self, item, *, page_id, item_type):
        item["page_id"] = page_id
        item["type"] = item_type
        self.db.items.insert_one(item)


def dump(src_path, db):
    parser = yulist.parser.Parser(src_path)
    dumper = Dumper(parser, db)
    dumper.dump()
    print("Saved %i pages and %i items" % (db.pages.count(), db.items.count()))


def main():
    config = yulist.config.read_conf()
    client = pymongo.MongoClient()
    db = client.yulist
    src = pathlib.Path(config["src"])
    dump(src, db)
