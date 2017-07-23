import sys
import subprocess

import pathlib


def collect_sources(ignore_func):
    top_path = pathlib.Path(".")
    for py_path in top_path.glob("**/*.py"):
        if not ignore_func(py_path):
            yield py_path


def ignore(p):
    """ Ignore hidden and test files """
    if any(x.startswith(".") for x in p.parts):
        return True
    if 'test' in p.parts:
        return True
    return False


def run_pyflakes():
    cmd = ["pyflakes"]
    cmd.extend(collect_sources(ignore_func=ignore))
    return subprocess.call(cmd)


if __name__ == "__main__":
    rc = run_pyflakes()
    sys.exit(rc)
