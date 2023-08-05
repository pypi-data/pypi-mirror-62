import io
import os
import re

from setuptools import find_packages
from setuptools import setup
import requirements
from pathlib import Path


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


def get_requires():
    r_path = Path(__file__).parent / 'requirements.txt'
    if r_path.exists():
        reqs = list(requirements.parse(r_path.read_text()))
        return [req.line for req in reqs]
    else:
        return []


setup(
    name="loglevel",
    version="0.1.1",
    url="",
    license='MIT',

    author="fx-kirin",
    author_email="fx.kirin@gmail.com",

    description="",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=get_requires(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
