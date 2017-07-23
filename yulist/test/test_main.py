import pathlib

import yulist.main


def test_build_site(tmp_path, example_path):
    args = [example_path, tmp_path]
    yulist.main.build(src_path=example_path, dest_path=tmp_path, output_format="txt")
    index_html = tmp_path / "index.txt"
    assert index_html.exists()
