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

DeFFcode - A cross-platform **High-performance Video Frames Decoder** that flexibly executes <br>FFmpeg pipeline inside a subprocess pipe for generating real-time, low-overhead, <br>lightning fast video frames with robust error-handling <br>in just a few lines of python code ⚡

</div>

&thinsp;

**<ins>Highly Adaptive</ins> -** _DeFFcode APIs implements a **standalone highly-extensible wrapper around [FFmpeg][ffmpeg]** multimedia framework. These APIs **supports a wide-ranging media streams as input** source such as [live USB/Virtual/IP camera feeds][capturing-and-previewing-frames-from-a-webcam], [regular multimedia files][capturing-rgb-frames-from-a-video-file], [screen recordings][capturing-and-previewing-frames-from-your-desktop], [image sequences][decoding-image-sequences], [network URL schemes][decoding-network-streams] (such as HTTP(s), RTP/RSTP, etc.), so on and so forth._

**<ins>Highly Flexible</ins> -** _DeFFcode APIs gains an edge over other FFmpeg Wrappers by providing **complete control over the underline pipeline** including **access to almost any FFmpeg specification thinkable** such as specifying framerate, resolution, hardware decoder(s), filtergraph(s), and pixel-format(s) that are readily **supported by all well known Computer Vision libraries**._

**<ins>Highly Convenient</ins> -** _FFmpeg has a steep learning curve especially for users unfamiliar with a command line interface. DeFFcode helps users by maintaining the **same standard [OpenCV-Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) (Python API for OpenCV) coding syntax for its APIs**, thereby making it even **easier to learn, create, and develop FFmpeg based apps** in Python._

&nbsp;

### Key features of DeFFcode

Here are some key features that stand out:

- High-performance, low-overhead video frames decoding with robust error-handling.
- Flexible API with access to almost any FFmpeg specification thinkable.
- Supports a wide-range of media streams/devices/protocols as input source.
- Curated list of well-documented recipes ranging from [**Basic**][basic-recipes] to [**Advanced**][advanced-recipes] skill levels.
- Easy to code **Real-time [Simple][transcoding-live-simple-filtergraphs] & [Complex][transcoding-live-complex-filtergraphs] Filtergraphs**. _(Yes, You read it correctly "Real-time"!)_
- Lightning fast dedicated **GPU-Accelerated Video [Decoding][hardware-accelerated-video-decoding] & [Transcoding][hardware-accelerated-video-transcoding]**.
- Enables precise FFmpeg [**Key-frame Seeking**][extracting-key-frames-as-png-image] with pinpoint accuracy.
- Effortless [**Metadata Extraction**][extracting-video-metadata] from all streams available in the source.
- Maintains the standard easy to learn [**OpenCV-Python**](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) coding syntax.
- Out-of-the-box support for all prominent Computer Vision libraries.
- Cross-platform, runs on Python 3.7+, and easy to install.  

