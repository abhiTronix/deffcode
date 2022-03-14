<!--
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
-->

# Release Notes

## v0.1.0 (2021-03-07)

??? tip "New Features"
    - [x] **:tada: Open-Sourced DeFFcode under the Apache 2.0 License.**
    - [x] **Added new Classes(APIs):**
        * FFdecoder: Performant Real-time **Video frames Generator** for generating blazingly fast video frames(RGB ndarray by default).
        * Sourcer: Extracts source video metadata _(bitrate, resolution, framerate, nframes etc.)_ using its subprocess FFmpeg output.
    - [x] **Added new Helper functions:**
        * ffhelper: Backend FFmpeg Wrapper that handles all subprocess transactions and gather data.
        * utils: Handles all additional Utilizes required for functioning of DeFFcode.
    - [x] **First PyPi Release:**
        * Released DeFFcode to Python Package Index (PyPI)
        * Added `setup.py` and related metadata.
        * Added `version.py`
    - [x] **Docs:** 
        * Added abstract and related information in README.md
        * Added installation instructions.
        * Added preliminary usage examples.
    - [x] **Maintenance:**
        * Added LICENSE.
        * Added `.gitignore`

??? success "Updates/Improvements"  
    - [x] **Maintenance:**
        * Bumped version to `0.1.0`
        * Updated LICENSE notice to add vidgear code usage notice.

??? danger "Breaking Updates/Changes"
    - [ ] **Fixed support for Python-3.7 and above legacies only.**

??? bug "Bug-fixes"
    - [x] Docs:
        * Fixed hyperlinks in README.
        * Fixed indentation and spacing.
        * Fixed typos and updated context.
        * Removed dead code.

&nbsp; 

&nbsp; 
