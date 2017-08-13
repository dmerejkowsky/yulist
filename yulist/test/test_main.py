import pathlib
import webbrowser

import yulist.main


def test_build_site(tmp_path, example_path):
    yulist.main.build(src_path=example_path, dest_path=tmp_path)
    index_html = tmp_path / "index.html"
    css = tmp_path / "static" / "style.css"
    assert index_html.exists()
    assert css.exists()
