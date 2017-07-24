import pathlib
import shutil

from yulist.parser import Parser
from yulist.generator import Generator


class Builder:
    def __init__(self, src_path, dest_path, media_url=""):
        self.src_path = src_path
        self.dest_path = dest_path
        self.parser = Parser(src_path)
        self.generator = Generator(media_url=media_url)

    def build(self):
        print("Building site ...")
        self.build_pages()
        self.copy_static_files()
        print("Done")

    def build_pages(self):
        pages_built = 0
        for page in self.parser.parse():
            out_path = self.dest_path / page["path"]
            out_path = out_path.with_suffix(".html")
            pages_built += 1
            out_path.parent.mkdir(parents=True, exist_ok=True)
            page_content = self.generator.generate_page(page)
            out_path.write_text(page_content)
        print("*", "Written", pages_built, "pages")

    def copy_static_files(self):
        this_path = pathlib.Path(__file__).parent
        static_path = this_path / "static"
        copied_files = 0
        # pylint: disable=no-member
        for entry in static_path.glob("**/*"):
            rel_path = entry.relative_to(this_path)
            full_dest = self.dest_path / rel_path
            full_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(entry, full_dest)
            copied_files += 1
        print("*", "Copied", copied_files, "static file(s)")
