"""Module for setting up PyVLX pypi object."""
import io
import os

from setuptools import find_packages, setup

REQUIRES = [
    'PyYAML'
]

PKG_ROOT = os.path.dirname(__file__)

VERSION = '0.2.11'

# Error-handling here is to allow package to be built w/o README included
try:
    README = io.open(os.path.join(PKG_ROOT, 'README.md'), encoding='utf-8').read()
except IOError:
    README = ''

setup(
    name='pyvlx',

    version=VERSION,
    download_url='https://github.com/Julius2342/pyvlx/archive/'+VERSION+'.zip',
    url='https://github.com/Julius2342/pyvlx',

    description="PyVLX is a wrapper for the Velux KLF 200 API.\n\nPyVLX enables you to run scenes and or open and close velux windows.",
    long_description=README,
    author='Julius Mittenzwei',
    author_email='julius@mittenzwei.com',
    license='LGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    packages=find_packages(),
    install_requires=REQUIRES,
    keywords='velux KLF 200 home automation',
    zip_safe=False)
