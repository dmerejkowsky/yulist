import pymongo

import pytest

from yulist.parser import Parser
from yulist.dumper import Dumper


@pytest.fixture
def db():
    client = pymongo.MongoClient()
    db = client.test_yulist
    yield db
    for collection in db.collection_names():
        db.drop_collection(collection)


def test_dumps_to_mongo(example_path, db):
    parser = Parser(example_path)
    dumper = Dumper(parser, db)
    dumper.dump()
    db = dumper.db
    assert db.pages.count() == 15
    assert db.items.count() == 10
