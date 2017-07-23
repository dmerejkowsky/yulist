import pathlib
import shutil

from yulist.parser import Parser
from yulist.generator import Generator


class Builder:
    def __init__(self, src_path, dest_path, prefix="", output_format="html"):
        self.src_path = src_path
        self.dest_path = dest_path
        self.output_format = output_format
        self.parser = Parser(src_path)
        self.generator = Generator(prefix=prefix,
                                   output_format=self.output_format)

    def build(self):
        print("Building site ...")
        self.build_pages()
        self.copy_static_files()
        print("Done")

    def build_pages(self):
        n = 0
        for page in self.parser.parse():
            out_path = self.dest_path / page["path"]
            out_path = out_path.with_suffix("." + self.output_format)
            n += 1
            out_path.parent.mkdir(parents=True, exist_ok=True)
            page_content = self.generator.generate_page(page)
            out_path.write_text(page_content)
        print("*", "Written", n, "pages")

    def copy_static_files(self):
        this_path = pathlib.Path(__file__).parent
        static_path = this_path / "static"
        n = 0
        for entry in static_path.glob("**/*"):
            rel_path = entry.relative_to(this_path)
            full_dest = self.dest_path / rel_path
            full_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(entry, full_dest)
            n += 1
        print("*", "Copied", n, "static file(s)")
