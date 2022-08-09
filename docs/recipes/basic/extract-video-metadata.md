<!--
======================================================================
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
======================================================================
-->

# :material-file-cog: Extracting Video Metadata

> DeFFcode's Sourcer API acts as **Source Probing Utility** for easily probing metadata information for each multimedia stream available in the given video source, and return it as in Human-readable _(as JSON string)_ or Machine-readable _(as Dictionary object)_ type with its [`retrieve_metadata()`](../../reference/sourcer/#deffcode.sourcer.Sourcer.retrieve_metadata) class method. Apart from this, you can also use [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object in FFdecoder API to extract this metadata information _(only as JSON string)_.

We'll discuss video metadata extraction using both these APIs briefly in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## Extracting video metadata using Sourcer API

!!! quote "This is the recommended way for extracting video metadata."

In this example we will probe all metadata information available within `foo.mp4` video file on :fontawesome-brands-windows: Windows machine, and print it in both Human-readable _(as JSON string)_ and Machine-readable _(as Dictionary object)_ types using `retrieve_metadata()` class method in Sourcer API:

!!! info "The Sourcer API's `retrieve_metadata()` class method provides `pretty_json` boolean parameter to return metadata as JSON string _(if `True`)_ and as Dictionary _(if `False`)_."

=== "As JSON string"

    ```python
    # import the necessary packages
    from deffcode import Sourcer

    # initialize and formulate the decoder using suitable source
    sourcer = Sourcer("foo.mp4").probe_stream()

    # print metadata as `json.dump`
    print(sourcer.retrieve_metadata(pretty_json=True))
    ```
    ???+ abstract "After running above python code, the resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"
        ```json
        {
          "ffmpeg_binary_path": "C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe",
          "source": "foo.mp4",
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

=== "As Dictionary object"

    ```python
    # import the necessary packages
    from deffcode import Sourcer

    # initialize and formulate the decoder using suitable source
    sourcer = Sourcer("foo.mp4").probe_stream()

    # print metadata as `dict`
    print(sourcer.retrieve_metadata())
    ```
    
    ???+ abstract "After running above python code, the resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"
        ```py
        {'ffmpeg_binary_path': 'C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe', 'source': 'foo.mp4', 'source_extension': '.mp4', 'source_video_resolution': [1280, 720], 'source_video_framerate': 25.0, 'source_video_pixfmt': 'yuv420p', 'source_video_decoder': 'h264', 'source_duration_sec': 5.31, 'approx_video_nframes': 133, 'source_video_bitrate': '1205k', 'source_audio_bitrate': '384k', 'source_audio_samplerate': '48000 Hz', 'source_has_video': True, 'source_has_audio': True, 'source_has_image_sequence': False}
    
        ```

&nbsp;

## Extracting video metadata using FFdecoder API

In this example we will probe all metadata information available within `foo.mp4` video file on :fontawesome-brands-windows: Windows machine, and print it as JSON string using  [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object in FFdecoder API.

!!! note "You can also update video's metadata by using the same overloaded [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object in FFdecoder API. More information can be found in this [Advanced Recipe :material-pot-steam: ➶](../../advanced/update-metadata/#updating-source-video-metadata-in-ffdecoder-api)"

```python
# import the necessary packages
from deffcode import FFdecoder

# initialize and formulate the decoder using suitable source
decoder = FFdecoder("foo.mp4").formulate()

# print metadata as `json.dump`
print(decoder.metadata)

# terminate the decoder
decoder.terminate()
```
??? abstract "After running above python code, the resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"
    ```json
    {
      "ffmpeg_binary_path": "C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe",
      "source": "foo.mp4",
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
      "ffdecoder_operational_mode": "Video-Only",
      "output_frames_pixfmt": "rgb24"
    }
    ```

&nbsp;