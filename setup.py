import os
import pathlib
import setuptools
from sys import version_info, exit
from pkg_resources import parse_requirements


def write_version_py():
    with open(os.path.join("indicnlp", "version.txt"), "r") as f:
        version = f.read().strip()

    with open(os.path.join("indicnlp", "version.py"), "w") as f:
        f.write(f'__version__ = "{version}"')
    return version


if version_info < (3, 8):
    exit("Sorry, Python >= 3.8 is required for IndicNLP Library for IT2")

with open("README.md", "r", errors="ignore", encoding="utf-8") as fh:
    long_description = fh.read()

version = write_version_py()

setuptools.setup(
    name="indic_nlp_library_IT2",  # Replace with your own username
    version=version,
    author="Varun Gumma",
    author_email="varun230999@gmail.com",
    description="The goal of the Indic NLP Library is to build Python based libraries for common"
    " text processing and Natural Language Processing in Indian languages. This fork is specialized for IndicTrans2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VarunGumma/indic_nlp_library",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        str(requirement)
        for requirement in parse_requirements(pathlib.Path("requirements.txt").open())
    ],
)
