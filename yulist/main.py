""" Main entry point """

import yulist.builder


def build(*, src_path, dest_path, output_format="html"):
    builder = yulist.builder.Builder(src_path, dest_path, output_format=output_format)
    builder.build()


def main():
    pass
