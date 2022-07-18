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

> DeFFcode is a cross-platform **High-performance Video Frames Decoder** that wraps FFmpeg pipeline inside a subprocess pipe for generating real-time, low-overhead, blazingly fast video frames in python :material-rocket-launch:

DeFFcode APIs **supports a wide-ranging media stream** as input source such as USB/Virtual/IP Camera Feed, Multimedia video file, Screen Capture, Image Sequence, Network URL schemes _(such as HTTP(s), RTP/RSTP, etc.)_, so on and so forth. 

DeFFcode APIs gains an edge over other FFmpeg Wrappers by providing **complete control over the underlying pipeline with access to almost any FFmpeg specification thinkable** such as framerate, resolution, hardware decoding, complex filters, and any pixel format that is readily supported by almost all prominent Computer Vision libraries. 

DeFFcode **maintains the same standard OpenCV-Python _(Python API for OpenCV)_ coding syntax** for all of its APIs, thereby making it even easier to learn and integrate DeFFcode APIs in existing or newer applications with least amount of effort.

&thinsp;

## Key Features

DeFFcode APIs wraps ==[**FFmpeg**][ffmpeg]== to offer you some of the following key features:

- [x] High-performance, low-overhead, blazingly fast RGB video frames decoding.
- [x] Supports a wide range of Camera Feeds, Multimedia files, Image Sequences, Network URL schemes, etc.
- [x] Flexible API with access to almost any FFmpeg specification thinkable.
- [x] Effortless metadata extraction from multimedia streams available in the given source.
- [x] Fast dedicated [Hardware-Accelerated Decoding](examples/advanced/#gpu-enabled-hardware-accelerated-decoding).
- [x] Precise FFmpeg [Frame Seeking](examples/basic/#saving-keyframes-as-image) with pinpoint accuracy.
- [x] Extensive support for real-time [Complex FFmpeg Filters](examples/advanced/#generating-video-with-complex-filter-applied).
- [x] Out-of-the-box support for Computer Vision libraries like OpenCV, Pytorch, etc.
- [x] Easier to transform frames into any pixel format that FFmpeg supports.
- [x] Fewer hard dependencies, and easy to install. 
- [x] Cross-platform and runs on Python 3.7+

<!--
- [x] Lossless Transcoding support with [WriteGear](https://abhitronix.github.io/deffcode/latest/gears/writegear/introduction/). #TODO
-->

&thinsp;

## Installation

If this is your first time using DeFFcode, head straight to the [**Installation Notes**](installation/) to install DeFFcode.

&thinsp;


## Quickstart

!!! tip "In case you're run into any problems, consult our [Help](help/get_help) section."

### Usage Examples

Once you have DeFFcode installed, Refer our **Well-Documented Recipes :material-pot-steam:** for examples:

- [x] [**Basic Recipes :pie:**](examples/basic): Accessible to Python programmers of all skill levels.
- [x] [**Advanced Recipes :croissant:**](examples/advanced): Involve advanced techniques that may not be “beginner friendly”.


### API in a nutshell

As a user, you just have to remember only two DeFFcode APIs:

!!! info "See [API Reference](reference/ffdecoder/#ffdecoder-api) for more in-depth information."

#### A. FFdecoder API 

The primary function of [FFdecoder API](reference/ffdecoder/#ffdecoder-api) is to generate 24-bit RGB video frames from the given source:

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

The primary function of [Sourcer API](reference/sourcer/#sourcer-api) is to gathers information from all multimedia streams available in the given input source:

```python
 # import the necessary packages
 from deffcode import Sourcer

 # initialize and formulate the decoder using suitable source
 sourcer = Sourcer("https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/big_buck_bunny_720p_1mb.mp4").probe_stream()

 # print metadata as `json.dump`
 print(sourcer.retrieve_metadata(pretty_json=True))

```

??? abstract "The resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"
     
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


&thinsp;


## Contributions

> Contributions are welcome, and greatly appreciated!  

Please read our [**Contribution Guidelines**](contribution/) for more details.

&thinsp;

## Community Channel

If you've come up with some new idea, or looking for the fastest way troubleshoot your problems. Please checkout our [**Gitter community channel ➶**][gitter]

&thinsp; 

## Become a Stargazer

You can be a  [**Stargazer** :star2:{ .heart }][stargazer]  by starring us on Github, it helps us a lot and you're making it easier for others to find & trust this library. Thanks!

&thinsp;

## Donations

> DeFFcode is free and open source and will always remain so. :heart:{ .heart }

It is something I am doing with my own free time. But so much more needs to be done, and I need your help to do this. For just the price of a cup of coffee, you can make a difference :slight_smile:

<script type='text/javascript' src='https://ko-fi.com/widgets/widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('Support Me on Ko-fi', '#eba100', 'W7W8WTYO');kofiwidget2.draw();</script> 


&thinsp;

<!--
External URLs
-->

[gitter]: https://gitter.im/deffcode-python/community
[stargazer]: https://github.com/abhiTronix/deffcode/stargazers
[ffmpeg]:https://www.ffmpeg.org/
