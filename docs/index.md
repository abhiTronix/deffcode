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

<img src="assets/images/deffcode.png" alt="DeFFcode" title="Logo designed by Abhishek Thakur(@abhiTronix), under CC-BY-NC-SA 4.0 License" loading="lazy" width="87%" class="shadow2" />

> DeFFcode is a powerful High-performance Real-time **Video frames Generator** that wraps FFmpeg pipeline inside a subprocess module for generating blazingly fast video frames in python :fire:

The primary purpose of DeFFcode is to provide a cross-platform solution for fast and low-overhead decoding of a wide range of video streams into 3D [`ndarray`](https://numpy.org/doc/stable/reference/arrays.ndarray.html#the-n-dimensional-array-ndarray) frames while providing **complete control over the underlying FFmpeg pipeline** without the need to go deeper into hefty documentation and in just a few lines of python code.

DeFFcode can **extract frames in real-time with any custom specification imaginable** such as Framerate, Resolution, Hardware decoding, Complex Filters into any pixel format while giving users the complete freedom to play with any desired FFmpeg supported parameter. On top of that, DeFFcode enables **effortless and precise FFmpeg Frame Seeking** natively. 

Finally, DeFFcode APIs are designed with **simplicity, flexibility, and modularity** in mind for the best developer experience. 


&thinsp;

## Key Features

DeFFcode APIs are build on ==[**FFmpeg**][ffmpeg] - a leading multimedia framework==, that gives you the following:

- [x] Extremely exceptional real-time performance :zap: with low-memory footprints.
- [x] Flexible API with access to almost every parameter available within FFmpeg.
- [x] Fast dedicated [Hardware-Accelerated Decoding](examples/advanced/#gpu-enabled-hardware-accelerated-decoding).
- [x] Precise FFmpeg [Frame Seeking](examples/basic/#saving-keyframes-as-image) with pinpoint accuracy.
- [x] Extensive support for real-time [Complex FFmpeg Filters](examples/advanced/#generating-video-with-complex-filter-applied).
- [x] Out-of-the-box support for Computer Vision libraries like OpenCV, Pytorch, etc.
- [x] Support a wide range of media files, devices, image-sequence and network streams.
- [x] Easier to ingest streams into any pixel format that FFmpeg supports.
- [x] Lossless Transcoding support with [WriteGear](https://abhitronix.github.io/deffcode/latest/gears/writegear/introduction/).
- [x] Fewer hard dependencies, and easy to install. 
- [x] Designed modular for best developer experience.
- [x] Cross-platform and runs on Python 3.7+

&thinsp;

## Getting Started

!!! tip "In case you're run into any problems, consult our [Help](help/get_help) section."

If this is your first time using DeFFcode, head straight to the [**Installation Notes**](installation/) to install DeFFcode.

The default function of DeFFcode's [**FFdecoder API**](reference/ffdecoder/#ffdecoder-api) is to generate 24-bit RGB (3D [`ndarray`](https://numpy.org/doc/stable/reference/arrays.ndarray.html#the-n-dimensional-array-ndarray)) frames from the given source:

```py
# import the necessary packages
from deffcode import FFdecoder

# formulate the decoder with suitable source(for e.g. foo.mp4)
decoder = FFdecoder("foo.mp4").formulate()

# grab RGB24(default) 3D frames from decoder
for frame in decoder.generateFrame():
    # lets print its shape
    print(frame.shape)

# print metadata as `json.dump`
print(decoder.metadata)

# terminate the decoder
decoder.terminate()
```

**For more in-depth usage, kindly refer our [Basic Recipes :pie:](examples/basic) and [Advanced Recipes :microscope:](examples/advanced)**

&thinsp;

## Contributions

> Contributions are welcome, and greatly appreciated!  

Please read our [**Contribution Guidelines**](contribution/) for more details.

&thinsp;

## Community Channel

If you've come up with some new idea, or looking for the fastest way troubleshoot your problems. Please checkout our [**Gitter community channel ???**][gitter]

&thinsp; 

## Become a Stargazer

You can be a [**Stargazer** :star2:{ .heart }][stargazer] by starring us on Github, it helps us a lot and you're making it easier for others to find & trust this library. Thanks!

&thinsp;

## Donations

> DeFFcode is free and open source and will always remain so. :heart:{ .heart }

It is something I am doing with my own free time. If you would like to say thanks, please feel free to make a donation:

<script type='text/javascript' src='https://ko-fi.com/widgets/widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('Support Me on Ko-fi', '#eba100', 'W7W8WTYO');kofiwidget2.draw();</script> 

&thinsp;

<!--
External URLs
-->

[gitter]: https://gitter.im/deffcode-python/community
[stargazer]: https://github.com/abhiTronix/deffcode/stargazers
[ffmpeg]:https://www.ffmpeg.org/
