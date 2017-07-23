import yulist.parser


def test_parse(example_path):
    parser = yulist.parser.Parser(example_path)
    parser.parse()
    items = parser.items
    first = items[0]
    assert first["title"] == "Welcome to YuList"
    assert first["toc"] == ["software", "music", "text", "video"]
    assert first["path"] == "index"

    software = items[1]
    assert software["title"] == "Software"
    assert software["path"] == "software/index"

    mcu = [x for x in items if x["title"] == "Marvel Cinematic Universe"][0]
    assert mcu["path"] == "video/movies/mcu"
