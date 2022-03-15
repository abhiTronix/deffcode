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

# FFdecoder API

FFdecoder API is a powerful real-time **Video-frames [Generator](https://wiki.python.org/moin/Generators)** built upon [FFmpeg](https://ffmpeg.org/), that keeps on generating 3D [24-bit RGB](https://en.wikipedia.org/wiki/List_of_monochrome_and_RGB_color_formats#24-bit_RGB)(default) NumPy's [`ndarray`](https://numpy.org/doc/stable/reference/arrays.ndarray.html#the-n-dimensional-array-ndarray) frames from its pipeline with low-memory overhead continuously.

FFdecoder supports a **wide range of handle/control media stream** such as any Video Input devices like USB Cameras, Multimedia video file format, Screen Captures, Image Sequences, plus any network stream URL _(such as http(s), rtp, rstp, rtmp, mms, etc.)_.

FFdecoder **wraps FFmpeg pipeline inside a [`subprocess`](https://docs.python.org/3/library/subprocess.html)** that run as completely independent entities and executes the pipeline concurrently with original process, extracting dataframes(in bytes) into NumPy's buffer(as a 1D array) from its `stdout` output. These dataframes are then converted into 3D NumPy's `ndarray` frames that are supported by almost all prominent Computer Vision libraries like OpenCV, Pytorch, dlib ,etc. and can be easily employed to perform various digital processing functions _(like translation, rotation, resizing, cropping, fading, scaling)_ on-the-go.

Furthermore, DeFFcode can **extract frames with any specification** such as Framerate, Resolution, Hardware decoder, Complex Filter into any pixel format FFmpeg supports and also provides extensive support for almost FFmpeg parameter available. 

&thinsp;

!!! example "For usage, kindly refer our **[Basic Recipes :pie:](../../examples/basic)** and **[Advanced Recipes :microscope:](../../examples/advanced)**"

!!! info "FFdecoder API parameters are explained [here ➶](params/)"

::: deffcode.FFdecoder

&nbsp;