import pathlib
import webbrowser

import yulist.main


def test_dump(example_path, empty_db):
    yulist.main.dump(example_path, empty_db)
