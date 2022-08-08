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

# :material-cog-refresh: Updating Video Metadata

> In addition of using [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object in FFdecoder API for probing metadata information _(only as JSON string)_  for each multimedia stream available in the given video source, you can also easily update the video metadata on-the-fly by assigning desired data as python dictionary to the same overloaded `metadata` property object. This metadata information is used by FFdecoder API to formulate its default FFmpeg Pipeline for real-time video-frames generation.

We'll discuss video metadata extraction using both these APIs briefly in the following recipes:

!!! quote "This feature is not yet fully explored, but in the near future you'll be able to use it to dynamically alter any FFmpeg Pipeline property of your video frames _(such as frame-size, pixel-format, etc.)_ in real-time like a pro. Stay tuned :smiley:"

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## Added new properties to metadata in FFdecoder API

> In FFdecoder API, you can easily define **any number** of new properties for its metadata _(formatted as python dictionary)_ with desired data of **any datatype(s)[^1]** , without affecting its default Video frames Decoder pipeline.

In this example we will probe all metadata information available within `foo.mp4` video file on :fontawesome-brands-windows: Windows machine, thereby add new propertys  _(formatted as python dictionary)_ with desired data of different datatype(s) through overloaded `metadata` property object, and then finally print it as JSON string using the same `metadata` property object in FFdecoder API.

!!! warning "The value assigned to [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object can be of [`dictionary`](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) datatype only. Any other type will immediately raise `ValueError`!"

```python
# import the necessary packages
from deffcode import FFdecoder
import json

# initialize the decoder using suitable source
decoder = FFdecoder("foo.mp4", verbose=True)

# format your data as dictionary (with data of any [printable] datatype)
data = dict(
    mystring="abcd",  # string data
    myint=1234,  # integers data
    mylist=[1, "Rohan", ["inner_list"]],  # list data
    mytuple=(1, "John", ("inner_tuple")),  # tuple data
    mydict={"anotherstring": "hello"},  # dictionary data
    myjson=json.loads('{"name": "John", "age": 30, "city": "New York"}'),  # json data
)

# assign your dictionary data
decoder.metadata = data

# finally formulate the decoder
decoder.formulate()

# print metadata as `json.dump`
print(decoder.metadata)

# terminate the decoder
decoder.terminate()
```
??? abstract "After running above python code, the resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"
    ```json
    {
      "ffmpeg_binary_path": "C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe",
      "source": "D:\\foo.mp4",
      "source_extension": ".mp4",
      "source_video_resolution": [
        1920,
        1080
      ],
      "source_video_framerate": 29.97,
      "source_video_pixfmt": "yuv420p",
      "source_video_decoder": "h264",
      "source_duration_sec": 21.03,
      "approx_video_nframes": 630,
      "source_video_bitrate": "4937k",
      "source_audio_bitrate": "256k",
      "source_audio_samplerate": "48000 Hz",
      "source_has_video": true,
      "source_has_audio": true,
      "source_has_image_sequence": false,
      "ffdecoder_operational_mode": "Video-Only",
      "output_frames_pixfmt": "rgb24",
      "mystring": "abcd",
      "myint": 1234,
      "mylist": [
        1,
        "Rohan",
        [
          "inner_list"
        ]
      ],
      "mytuple": [
        1,
        "John",
        "inner_tuple"
      ],
      "mydict": {
        "anotherstring": "hello"
      },
      "myjson": {
        "name": "John",
        "age": 30,
        "city": "New York"
      }
    }
    ```

&nbsp;


## Updating source video metadata in FFdecoder API

> In FFdecoder API, you can also use its `metadata` to alter the source video properties _(as frame-size, frame pixel-format, video-framerate, video-decoder etc.)_ that directly affects its default Video frames Decoder pipeline that decodes real-time video-frames.

!!! alert "The `"source"` property in metadata cannot be altered in any manner."

??? danger "Source Video metadata values must be handled carefully"

    > Source Video metadata information is used by FFdecoder API to formulate its default Video frames Decoder pipeline, and any improper or invalid inputted video property could crash the pipeline with `RuntimeError`. 

    Therefore to safeguard against it, **FFdecoder API discards any Source Video metadata dictionary keys, if its value's datatype fails to match the exact valid datatype defined in following table:**

    !!! info "Only either `source_demuxer` or `source_extension` key can be present in source video metadata." 

    !!! quote "Not all Source Video metadata properties directly affects the pipeline _(as mentioned in the table)_. But this might change in future versions."


    | Source Video Metadata Keys | Valid Value Datatype | Effect on Pipeline |
    |:---------------------------:|:---------------------:|:---:|
    |`"source_extension"`|`string`| None |
    |`"source_demuxer"`|`string`| Direct |
    |`"source_video_resolution"`|`list of integers` _e.g. `[1280,720]`_| Direct |
    |`"source_video_framerate"`|`float`| Direct |
    |`"source_video_pixfmt"`|`string`| Direct |
    |`"source_video_decoder"`|`string`| Direct |
    |`"source_duration_sec"`|`float`| None |
    |`"approx_video_nframes"`|`integer`| Direct |
    |`"source_video_bitrate"`|`string`| None |
    |`"source_audio_bitrate"`|`string`| None |
    |`"source_audio_samplerate"`|`string`| None |
    |`"source_has_video"`|`bool`| Direct |
    |`"source_has_audio"`|`bool`| None |
    |`"source_has_image_sequence"`|`bool`| Direct |
    |`"ffdecoder_operational_mode"`|`str`| None |
    |`"output_frames_pixfmt"`|`str`| Direct |


    Hence for instance, if "source_video_resolution" is assigned `"1280x720"` _(i.e. `string` datatype value instead of `list`)_, then it will be discarded.


In this example we will probe all metadata information available within `foo.mp4` video file, and alter frame size _(originally `1920x1080`)_ and pixel-format  _(originally `rgb24`)_ to our desired values through overloaded `metadata` property object in FFdecoder API, and thereby preview them using OpenCV Library's `cv2.imshow()` method.

!!! warning "The value assigned to [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object can be of [`dictionary`](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) datatype only. Any other type will immediately raise `ValueError`!"

!!! note "Once the [`formulate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.formulate) method is called, the metadata information present in FFdecoder API is finalized and thereby used to formulate its default pipeline for decoding real-time video-frames. Therefore make all changes to video properties beforehand."

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# initialize and formulate the decoder using suitable source
decoder = FFdecoder("foo.mp4", verbose=True)

# assign custom source metadata values
# !!! [WARNING] Make sure each value datatype matches the table !!!
decoder.metadata = {
    "output_frames_pixfmt": "gray",  # gray frame-pixfmt
    "source_video_resolution": [1280, 720],  # 1280x720 frame-size
}

# finally formulate the decoder
decoder.formulate()

# [NOTE] uncomment following line to debug values
# print(decoder.metadata)

# let's grab the 1280x720 sized gray frames from decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with gray frame here}

    # Show gray frames in output window
    cv2.imshow("Output gray", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# terminate the decoder
decoder.terminate()
```

&nbsp;

[^1]: :warning: **There is no concept of `tuple` datatype in the JSON format.** Thereby, Python's [`json`](https://docs.python.org/3/library/json.html) module auto-converts all `tuple` python values into JSON `list` because that's the closest thing in JSON format to a tuple.