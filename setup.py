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

from setuptools import setup

# apply various patches to README text and prepare
# valid long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    # patch to remove github README specific text
    long_description = (
        long_description.replace(
            "![DeFFcode](https://user-images.githubusercontent.com/34266896/211494463-a63a03d2-72a6-46bb-b40a-ab485a63674b.png#gh-dark-mode-only)",
            "",
        )
        .replace("#gh-light-mode-only", "")
        .replace("<ins>", "")
        .replace("</ins>", "")
    )
    # patch for unicodes
    long_description = long_description.replace("➶", ">>").replace("©", "(c)")
    # patch internal hyperlinks
    long_description = long_description.replace(
        "(#", "(https://github.com/abhiTronix/deffcode#"
    )

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
)
