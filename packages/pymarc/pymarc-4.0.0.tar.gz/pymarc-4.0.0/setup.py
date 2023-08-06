# This file is part of pymarc. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution and at
# https://opensource.org/licenses/BSD-2-Clause. pymarc may be copied, modified,
# propagated, or distributed according to the terms contained in the LICENSE
# file.

"""Pymarc setup."""

from setuptools import setup

version = "4.0.0"

classifiers = """
Intended Audience :: Education
Intended Audience :: Developers
Intended Audience :: Information Technology
License :: OSI Approved :: BSD License
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Text Processing :: General
"""


with open("README.md") as f:
    long_description = f.read()

setup(
    name="pymarc",
    version=version,
    url="http://gitlab.com/pymarc/pymarc",
    author="Ed Summers",
    author_email="ehs@pobox.com",
    license="http://www.opensource.org/licenses/bsd-license.php",
    packages=["pymarc"],
    description="Read, write and modify MARC bibliographic data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=list(filter(None, classifiers.split("\n"))),
    test_suite="test",
    python_requires=">=3.6.*",
)
