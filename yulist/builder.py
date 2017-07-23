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
        for page in self.parser.parse():
            out_path = self.dest_path / page["path"]
            out_path = out_path.with_suffix("." + self.output_format)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            page_content = self.generator.generate_page(page)
            out_path.write_text(page_content)
            print(out_path.relative_to(self.dest_path))
