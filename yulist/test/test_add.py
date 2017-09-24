import pathlib
import shutil

import pytest

import yulist.add
import yulist.config
import yulist.parser


@pytest.fixture
def example_copy(example_path, tmp_path):
    dest_path = tmp_path / "example"
    shutil.copytree(example_path, dest_path)
    return dest_path


def test_add_music_file(example_copy, empty_db):
    db = empty_db
    config = yulist.config.read_conf()
    media_path = pathlib.Path(config["paths"]["media"])
    song_path = media_path / "music/Songs/Kiss/Kiss - I Was Made For Loving You.mp3"

    yulist.add.add_music(example_copy, song_path, "evening")

    parser = yulist.parser.Parser(example_copy)
    items = list(parser.parse())
    dumper = yulist.dumper.Dumper(parser, empty_db)
    dumper.dump()

    evening_page = db.pages.find({"path": "music/evening"})[0]
    evening_songs = db.items.find({"page_id": evening_page["_id"]})

    last_song = list(evening_songs)[-1]
    assert last_song["artist"] == "Kiss"
    assert last_song["title"] == "I Was Made For Loving You"
    assert last_song["music_path"] == "Songs/Kiss/Kiss - I Was Made For Loving You.mp3"
