import yulist.generator


def test_generate_bread_cumbs():
    generator = yulist.generator.Generator(output_format="html")
    actual = generator.generate_bread_crumbs("software/python/index")
    assert actual == [
        {"link": "/index.html", "text": "home"},
        {"link": "/software/index.html", "text": "software"},
        {"link": "/software/python/index.html", "text": "python"},
    ]
