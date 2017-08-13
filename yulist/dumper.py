class Dumper:
    def __init__(self, parser, db):
        self.parser = parser
        self.db = db

    def dump(self):
        for page in self.parser.parse():
            self.dump_page(page)

    def dump_page(self, page):
        page_id = self.db.pages.insert_one(
            {
                "path": str(page["path"]),
                "intro": page.get("intro"),
                "outro": page.get("outro"),
                "toc": page.get("toc"),
            }
        ).inserted_id
        for item in page.get("items", list()):
            self.dump_item(page_id, item)

    def dump_item(self, page_id, item):
        item["page_id"] = page_id
        self.db.items.insert_one(item)
