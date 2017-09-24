""" Add something to a page """

import argparse
import pathlib
import subprocess
import sys

import ruamel.yaml
import taglib
import ui

import yulist.config


def add_music(text_db_path, music_path, kind):
    cfg = yulist.config.read_conf()
    media_path = pathlib.Path(cfg["paths"]["media"])
    music_root_path = media_path / "music"

    # pylint: disable=no-member
    tagfile = taglib.File(str(music_path))
    artist = tagfile.tags["ARTIST"][0]
    title = tagfile.tags["TITLE"][0]
    music_rel_path = music_path.absolute().relative_to(music_root_path)

    new_item = {
        "artist": artist,
        "title": title,
        "music_path": str(music_rel_path)
    }
    yaml_path = (text_db_path / "music" / kind).with_suffix(".yml")
    data = ruamel.yaml.load(yaml_path.read_text(), ruamel.yaml.RoundTripLoader)
    data["items"].append(new_item)

    dumped = ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper)
    yaml_path.write_text(dumped)
    desc = '%s - "%s"' % (artist, title)
    return desc


def push_db(text_db_path, kind, desc):
    cmd = ["git", "add", "."]
    subprocess.run(cmd, check=True, cwd=text_db_path)
    cmd = ["git", "commit", "--message", "%s: add %s" % (kind, desc)]
    subprocess.run(cmd, check=True, cwd=text_db_path)
    cmd = ["git", "diff", "--color=always", "HEAD~1", "HEAD"]
    subprocess.run(cmd, check=True, cwd=text_db_path)
    should_push = ui.ask_yes_no("OK to push?", default=True)
    if not should_push:
        sys.exit(1)
    cmd = ["git", "push"]
    subprocess.run(cmd, check=True, cwd=text_db_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("music_path", type=pathlib.Path)
    parser.add_argument("-k", "--kind", required=True)
    args = parser.parse_args()
    music_path = args.music_path
    kind = args.kind
    cfg = yulist.config.read_conf()
    text_db_path = pathlib.Path(cfg["paths"]["text_db"])
    desc = add_music(text_db_path, music_path, kind)
    push_db(text_db_path, kind, desc)


if __name__ == "__main__":
    main()
