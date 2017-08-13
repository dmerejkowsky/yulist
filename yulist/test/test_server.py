from yulist.parser import Parser
from yulist.dumper import Dumper

import pytest


@pytest.fixture(autouse=True)
def init_db(example_path, db):
    parser = Parser(example_path)
    dumper = Dumper(parser, db)
    dumper.dump()


def test_index(browser):
    browser.open("/")
    assert "Welcome" in browser.page
