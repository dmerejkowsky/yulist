import pathlib
import ruamel.yaml


def read_conf():
    cfg_path = pathlib.Path("~/.config/yulist.yml").expanduser()
    return ruamel.yaml.safe_load(cfg_path.read_text())
