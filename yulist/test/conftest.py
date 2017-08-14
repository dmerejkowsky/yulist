import pathlib

import bs4
import pymongo

import yulist.server
from yulist.parser import Parser
from yulist.dumper import Dumper


import pytest


@pytest.fixture
def tmp_path(tmpdir):
    return pathlib.Path(tmpdir)


@pytest.fixture
def test_data():
    return pathlib.Path(__file__).parent / "data"


@pytest.fixture
def example_path():
    return pathlib.Path(__file__).parent.parent.parent / "example"


@pytest.fixture
def empty_db():
    client = pymongo.MongoClient()
    db = client.test_yulist
    yield db
    for collection in db.collection_names():
        db.drop_collection(collection)


@pytest.fixture
def full_db(example_path, empty_db):
    parser = Parser(example_path)
    dumper = Dumper(parser, empty_db)
    dumper.dump()
    return dumper.db


@pytest.fixture
def app(full_db):
    res = yulist.server.app
    yulist.server.configure_app(db=full_db)

    return res


class Browser():
    def __init__(self, flask_client):
        self._flask_client = flask_client

    def open(self, url):
        response = self._flask_client.get(url)
        assert 200 <= response.status_code < 400
        self.page = response.data.decode()

    def submit_form(self, url, **kwargs):
        response = self._flask_client.post(url, data=kwargs, follow_redirects=True)
        assert 200 <= response.status_code < 400
        self.page = response.data.decode()

    @property
    def html_soup(self):
        return bs4.BeautifulSoup(self.page, "html.parser")

    def find_link(self, text):
        link = self.html_soup.find("a", text=text)
        return link

    def click_link(self, link):
        assert link is not None
        href = link.attrs["href"]
        self.open(href)


@pytest.fixture
def browser(app, client):
    return Browser(client)
