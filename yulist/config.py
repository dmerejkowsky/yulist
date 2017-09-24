import pathlib
import ruamel.yaml


def get_cfg_path():
    return pathlib.Path("~/.config/yulist.yml").expanduser()


def read_conf():
    cfg_path = get_cfg_path()
    return ruamel.yaml.safe_load(cfg_path.read_text())
