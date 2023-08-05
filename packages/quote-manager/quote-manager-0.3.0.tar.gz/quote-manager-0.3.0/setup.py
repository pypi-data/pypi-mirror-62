import os

from setuptools import setup, find_packages
from typing import List


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


# This currently has no purpose
# In other projects we do this so that VERSION can be read by CICD system easily
# Such as what we do in ./build_release.sh
# Copying to marian_client/version.py is to make it available at runtime
# so we could add version info to MarianClient class
# I guess this is a @TODO
with open(os.path.join(here, "VERSION"), encoding="utf-8") as f:
    __version__ = f.read().strip()
    with open(
        os.path.join(here, "quote_manager", "version.py"), "w+", encoding="utf-8"
    ) as v:
        v.write("# CHANGES HERE HAVE NO EFFECT: ../VERSION is the source of truth\n")
        v.write(f'__version__ = "{__version__}"')


setup(
    name="quote-manager",
    packages=find_packages(),
    author="Qordoba",
    author_email="Sam Havens <sam.havens@qordoba.com>",
    url="https://github.com/Qordobacode/library.quote.manager",
    version=__version__,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.4",
    install_requires=["diff-match-patch==20181111"],
    tests_require=[
                    "twine>=3.1.0",
                    "pytest==5.3.1",
    ],
)
