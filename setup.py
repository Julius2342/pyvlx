"""Module for setting up PyVLX pypi object."""
import os
from os import path

from setuptools import find_packages, setup

REQUIRES = ["PyYAML"]

PKG_ROOT = os.path.dirname(__file__)

VERSION = "0.2.18"


def get_long_description():
    """Read long description from README.md."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md")) as readme:
        long_description = readme.read()
        return long_description


setup(
    name="pyvlx",
    version=VERSION,
    download_url="https://github.com/Julius2342/pyvlx/archive/" + VERSION + ".zip",
    url="https://github.com/Julius2342/pyvlx",
    description="PyVLX is a wrapper for the Velux KLF 200 API. PyVLX enables you to run scenes and or open and close velux windows.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Julius Mittenzwei",
    author_email="julius@mittenzwei.com",
    license="LGPL",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    install_requires=REQUIRES,
    keywords="velux KLF 200 home automation",
    zip_safe=False,
)
