import ruamel.yaml


class Parser():
    def __init__(self, src_path):
        self.src_path = src_path
        self.items = list()

    def parse(self):
        top_yml = self.src_path / "index.yml"
        self._parse_file(top_yml)

    def _parse_file(self, yml_path):
        contents = ruamel.yaml.safe_load(yml_path.read_text())
        rel_path = yml_path.relative_to(self.src_path)
        rel_path = rel_path.with_suffix("")
        contents["path"] = str(rel_path)
        self.items.append(contents)
        toc = contents.get("toc")
        if toc:
            self._parse_toc(yml_path, toc)
        return contents

    def _parse_toc(self, yml_path, toc_entries):
        for entry in toc_entries:
            self._parse_toc_entry(yml_path, entry)

    def _parse_toc_entry(self, yml_path, entry):
        entry_path = yml_path.parent / entry
        if entry_path.is_dir():
            yml_path = entry_path / "index.yml"
        else:
            yml_path = entry_path.with_suffix(".yml")
        self._parse_file(yml_path)
