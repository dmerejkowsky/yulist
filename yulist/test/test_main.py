import pathlib

import yulist.main


def test_gen_site(tmp_path, example_path):
    args = [example_path, tmp_path]
    yulist.main.generate(src_path=example_path, dest_path=tmp_path)
    index_html = tmp_path / "index.html"
    assert index_html.exists()
