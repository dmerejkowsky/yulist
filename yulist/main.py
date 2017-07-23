""" Main entry point """


# pylint: disable=unused-argument
def generate(*, src_path, dest_path):
    index_html = dest_path / "index.html"
    index_html.write_text("This is an index")


def main():
    pass
