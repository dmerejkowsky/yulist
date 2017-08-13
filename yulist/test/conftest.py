import pathlib

import pymongo

import yulist.server

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
def db():
    client = pymongo.MongoClient()
    db = client.test_yulist
    yield db
    for collection in db.collection_names():
        db.drop_collection(collection)


@pytest.fixture
def app():
    return yulist.server.app


class Browser():
    def __init__(self, flask_client):
        self._flask_client = flask_client

    def open(self, url):
        response = self._flask_client.get(url)
        assert 200 <= response.status_code < 400
        self.page = response.data.decode()

    @property
    def html_soup(self):
        return bs4.BeautifulSoup(self.page, "html.parser")

    def clink_link(self, link):
        assert link is not None
        href = link.attrs["href"]
        self.open(href)


@pytest.fixture()
def browser(client):
    return Browser(client)
