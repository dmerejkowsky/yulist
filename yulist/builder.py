import shutil

import yulist.parser
import yulist.generator


class Builder:
    def __init__(self, src_path, dest_path, output_format="html"):
        self.src_path = src_path
        self.dest_path = dest_path
        self.output_format = output_format
        self.parser = yulist.parser.Parser(src_path)
        self.generator = yulist.generator.Generator(output_format=self.output_format)

    def build(self):
        self.build_pages()
        self.copy_static_files()

    def build_pages(self):
        for page in self.parser.parse():
            out_path = self.dest_path / page["path"]
            out_path = out_path.with_suffix("." + self.output_format)
            print("::", out_path.relative_to(self.dest_path))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            page_content = self.generator.generate_page(page)
            out_path.write_text(page_content)

    def copy_static_files(self):
        static_path = self.src_path / "static"
        for entry in static_path.glob("**/*"):
            rel_path = entry.relative_to(self.src_path)
            full_dest = self.dest_path / rel_path
            full_dest.parent.mkdir(parents=True, exist_ok=True)
            print("->", rel_path)
            shutil.copy(entry, full_dest)
