import pymongo

from yulist.parser import Parser
from yulist.dumper import Dumper


def test_dumps_to_mongo(example_path, db):
    parser = Parser(example_path)
    dumper = Dumper(parser, db)
    dumper.dump()
    db = dumper.db
    assert db.pages.count() == 15
    assert db.items.count() == 10
