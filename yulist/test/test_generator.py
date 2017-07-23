import textwrap

import ruamel.yaml

import yulist.generator


def test_text_generator(test_data):
    in_yml = test_data / "software.yml"
    page = ruamel.yaml.safe_load(in_yml.read_text())
    out_html = test_data / "software.txt"
    expected = out_html.read_text()
    generator = yulist.generator.Generator(output_format="txt")
    actual = generator.generate_page(page)
    actual_path = test_data / "software.actual.txt"
    if actual != expected:
        actual_path.write_text(actual)
        assert False
