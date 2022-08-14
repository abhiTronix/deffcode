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

# Introduction

![DeFFcode](assets/images/deffcode.png#only-light){ loading=lazy }
![DeFFcode](assets/images/deffcode-dark.png#only-dark){ loading=lazy }

<center>A cross-platform **:fontawesome-solid-gauge-high: High-performance Video Frames Decoder** that flexibly executes FFmpeg pipeline inside a subprocess pipe for generating real-time, low-overhead, <br>lightning fast video frames with robust error-handling <br>in just a few lines of python code :fontawesome-solid-fire-flame-curved:</center>

<div class="spacer"></div>

**==Highly Adaptive== -** DeFFcode APIs implements a **standalone highly-extensible wrapper around [FFmpeg][ffmpeg]** multimedia framework. These APIs **supports a wide-ranging media streams as input** source such as live USB/Virtual/IP camera feeds, regular multimedia files, screen recordings, image sequences, network protocols _(such as HTTP(s), RTP/RSTP, etc.)_, so on and so forth.

**==Highly Flexible== -** DeFFcode APIs gains an edge over other Wrappers by providing **complete control over the underline pipeline** including **access to almost any FFmpeg specification thinkable** such as specifying framerate, resolution, hardware decoder(s), filtergraph(s), and pixel-format(s) that are readily **supported by all well known Computer Vision libraries**.

**==Highly Convenient== -**  FFmpeg has a steep learning curve especially for users unfamiliar with a command line interface. DeFFcode helps users by keeping the **same [OpenCV-Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) _(Python API for OpenCV)_ coding syntax for its APIs**, thereby making it even **easier to learn, create, and develop FFmpeg based apps** in Python.

&thinsp;

## Key features of DeFFcode

Here are some key features that stand out:

- [x] High-performance, low-overhead video frames decoding with robust error-handling.
- [x] Flexible API with access to almost any FFmpeg specification thinkable.
- [x] Supports a wide-range of media streams/devices/protocols as input source. 
- [x] Curated list of well-documented recipes ranging from [**Basic**](recipes/basic/) to [**Advanced**](recipes/advanced/) skill levels.
- [x] Memory efficient **Live [Simple](recipes/basic/transcode-live-frames-simplegraphs/#transcoding-live-simple-filtergraphs) & [Complex](recipes/advanced/transcode-live-frames-complexgraphs/#transcoding-live-complex-filtergraphs) Filtergraphs**. _(Yes, You read it correctly "Live"!)_
- [x] Lightning fast dedicated **:fontawesome-solid-microchip: GPU-Accelerated Video [Decoding](recipes/advanced/decode-hw-acceleration/#hardware-accelerated-video-decoding) & [Transcoding](recipes/advanced/transcode-hw-acceleration/#hardware-accelerated-video-transcoding)**.
- [x] Enables precise FFmpeg [**Frame Seeking**](recipes/basic/save-keyframe-image/#extracting-key-frames-as-png-image) with pinpoint accuracy.
- [x] Effortless [**Metadata Extraction**](recipes/basic/extract-video-metadata/#extracting-video-metadata) from all streams available in the source.
- [x] Maintains the standard easy to learn [**OpenCV-Python**](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) coding syntax.
- [x] Out-of-the-box support for all prominent Computer Vision libraries.
- [x] Cross-platform, runs on Python 3.7+, and easy to install. 

??? question "Still missing a key feature in DeFFcode?"

      Please review [**DeFFcode's Roadmap**](https://github.com/abhiTronix/deffcode/issues/21#issue-1309685018). If you still can't find the desired feature there, then you can request one simply by **Commenting :speaking_head:** or **Upvoting an existing comment :thumbsup:** [on that issue](https://github.com/abhiTronix/deffcode/issues/21).


<!--
- [x] Lossless Transcoding support with [WriteGear](gears/writegear/introduction/). #TODO
-->


&nbsp;


## Getting Started

<div class="spacer"></div>

!!! tip "In case you're run into any problems, consult our [Help section](help/get_help)."

### :material-notebook-plus: Installation Notes

If this is your first time using DeFFcode, head straight to the **[Installation Notes](installation/#installation-notes) to install DeFFcode on your machine**.

<div class="spacer"></div>

### :material-pot-steam: Recipes a.k.a Examples


Once you have DeFFcode installed, checkout our **Well-Documented [Recipes :material-pot-steam:](recipes/basic) for usage examples**:

??? question "How to Begin?"
      
      If you’re just starting, check out the Beginner [**Basic Recipes :cake:**](recipes/basic) and as your confidence grows, move up to [**Advanced Recipes :croissant:**](recipes/advanced). 

- [x] [**Basic Recipes :cake:**](recipes/basic): Recipes for beginners of any skill level to get started.
- [x] [**Advanced Recipes :croissant:**](recipes/advanced): Recipes to take your skills to the next level.

<div class="spacer"></div>

### :material-api: API in a nutshell

As a user, you just have to remember only two DeFFcode APIs, namely:

!!! info "See [API Reference](reference/ffdecoder/#ffdecoder-api) for more in-depth information."

<div class="spacer"></div>

#### A. FFdecoder API 

The primary function of [**FFdecoder API**](reference/ffdecoder/#ffdecoder-api) is to **decode 24-bit RGB video frames** from the given source:

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

#### B. Sourcer API 

The primary function of [**Sourcer API**](reference/sourcer/#sourcer-api) is to **gather information from all multimedia streams available** in the given source:

```python
# import the necessary packages
from deffcode import Sourcer

# initialize and formulate the decoder using suitable source
sourcer = Sourcer("https://abhitronix.github.io/html/Big_Buck_Bunny_1080_10s_1MB.mp4").probe_stream()

# print metadata as `json.dump`
print(sourcer.retrieve_metadata(pretty_json=True))
```

??? abstract "The resultant Terminal Output will look something as following on :fontawesome-brands-windows: Windows machine:"
     
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


&nbsp;

## Contribution Guidelines

> Contributions are welcome, and greatly appreciated!  

Please read our [**Contribution Guidelines**](contribution/) for more details.

&nbsp;

## Community Channel

If you've come up with some new idea, or looking for the fastest way troubleshoot your problems. Please checkout our [**Gitter community channel ➶**][gitter]

&nbsp;

## Become a Stargazer

You can be a  [**Stargazer** :star2:{ .heart }][stargazer]  by starring us on Github, it helps us a lot and you're making it easier for others to find & trust this library. Thanks!

&nbsp;

## Donations

> DeFFcode is free and open source and will always remain so. :heart:{ .heart }

It is something I am doing with my own free time. But so much more needs to be done, and I need your help to do this. For just the price of a cup of coffee, you can make a difference :slight_smile:

<script type='text/javascript' src='https://ko-fi.com/widgets/widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('Support Me on Ko-fi', '#eba100', 'W7W8WTYO');kofiwidget2.draw();</script> 

&nbsp;

## Citation

Here is a Bibtex entry you can use to cite this project in a publication:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6984364.svg)](https://doi.org/10.5281/zenodo.6984364)

```BibTeX
@software{deffcode,
  author       = {Abhishek Thakur},
  title        = {abhiTronix/deffcode: v0.2.3},
  month        = aug,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {v0.2.3},
  doi          = {10.5281/zenodo.6984364},
  url          = {https://doi.org/10.5281/zenodo.6984364}
}
```

&nbsp;


<!--
External URLs
-->

[gitter]: https://gitter.im/deffcode-python/community
[stargazer]: https://github.com/abhiTronix/deffcode/stargazers
[ffmpeg]:https://www.ffmpeg.org/
