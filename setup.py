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
        "jinja2",
        "markdown",
        "ruamel.yaml",
      ],
      entry_points={
        "console_scripts": [
          "yulist = yulist.main:main",
        ]
      })
