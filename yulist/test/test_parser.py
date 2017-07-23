import yulist.parser


def test_parse(example_path):
    parser = yulist.parser.Parser(example_path)
    items = list(parser.parse())
    first = items[0]
    assert first["title"] == "Welcome to YuList"
    expected_paths = ["software/index", "music/index", "text/index", "video/index"]
    actual_paths = [str(x["path"]) for x in first["toc"]]
    assert expected_paths == actual_paths
    assert str(first["path"]) == "index"

    software = items[1]
    assert software["title"] == "Software"
    assert str(software["path"]) == "software/index"

    mcu = [x for x in items if x["title"] == "Marvel Cinematic Universe"][0]
    assert str(mcu["path"]) == "video/movies/mcu"
