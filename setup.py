import sys
from setuptools import setup, find_packages

if sys.version_info.major < 2:
    sys.exit("Error: Please upgrade to Python3")

setup(name="yulist",
      version="0.1",
      description="Hosts lists of things",
      url="https://dmerej.info/yulist",
      author="Dimitri Merejkowsky",
      author_email="d.merej@gmail.com",
      license="BSD",
      packages=find_packages(),
      install_requires=[
        "attrs",
        "bcrypt",
        "flask",
        "Flask-login",
        "jinja2",
        "jinja2-slug",
        "markdown",
        "pymongo",
        "pytaglib",
        "ruamel.yaml",
      ],
      entry_points={
        "console_scripts": [
          "yulist-add = yulist.add:main",
          "yulist-dump = yulist.dumper:main",
          "yulist-server = yulist.server:main",
          "yulist-admin = yulist.admin:main",
        ]
      })
