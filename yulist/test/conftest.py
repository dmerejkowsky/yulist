import pathlib

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
