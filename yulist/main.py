""" Main entry point """

import pathlib

import ruamel.yaml

import yulist.builder


def read_conf():
    cfg_path = pathlib.Path("~/.config/yulist.yml").expanduser()
    return ruamel.yaml.safe_load(cfg_path.read_text())


def build(src_path, dest_path, *, prefix="", url="", media_url=""):
    builder = yulist.builder.Builder(src_path, dest_path,
                                     prefix=prefix,
                                     media_url=media_url,
                                     output_format="html")
    builder.build()


def main():
    config = read_conf()
    src = pathlib.Path(config["src"])
    dest = pathlib.Path(config["dest"])
    media_url = pathlib.Path(config["media"]["url"])
    prefix = config.get("web", {}).get("prefix", "")
    build(src, dest, prefix=prefix, media_url=media_url)
