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

<div align="center">
  
  ![DeFFcode](docs/overrides/assets/images/deffcode.png#gh-light-mode-only)
  ![DeFFcode](docs/overrides/assets/images/deffcode-dark.png#gh-dark-mode-only)

</div>

<div align="center">

[![Build Status][github-cli]][github-flow] [![Codecov branch][codecov]][code]  [![Azure DevOps builds (branch)][azure-badge]][azure-pipeline]

[![Glitter chat][gitter-bagde]][gitter] [![Build Status][appveyor]][app] [![PyPi version][pypi-badge]][pypi] 

[![Code Style][black-badge]][black]


----

[Releases][release]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Recipes][recipes]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Documentation][docs]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Installation][installation-notes]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[License](#copyright)

----

</div>

<div align="center">

DeFFcode - A cross-platform **High-performance Video Frames Decoder** that executes <br>[**FFmpeg**][ffmpeg] pipeline inside a subprocess pipe for generating real-time, low-overhead, <br>lightning fast video frames with robust error-handling <br>in just a few lines of python code ⚡

</div>

&thinsp;

DeFFcode APIs **supports a wide-ranging media stream** as input source such as live USB/Virtual/IP camera feeds, regular multimedia files, grabbing devices, image sequences, network URL schemes _(such as HTTP(s), RTP/RSTP, etc.)_, so on and so forth. 

DeFFcode APIs gains an edge over other FFmpeg Wrappers by providing complete control over the underline pipeline including **access to almost any FFmpeg specification thinkable** such as framerate, resolution, hardware decoder(s), complex filter(s), and pixel format(s) that are readily supported by all well known Computer Vision libraries.

Furthermore, DeFFcode **maintains the same standard [OpenCV-Python][opencv-py] _(Python API for OpenCV)_ coding syntax** for every API, thereby making it even easier to learn and faster to code these APIs in your python applications without the need to dig into tedious FFmpeg documentation. 

&nbsp;

## Key features of DeFFcode

Here are some key features that stand out:

- High-performance, low-overhead, lightning fast video frames decoding.
- Supports a wide range of live camera feeds, multimedia files, grabbing devices, network URL schemes, etc.
- Flexible API with access to almost any FFmpeg specification thinkable.
- Effortless metadata extraction from multimedia streams available in the given source.
- Curated list of well-documented recipes from [**Basic**][basic-recipes] to [**Advanced**][advanced-recipes] skill levels.
- Out-of-the-box support for all well known Computer Vision libraries.
- Support easy dedicated [**Hardware-Accelerated Decoding**][hw-decoding-recipe].
- Precise FFmpeg [**Frame Seeking**][frame-seek-recipe] with pinpoint accuracy.
- Extensive support for real-time [**Complex Filters**][complex-filters-recipe].
- Cross-platform, runs on Python 3.7+, and easy to install. 

<!--
- [x] Lossless Transcoding support with [WriteGear](https://abhitronix.github.io/deffcode/latest/gears/writegear/introduction/). #TODO
-->

&nbsp;

&nbsp;

## Getting Started

---

**📚 Documentation: https://abhitronix.github.io/deffcode**

---

### Installation:

If this is your first time using DeFFcode, head straight to the **[Installation Notes][installation-notes] to install DeFFcode on your machine**.

<br>

### Recipes a.k.a Examples:

Once you have DeFFcode installed, checkout our **Well-Documented [Recipes 🍱][basic-recipes] for usage examples**:

- [**Basic Recipes 🍰**][basic-recipes]: Recipes for beginners of any skill level to get started.
- [**Advanced Recipes 🥐**][advanced-recipes]: Recipes to take your skills to the next level.

> **Note** In case you're run into any problems, consult our [Help section][help].

<br>

### API in a nutshell:

As a user, you just have to remember only two DeFFcode APIs, namely:

#### A. FFdecoder API 

The primary function of [**FFdecoder API**][ffdecoder-api] is to **generate 24-bit RGB video frames** from the given source:

> **Note** See [API Reference][ffdecoder-api] for more in-depth information.

```py
# import the necessary packages
from deffcode import FFdecoder

# formulate the decoder with suitable source
decoder = FFdecoder("https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/big_buck_bunny_720p_1mb.mp4").formulate()

# grab RGB24(default) 3D frames from decoder
for frame in decoder.generateFrame():
    
    # lets print its shape
    print(frame.shape) # (720, 1280, 3)

# terminate the decoder
decoder.terminate()
```

#### B. Sourcer API 

The primary function of [**Sourcer API**][sourcer-api] is to **gather information from all multimedia streams available** in the given source:

```python
 # import the necessary packages
 from deffcode import Sourcer

 # initialize and formulate the decoder using suitable source
 sourcer = Sourcer("https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/big_buck_bunny_720p_1mb.mp4").probe_stream()

 # print metadata as `json.dump`
 print(sourcer.retrieve_metadata(pretty_json=True))

```

<details>
  <summary><b>The resultant Terminal Output will look something as following on Windows machine</b></summary>

  ```json
      {
        "ffmpeg_binary_path": "C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe",
        "source": "https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/big_buck_bunny_720p_1mb.mp4",
        "source_extension": ".mp4",
        "source_video_resolution": [
          1280,
          720
        ],
        "source_video_framerate": 25.0,
        "source_video_pixfmt": "yuv420p",
        "source_video_decoder": "h264",
        "source_duration_sec": 5.31,
        "approx_video_nframes": 133,
        "source_video_bitrate": "1205k",
        "source_audio_bitrate": "384k",
        "source_audio_samplerate": "48000 Hz",
        "source_has_video": true,
        "source_has_audio": true,
        "source_has_image_sequence": false,
      }
  ```
</details>


&nbsp;

&nbsp;


# Contributions

> We're happy to meet new contributors💗 

We welcome your contributions to help us improve and extend this project. If you want to get involved with VidGear development, checkout the **[Contribution Guidelines ▶️][contribute]**

We're offering support for DeFFcode on [**Gitter Community Channel**][gitter]. Come and join the conversation over there!

&nbsp;

&nbsp;

# Donations

<div align="center">
   <img src="docs/overrides/assets/images/help_us.png" alt="PiGear" width="50%" />
   <p><i>DeFFcode is free and open source and will always remain so. ❤️</i></p>
</div>

It is something I am doing with my own free time. But so much more needs to be done, and I need your help to do this. For just the price of a cup of coffee, you can make a difference 🙂

<a href='https://ko-fi.com/W7W8WTYO' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=4' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>


&nbsp;

&nbsp;

# Copyright

**Copyright © abhiTronix 2021**

This library is released under the **[Apache 2.0 License][license]**.


<!--
CI Badges
-->
[appveyor]:https://img.shields.io/appveyor/ci/abhitronix/deffcode.svg?style=for-the-badge&logo=appveyor
[codecov]:https://img.shields.io/codecov/c/gh/abhiTronix/deffcode?logo=codecov&style=for-the-badge&token=zrES4mwVKe
[github-cli]:https://img.shields.io/github/workflow/status/abhiTronix/deffcode/GitHub%20Action%20workflow%20for%20Linux?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMTAgMWE5IDkgMCAwMTkgOSA5IDkgMCAwMS05IDkgOSA5IDAgMDEtOS05IDkgOSAwIDAxOS05ek0yMyAxOWE2IDYgMCAxMTAgMTIgNiA2IDAgMDEwLTEyek0yMyAzNWE2IDYgMCAxMTAgMTIgNiA2IDAgMDEwLTEyeiIgc3Ryb2tlPSJ2YXIoLS1jb2xvci1tYXJrZXRpbmctaWNvbi1wcmltYXJ5LCAjMjA4OEZGKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48cGF0aCBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik00MSAzNWE2IDYgMCAxMTAgMTIgNiA2IDAgMDEwLTEyeiIgc3Ryb2tlPSJ2YXIoLS1jb2xvci1tYXJrZXRpbmctaWNvbi1zZWNvbmRhcnksICM3OUI4RkYpIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPjxwYXRoIGQ9Ik0yNS4wMzcgMjMuNjA3bC0zLjA3IDMuMDY1LTEuNDktMS40ODUiIHN0cm9rZT0idmFyKC0tY29sb3ItbWFya2V0aW5nLWljb24tcHJpbWFyeSwgIzIwODhGRikiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PHBhdGggY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNNDEgMTlhNiA2IDAgMTEwIDEyIDYgNiAwIDAxMC0xMnoiIHN0cm9rZT0idmFyKC0tY29sb3ItbWFya2V0aW5nLWljb24tcHJpbWFyeSwgIzIwODhGRikiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PHBhdGggZD0iTTQzLjAzNiAyMy42MDdsLTMuMDY5IDMuMDY1LTEuNDktMS40ODVNNyA2LjgxMmExIDEgMCAwMTEuNTMzLS44NDZsNS4xMTMgMy4yMmExIDEgMCAwMS0uMDA2IDEuNjk3bC01LjExMyAzLjE3QTEgMSAwIDAxNyAxMy4yMDNWNi44MTN6TTkgMTl2MTVjMCAzLjg2NiAzLjE3NyA3IDcgN2gxIiBzdHJva2U9InZhcigtLWNvbG9yLW1hcmtldGluZy1pY29uLXByaW1hcnksICMyMDg4RkYpIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPjxwYXRoIGQ9Ik0xNi45NDkgMjZhMSAxIDAgMTAwLTJ2MnpNOCAxOS4wMzVBNi45NjUgNi45NjUgMCAwMDE0Ljk2NSAyNnYtMkE0Ljk2NSA0Ljk2NSAwIDAxMTAgMTkuMDM1SDh6TTE0Ljk2NSAyNmgxLjk4NHYtMmgtMS45ODR2MnoiIGZpbGw9InZhcigtLWNvbG9yLW1hcmtldGluZy1pY29uLXByaW1hcnksICMyMDg4RkYpIi8+PHBhdGggZD0iTTI5LjA1NSAyNWg1Ljk0NCIgc3Ryb2tlPSJ2YXIoLS1jb2xvci1tYXJrZXRpbmctaWNvbi1wcmltYXJ5LCAjMjA4OEZGKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTIxIDQwYTEgMSAwIDExLS4wMDEgMi4wMDFBMSAxIDAgMDEyMSA0MHpNMjUgNDBhMSAxIDAgMTEtLjAwMSAyLjAwMUExIDEgMCAwMTI1IDQweiIgZmlsbD0idmFyKC0tY29sb3ItbWFya2V0aW5nLWljb24tc2Vjb25kYXJ5LCAjNzlCOEZGKSIvPjxwYXRoIGQ9Ik0zNC4wMDUgNDEuMDA3bC0xLjAxMy4wMzMiIHN0cm9rZT0idmFyKC0tY29sb3ItbWFya2V0aW5nLWljb24tc2Vjb25kYXJ5LCAjNzlCOEZGKSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz48L3N2Zz4=
[prs-badge]:https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABC0lEQVRYhdWVPQoCMRCFX6HY2ghaiZUXsLW0EDyBrbWtN/EUHsHTWFnYyCL4gxibVZZlZzKTnWz0QZpk5r0vIdkF/kBPAMOKeddE+CQPKoc5Yt5cTjBMdQSwDQToWgBJAn3jmhqgltapAV6E6b5U17MGGAUaUj07TficMfIBZDV6vxowBm1BP9WbSQE4o5h9IjPJmy73TEPDDxVmoZdQrQ5jRhly9Q8tgMUXkIIWn0oG4GYQfAXQzz1PGoCiQndM7b4RgJay/h7zBLT3hASgoKjamQJMreKf0gfuAGyYtXEIAKcL/Dss15iq6ohXghozLYiAMxPuACwtIT4yeQUxAaLrZwAoqGRKGk7qDSYTfYQ8LuYnAAAAAElFTkSuQmCC
[azure-badge]:https://img.shields.io/azure-devops/build/abhiuna12/942b3b13-d745-49e9-8d7d-b3918ff43ac2/3/master?logo=azure-pipelines&style=for-the-badge
[pypi-badge]:https://img.shields.io/pypi/v/deffcode.svg?style=for-the-badge&logo=pypi
[gitter-bagde]:https://img.shields.io/badge/Chat-Gitter-blueviolet.svg?style=for-the-badge&logo=gitter
[Coffee-badge]:https://abhitronix.github.io/img/deffcode/orange_img.png
[kofi-badge]:https://www.ko-fi.com/img/githubbutton_sm.svg
[black-badge]:https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge&logo=github

<!--
Internal URLs
-->
[docs]:https://abhitronix.github.io/deffcode/latest/
[release]:https://github.com/abhiTronix/deffcode/releases/latest
[recipes]:https://abhitronix.github.io/deffcode/latest/recipes/basic/
[license]:https://github.com/abhiTronix/deffcode/blob/master/LICENSE
[basic-recipes]:https://abhitronix.github.io/deffcode/latest/recipes/basic
[advanced-recipes]:https://abhitronix.github.io/deffcode/latest/recipes/advanced
[hw-decoding-recipe]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/#gpu-enabled-hardware-accelerated-decoding
[frame-seek-recipe]:https://abhitronix.github.io/deffcode/latest/recipes/basic/#saving-keyframes-as-image
[complex-filters-recipe]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/#generating-video-with-complex-filter-applied
[help]:https://abhitronix.github.io/deffcode/latest/https://abhitronix.github.io/deffcode/latest/help/get_help
[installation-notes]:https://abhitronix.github.io/deffcode/latest/installation/#installation-notes
[ffdecoder-api]:https://abhitronix.github.io/deffcode/latest/reference/ffdecoder/#ffdecoder-api
[sourcer-api]:https://abhitronix.github.io/deffcode/latest/reference/sourcer/#sourcer-api
[contribute]:https://abhitronix.github.io/deffcode/latest/contribution/

<!--
CI Apps URLs
-->
[github-flow]:https://github.com/abhiTronix/deffcode/actions/workflows/CIlinux.yml
[azure-pipeline]:https://dev.azure.com/abhiuna12/public/_build?definitionId=3
[app]:https://ci.appveyor.com/project/abhiTronix/deffcode
[code]:https://codecov.io/gh/abhiTronix/deffcode
[black]: https://github.com/psf/black

<!--
External URLs
-->
[opencv-py]:https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
[ffmpeg]:https://www.ffmpeg.org/
[pypi]:https://pypi.org/project/deffcode/
[gitter]:https://gitter.im/deffcode-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[coffee]:https://www.buymeacoffee.com/2twOXFvlA
[kofi]: https://ko-fi.com/W7W8WTYO