<!--
- [x] Lossless Transcoding support with [WriteGear](https://abhitronix.github.io/deffcode/latest/gears/writegear/introduction/). #TODO
-->

&nbsp;

&nbsp;

# Getting Started

---

**📚 Documentation: https://abhitronix.github.io/deffcode**

---

## Installation:

If this is your first time using DeFFcode, head straight to the **[Installation Notes][installation-notes] to install DeFFcode on your machine**.

<br>

<br>

### Recipes _a.k.a_ Examples:

Once you have DeFFcode installed, checkout our Well-Documented **[Recipes 🍱][basic-recipes] for usage examples**:

> **Note** In case you're run into any problems, consult our [Help section][help].

### A. [**Basic Recipes 🍰**][basic-recipes]: _Recipes for beginners of any skill level to get started._

<br>
<div align="center">
  <a href="https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames-simplegraphs/#transcoding-trimmed-and-reversed-video"><img src="docs/overrides/assets/gifs/bigbuckbunny_reversed.gif" alt="Big Buck Bunny Reversed" title="Click to view source code" width="70%" /> </a>
  <br>
  <sub><i>Big Buck Bunny Reversed using Live Simple Filtergraph</i></sub>
</div>

<br>

<details open>
  <summary><b>Basic Decoding Recipes</b></summary>

- [Capturing RGB frames from a video file][capturing-rgb-frames-from-a-video-file]
- [Capturing and Previewing BGR frames from a video file][capturing-and-previewing-bgr-frames-from-a-video-file] _(OpenCV Support)_
- [Playing with any other FFmpeg pixel formats][capturing-and-previewing-bgr-frames-from-a-video-file]
- [Capturing and Previewing frames from a Webcam][capturing-and-previewing-frames-from-a-webcam]
- [Capturing and Previewing frames from your Desktop][capturing-and-previewing-frames-from-your-desktop] _(Screen Recording)_
- [Capturing and Previewing frames from a HTTPs Stream][capturing-and-previewing-frames-from-a-https-stream]
- [Capturing and Previewing frames from a RTSP/RTP Stream][capturing-and-previewing-frames-from-a-rtsprtp-stream]
- [Capturing and Previewing frames from Sequence of images][capturing-and-previewing-frames-from-sequence-of-images]
- [Capturing and Previewing frames from Single looping image][capturing-and-previewing-frames-from-single-looping-image]

</details>

<details open>
  <summary><b>Basic Transcoding Recipes</b></summary>

- [Transcoding video using OpenCV VideoWriter API][transcoding-video-using-opencv-videowriter-api]
- [Transcoding lossless video using WriteGear API][transcoding-lossless-video-using-writegear-api]
- [Transcoding Trimmed and Reversed video][transcoding-trimmed-and-reversed-video]
- [Transcoding Cropped video][transcoding-cropped-video]
- [Transcoding Rotated video (with `rotate` filter)][transcoding-rotated-video-with-rotate-filter]
- [Transcoding Rotated video (with `transpose` filter)][transcoding-rotated-video-with-transpose-filter]   
- [Transcoding Horizontally flipped and Scaled video][transcoding-horizontally-flipped-and-scaled-video]
- [Extracting Key-frames as PNG image][extracting-key-frames-as-png-image]
- [Generating Thumbnail with a Fancy filter][generating-thumbnail-with-a-fancy-filter]
</details>

<details open>
  <summary><b>Basic Metadata Recipes</b></summary>

- [Extracting video metadata using Sourcer API][extracting-video-metadata-using-sourcer-api]
- [Extracting video metadata using FFdecoder API][extracting-video-metadata-using-ffdecoder-api]

</details>

<br>


### B. [**Advanced Recipes 🥐**][advanced-recipes]: _Recipes to take your skills to the next level._

<br>
<p align="center">
  <a href="https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-mandelbrot-test-pattern-with-vectorscope-waveforms"><img src="docs/overrides/assets/gifs/mandelbrot_vectorscope_waveforms.gif" alt="mandelbrot test pattern" title="Click to view source code" width="70%" /></a>
  <br>
  <sub><i>Live Mandelbrot pattern with a Vectorscope & two Waveforms</i></sub>
</p>

<br>

<details open>
  <summary><b>Advanced Decoding Recipes</b></summary>

- [Generate and Decode frames from Sierpinski pattern][generate-and-decode-frames-from-sierpinski-pattern]
- [Generate and Decode frames from Test Source pattern][generate-and-decode-frames-from-test-source-pattern]
- [Generate and Decode frames from Gradients with custom Text effect][generate-and-decode-frames-from-gradients-with-custom-text-effect]
- [Generate and Decode frames from Mandelbrot test pattern with vectorscope & waveforms][generate-and-decode-frames-from-mandelbrot-test-pattern-with-vectorscope-waveforms]
- [Generate and Decode frames from Game of Life Visualization][generate-and-decode-frames-from-game-of-life-visualization]
- [GPU-accelerated Hardware-based Video Decoding][gpu-accelerated-hardware-based-video-decoding]

</details>

<details open>
  <summary><b>Advanced Transcoding Recipes</b></summary>

- [Transcoding video with Live Custom watermark image overlay][transcoding-video-with-live-custom-watermark-image-overlay]
- [Transcoding video from sequence of Images with additional filtering][transcoding-video-from-sequence-of-images-with-additional-filtering]
- [Transcoding video art with YUV Bitplane Visualization][transcoding-video-art-with-yuv-bitplane-visualization]
- [Transcoding video art with Jetcolor effect][transcoding-video-art-with-jetcolor-effect] 
- [Transcoding video art with Ghosting effect][transcoding-video-art-with-ghosting-effect]
- [Transcoding video art with Pixelation effect][transcoding-video-art-with-pixelation-effect]
- [GPU-accelerated Hardware-based Video Transcoding with WriteGear API][gpu-accelerated-hardware-based-video-transcoding-with-writegear-api]

</details>

<details open>
  <summary><b>Advanced Metadata Recipes</b></summary>

- [Added new attributes to metadata in FFdecoder API][added-new-attributes-to-metadata-in-ffdecoder-api]
- [Overriding source video metadata in FFdecoder API][overriding-source-video-metadata-in-ffdecoder-api]

</details>

<br>

<br>

## API in a nutshell:

As a user, you just have to remember only two DeFFcode APIs, namely:

### A. FFdecoder API 

The primary function of [**FFdecoder API**][ffdecoder-api] is to **decode 24-bit RGB video frames** from the given source:

> **Note** See [API Reference][ffdecoder-api] for more in-depth information.

```py
# import the necessary packages
from deffcode import FFdecoder

# formulate the decoder with suitable source
decoder = FFdecoder("https://abhitronix.github.io/html/Big_Buck_Bunny_1080_10s_1MB.mp4").formulate()

# grab RGB24(default) 3D frames from decoder
for frame in decoder.generateFrame():
    
    # lets print its shape
    print(frame.shape) # (1080, 1920, 3)

# terminate the decoder
decoder.terminate()
```

### B. Sourcer API 

The primary function of [**Sourcer API**][sourcer-api] is to **gather metadata information from all multimedia streams available** in the given source:

```python
# import the necessary packages
from deffcode import Sourcer

# initialize and formulate the decoder using suitable source
sourcer = Sourcer("https://abhitronix.github.io/html/Big_Buck_Bunny_1080_10s_1MB.mp4").probe_stream()

# print metadata as `json.dump`
print(sourcer.retrieve_metadata(pretty_json=True))
```

<details>
  <summary><b>The resultant Terminal Output will look something as following on Windows machine</b></summary>

  ```json
      {
        "ffmpeg_binary_path": "C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe",
        "source": "https://abhitronix.github.io/html/Big_Buck_Bunny_1080_10s_1MB.mp4",
        "source_extension": ".mp4",
        "source_video_resolution": [
          1920,
          1080
        ],
        "source_video_framerate": 60.0,
        "source_video_pixfmt": "yuv420p",
        "source_video_decoder": "h264",
        "source_duration_sec": 10.0,
        "approx_video_nframes": 600,
        "source_video_bitrate": "832k",
        "source_audio_bitrate": "",
        "source_audio_samplerate": "",
        "source_has_video": true,
        "source_has_audio": false,
        "source_has_image_sequence": false
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
   <img src="docs/overrides/assets/images/help_us.png" alt="Donation" width="50%" />
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
[help]:https://abhitronix.github.io/deffcode/latest/https://abhitronix.github.io/deffcode/latest/help/get_help
[installation-notes]:https://abhitronix.github.io/deffcode/latest/installation/#installation-notes
[ffdecoder-api]:https://abhitronix.github.io/deffcode/latest/reference/ffdecoder/#ffdecoder-api
[sourcer-api]:https://abhitronix.github.io/deffcode/latest/reference/sourcer/#sourcer-api
[contribute]:https://abhitronix.github.io/deffcode/latest/contribution/

<!--
Basic Recipes
-->
[basic-recipes]:https://abhitronix.github.io/deffcode/latest/recipes/basic/
[decoding-video-files]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-video-files/#decoding-video-files
[decoding-live-feed-devices]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-live-feed-devices/#decoding-live-feed-devices
[decoding-network-streams]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-network-streams/#decoding-network-streams
[decoding-image-sequences]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-image-sequences/#decoding-image-sequences
[transcode-live-frames]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames/
[transcoding-live-simple-filtergraphs]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames-simplegraphs/#transcoding-live-simple-filtergraphs
[saving-key-frames-as-image]:https://abhitronix.github.io/deffcode/latest/recipes/basic/save-keyframe-image/#saving-key-frames-as-image
[extracting-video-metadata]:https://abhitronix.github.io/deffcode/latest/recipes/basic/extract-video-metadata/#extracting-video-metadata

[capturing-rgb-frames-from-a-video-file]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-video-files/#capturing-rgb-frames-from-a-video-file
[capturing-and-previewing-bgr-frames-from-a-video-file]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-video-files/#capturing-and-previewing-bgr-frames-from-a-video-file
[capturing-and-previewing-bgr-frames-from-a-video-file]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-video-files/#capturing-and-previewing-bgr-frames-from-a-video-file
[capturing-and-previewing-frames-from-a-webcam]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-live-feed-devices/#capturing-and-previewing-frames-from-a-webcam
[capturing-and-previewing-frames-from-your-desktop]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-live-feed-devices/#capturing-and-previewing-frames-from-your-desktop
[capturing-and-previewing-frames-from-a-https-stream]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-network-streams/#capturing-and-previewing-frames-from-a-https-stream
[capturing-and-previewing-frames-from-a-rtsprtp-stream]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-network-streams/#capturing-and-previewing-frames-from-a-rtsprtp-stream
[capturing-and-previewing-frames-from-sequence-of-images]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-image-sequences/#capturing-and-previewing-frames-from-sequence-of-images
[capturing-and-previewing-frames-from-single-looping-image]:https://abhitronix.github.io/deffcode/latest/recipes/basic/decode-image-sequences/#capturing-and-previewing-frames-from-single-looping-image
[transcoding-video-using-opencv-videowriter-api]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames/#transcoding-video-using-opencv-videowriter-api
[transcoding-lossless-video-using-writegear-api]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames/#transcoding-lossless-video-using-writegear-api
[transcoding-trimmed-and-reversed-video]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames-simplegraphs/#transcoding-trimmed-and-reversed-video
[transcoding-cropped-video]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames-simplegraphs/#transcoding-cropped-video
[transcoding-rotated-video-with-rotate-filter]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames-simplegraphs/#transcoding-rotated-video-with-rotate-filter
[transcoding-rotated-video-with-transpose-filter]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames-simplegraphs/#transcoding-rotated-video-with-transpose-filter
[transcoding-horizontally-flipped-and-scaled-video]:https://abhitronix.github.io/deffcode/latest/recipes/basic/transcode-live-frames-simplegraphs/#transcoding-horizontally-flipped-and-scaled-video
[extracting-key-frames-as-png-image]:https://abhitronix.github.io/deffcode/latest/recipes/basic/save-keyframe-image/#extracting-key-frames-as-png-image
[generating-thumbnail-with-a-fancy-filter]:https://abhitronix.github.io/deffcode/latest/recipes/basic/save-keyframe-image/#generating-thumbnail-with-a-fancy-filter
[extracting-video-metadata-using-sourcer-api]:https://abhitronix.github.io/deffcode/latest/recipes/basic/extract-video-metadata/#extracting-video-metadata-using-sourcer-api
[extracting-video-metadata-using-ffdecoder-api]:https://abhitronix.github.io/deffcode/latest/recipes/basic/extract-video-metadata/#extracting-video-metadata-using-ffdecoder-api

<!--
Advanced Recipes
-->
[advanced-recipes]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/
[decoding-live-virtual-sources]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-live-virtual-sources/#decoding-live-virtual-sources
[hardware-accelerated-video-decoding]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-hw-acceleration/#hardware-accelerated-video-decoding
[transcoding-live-complex-filtergraphs]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-live-frames-complexgraphs/#transcoding-live-complex-filtergraphs
[transcoding-video-art-with-filtergraphs]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-art-filtergraphs/#transcoding-video-art-with-filtergraphs
[hardware-accelerated-video-transcoding]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-hw-acceleration/#hardware-accelerated-video-transcoding
[updating-video-metadata]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/update-metadata/#updating-video-metadata


[generate-and-decode-frames-from-sierpinski-pattern]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-sierpinski-pattern
[generate-and-decode-frames-from-test-source-pattern]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-test-source-pattern
[generate-and-decode-frames-from-gradients-with-custom-text-effect]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-gradients-with-custom-text-effect
[generate-and-decode-frames-from-mandelbrot-test-pattern-with-vectorscope-waveforms]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-mandelbrot-test-pattern-with-vectorscope-waveforms
[generate-and-decode-frames-from-game-of-life-visualization]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-game-of-life-visualization
[gpu-accelerated-hardware-based-video-decoding]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/decode-hw-acceleration/#gpu-accelerated-hardware-based-video-decoding
[transcoding-video-with-live-custom-watermark-image-overlay]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-live-frames-complexgraphs/#transcoding-video-with-live-custom-watermark-image-overlay
[transcoding-video-from-sequence-of-images-with-additional-filtering]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-live-frames-complexgraphs/#transcoding-video-from-sequence-of-images-with-additional-filtering
[transcoding-video-art-with-jetcolor-effect]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-art-filtergraphs/#transcoding-video-art-with-jetcolor-effect
[transcoding-video-art-with-yuv-bitplane-visualization]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-art-filtergraphs/#transcoding-video-art-with-yuv-bitplane-visualization
[transcoding-video-art-with-ghosting-effect]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-art-filtergraphs/#transcoding-video-art-with-ghosting-effect
[transcoding-video-art-with-pixelation-effect]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-art-filtergraphs/#transcoding-video-art-with-pixelation-effect
[gpu-accelerated-hardware-based-video-transcoding-with-writegear-api]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/transcode-hw-acceleration/#gpu-accelerated-hardware-based-video-transcoding-with-writegear-api
[added-new-attributes-to-metadata-in-ffdecoder-api]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/update-metadata/#added-new-attributes-to-metadata-in-ffdecoder-api
[overriding-source-video-metadata-in-ffdecoder-api]:https://abhitronix.github.io/deffcode/latest/recipes/advanced/update-metadata/#overriding-source-video-metadata-in-ffdecoder-api

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
