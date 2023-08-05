from setuptools import setup, find_namespace_packages
from optimeed import VERSION
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="optimeed",
    version="{}".format(VERSION),
    author="Christophe De Gréef",
    author_email="christophe.degreef@uclouvain.be",
    description="Powerful ptimization and vizualisation tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.immc.ucl.ac.be/chdegreef/optimeed",
    packages=find_namespace_packages(include=['optimeed.*']),
    install_requires=['numpy', 'PyOpenGL', 'PyQt5', 'pytypes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.6',
)
