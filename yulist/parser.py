import ruamel.yaml


class Parser():
    def __init__(self, src_path):
        self.src_path = src_path

    def parse(self):
        top_yml = self.src_path / "index.yml"
        yield from self._parse_file(top_yml)

    def _parse_file(self, yml_path):
        try:
            contents = ruamel.yaml.safe_load(yml_path.read_text())
        except ruamel.yaml.parser.ParserError as error:
            print(error)
            raise Exception("Invaild yaml at", yml_path) from None
        rel_path = yml_path.relative_to(self.src_path)
        rel_path = rel_path.with_suffix("")
        contents["path"] = rel_path
        yield contents
        toc = contents.get("toc")
        if toc:
            yield from self._parse_toc(yml_path, toc)
        return contents

    def _parse_toc(self, yml_path, toc_entries):
        for entry in toc_entries:
            yield from self._parse_toc_entry(yml_path, entry)

    def _parse_toc_entry(self, yml_path, entry):
        entry_path = yml_path.parent / entry["path"]
        yml_path = entry_path.with_suffix(".yml")
        yield from self._parse_file(yml_path)
