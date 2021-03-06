import itertools
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
        try:
            page_id = self.dump_page_metada(page)
            self.dump_items(page, page_id)
        except Exception as error:
            raise yulist.Error("Could not dump", page["path"]) from error

    def dump_items(self, page, page_id):
        top_items = self.yield_top_items(page)
        other_items = self.yield_section_items(page)
        all_items = list(itertools.chain(top_items, other_items))
        if not all_items:
            return
        item_type = page.get("items_type")
        if not item_type:
            message = (
                "Page {path} contains items, but does not have "
                "`items_type` set"
            )
            raise yulist.Error(message.format(path=page["path"]))
        for item in all_items:
            item["page_id"] = page_id
            item["type"] = item_type
            self.db.items.insert_one(item)

    @staticmethod
    def yield_top_items(page):
        yield from page.get("items", list())

    @staticmethod
    def yield_section_items(page):
        sections = page.get("sections", list())
        for section in sections:
            items = section.get("items", list())
            for item in items:
                item["section"] = section["name"]
                yield item

    def dump_page_metada(self, page):
        sections = [x["name"] for x in page.get("sections", list())]
        query = self.db.pages.insert_one(
            {
                "sections": sections,
                "outline": page.get("outline"),
                "title": page["title"],
                "path": str(page["path"]),
                "intro": page.get("intro"),
                "outro": page.get("outro"),
                "toc": page.get("toc"),
            }
        )
        return query.inserted_id


def dump(text_db_path, db):
    parser = yulist.parser.Parser(text_db_path)
    dumper = Dumper(parser, db)
    dumper.dump()
    total_pages = db.pages.count()
    num_items = db.items.count()
    print("Saved %i pages and %i items" % (total_pages, num_items))


def main():
    cfg = yulist.config.read_conf()
    text_db_path = pathlib.Path(cfg["paths"]["text_db"])
    client = pymongo.MongoClient()
    db = client.yulist
    dump(text_db_path, db)
