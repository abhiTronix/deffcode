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

# Sourcer API

DeFFcode's Sourcer API acts as **Source Validator and Classifier** _(just like ==_talent sourcer_==)_ for its [FFdecoder API](../../reference/ffdecoder). This API parses FFmpeg's [`subprocess`](https://docs.python.org/3/library/subprocess.html) output for a given source and uses it to validate and identify all valid streams available in it.

Sourcer API also acts as a **Metadata Extraction Tool** that extracts metadata of all specified valid streams that FFdecoder API uses for formatting its default FFmpeg pipeline for frames generation. Furthermore, Sourcer is responsible for **validating FFmpeg executable path** for DeFFcode. 

???+ info "Extracting Source Video Metadata in DeFFcode"
      Metadata can be easily extracted as a dictionary in Sourcer API using its [`retrieve_metadata()`](#deffcode.sourcer.Sourcer.retrieve_metadata) method. However, you can also use [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object in FFdecoder API to extract metadata as Pretty JSON, and update it directly as desired. **More information can be found in [this usage example ➶](../../examples/basic/#generate-source-video-metadata)**.

All parameter available with Sourcer API extracted as python dictionary(On :fontawesome-brands-windows:Windows), are as follows:  

```py
{
    "ffmpeg_binary_path": "C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe",
    "source": "foo.mp4",
    "source_extension": ".mp4",
    "source_video_resolution": [1280, 720],
    "source_video_framerate": 25.0,
    "source_video_pixfmt": "yuv420p",
    "source_video_decoder": "h264",
    "source_duration_sec": 5.31,
    "approx_video_nframes": 133,
    "source_video_bitrate": "1205k",
    "source_audio_bitrate": "384k",
    "source_audio_samplerate": "48000 Hz",
    "source_has_video": True,
    "source_has_audio": True,
    "source_has_image_sequence": False,
}
```

&thinsp;

!!! example "For usage, kindly refer our **[Basic Recipes :pie:](../../examples/basic)** and **[Advanced Recipes :microscope:](../../examples/advanced)**"

!!! info "Sourcer API parameters are explained [here ➶](params/)"

::: deffcode.Sourcer

&nbsp;

