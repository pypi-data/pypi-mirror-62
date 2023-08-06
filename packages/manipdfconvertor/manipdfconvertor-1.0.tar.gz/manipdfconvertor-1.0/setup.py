import setuptools
from pathlib import Path

setuptools.setup(
    name="manipdfconvertor",
    version=1.0,
    long_desxription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test","data"])
)