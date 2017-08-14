""" Main entry point """

import pathlib

import pymongo

import yulist.config
import yulist.parser
import yulist.dumper


def dump(src_path, db):
    parser = yulist.parser.Parser(src_path)
    dumper = yulist.dumper.Dumper(parser, db)
    dumper.dump()
    print("Saved %i pages and %i items" % (db.pages.count(), db.items.count()))


def main():
    config = yulist.config.read_conf()
    client = pymongo.MongoClient()
    db = client.yulist
    src = pathlib.Path(config["src"])
    dump(src, db)
