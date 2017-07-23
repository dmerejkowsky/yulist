import pathlib

import yulist.generator


def test_generate_bread_cumbs():
    generator = yulist.generator.Generator(output_format="html")
    actual = generator.generate_bread_crumbs(pathlib.Path("software/python/index"))
    assert actual == [
        {"link": "/index.html", "text": "home"},
        {"link": "/software/index.html", "text": "software"},
        {"link": "/software/python/index.html", "text": "python"},
    ]


def test_generate_toc_entries():
    toc = ["foo/index", "bar"]
    generator = yulist.generator.Generator(output_format="html")
    actual = generator.generate_toc_links(pathlib.Path("spam/eggs/index"), toc)
    assert actual == [
        {"link": "/spam/eggs/foo/index.html",  "text": "foo"},
        {"link": "/spam/eggs/bar.html",  "text": "bar"},
    ]


def test_generate_toc_entries_root():
    toc = ["foo/index", "bar"]
    generator = yulist.generator.Generator(output_format="html")
    actual = generator.generate_toc_links(pathlib.Path("index"), toc)
    assert actual == [
        {"link": "/foo/index.html",  "text": "foo"},
        {"link": "/bar.html",  "text": "bar"},
    ]
