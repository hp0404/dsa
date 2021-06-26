import os
from setuptools import setup, find_packages
from dsa import __version__


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="dsa",
    version=__version__,
    url="https://github.com/hp0404/dsa.git",
    author="Hryhorii Pavlenko",
    author_email="hryhorii.pavlenko@gmail.com",
    description="Опрацювання протоколів автоматизованого розподілу судових справ між суддями",
    long_description=get_long_description(),
    packages=find_packages(),
)