""" Main entry point """

import pathlib

import pymongo
import ruamel.yaml

import yulist.parser
import yulist.dumper


def read_conf():
    cfg_path = pathlib.Path("~/.config/yulist.yml").expanduser()
    return ruamel.yaml.safe_load(cfg_path.read_text())


def dump(src_path, db):
    parser = yulist.parser.Parser(src_path)
    dumper = yulist.dumper.Dumper(parser, db)
    dumper.dump()
    print("Saved %i pages and %i items" % (db.pages.count(), db.items.count()))


def main():
    config = read_conf()
    client = pymongo.MongoClient()
    db = client.yulist
    for collection in db.collection_names():
        db.drop_collection(collection)
    src = pathlib.Path(config["src"])
    dump(src, db)
