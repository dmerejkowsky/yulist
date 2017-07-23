""" Main entry point """

import argparse
import pathlib

import yulist.builder


def build(*, src_path, dest_path, prefix="", output_format="html"):
    builder = yulist.builder.Builder(src_path, dest_path,
                                     prefix=prefix,
                                     output_format=output_format)
    builder.build()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=pathlib.Path)
    parser.add_argument("dest", type=pathlib.Path)
    parser.add_argument("--prefix")
    args = parser.parse_args()
    build(src_path=args.src, dest_path=args.dest, prefix=args.prefix)
