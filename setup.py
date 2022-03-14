"""
===============================================
DeFFcode library source-code is deployed under the Apache 2.0 License:

Copyright (c) 2021 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
===============================================
"""

# import the necessary packages
import setuptools
from setuptools import setup
from distutils.util import convert_path

pkg_version = {}
ver_path = convert_path("deffcode/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), pkg_version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = long_description.replace(
        "(#", "(https://github.com/abhiTronix/deffcode#"
    )
    # patch for unicodes
    long_description = long_description.replace("➶", ">>")
    long_description = long_description.replace("©", "(c)")

setup(
    name="deffcode",
    packages=["deffcode"],
    version=pkg_version["__version__"],
    description="High-performance Real-time Video frames Generator for generating blazingly fast video frames in python",
    license="Apache License 2.0",
    author="Abhishek Thakur",
    install_requires=[
        "cython",  # (not really a dependency) just helper for numpy install
        "numpy",
        "requests",
        "colorlog",
        "tqdm",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="abhi.una12@gmail.com",
    url="https://abhitronix.github.io/deffcode",
    keywords=[
        "FFmpeg",
        "Video Processing",
        "Computer Vision",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    scripts=[],
    project_urls={
        "Bug Reports": "https://github.com/abhiTronix/deffcode/issues",
        "Funding": "https://ko-fi.com/W7W8WTYO",
        "Source": "https://github.com/abhiTronix/deffcode",
        "Documentation": "https://abhitronix.github.io/deffcode",
        "Changelog": "https://abhitronix.github.io/deffcode/latest/changelog/",
    },
)
