import setuptools
import re
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setuptools.setup(
    name="pyShellyEx",
    version=find_version("pyShelly", "const.py"),
    author="StyraHem / Tarra AB",
    author_email="info@styrahem.se",
    description="Library for Shelly smart home devices (Modified version)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoNzCiD/pyShelly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
