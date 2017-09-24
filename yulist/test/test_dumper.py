import pymongo

from yulist.parser import Parser
from yulist.dumper import Dumper


def test_dumps_to_mongo(example_path, empty_db):
    parser = Parser(example_path)
    dumper = Dumper(parser, empty_db)
    dumper.dump()
    db = dumper.db

    software_page = db.pages.find_one({"title": "Software"})
    assert software_page["sections"] == ["Misc", "Building stuff", "For Python"]
    page_id = software_page["_id"]
    software_links = list(db.items.find({"page_id": page_id}))
    add_include = software_links[0]
    assert add_include.get("section") == "Misc"
    bazel = software_links[2]
    assert bazel["section"] == "Building stuff"
