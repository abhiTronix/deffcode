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

# :fontawesome-solid-cloud-arrow-down: Decoding Network Streams

> Similar to decoding Video files, DeFFcode's FFdecoder API directly supports Network Streams with specific protocols _(such as RTSP/RTP, HTTP(s), MPEG-TS, etc.)_ as input to its [`source`](../../reference/sourcer/params/#source) parameter. 

We'll discuss Network Streams support briefly in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../installation/ffmpeg_install/) for its installation.

??? info "Additional Python Dependencies for following recipes"

    Following recipes requires additional python dependencies which can be installed easily as below:

    - [x] **OpenCV:** OpenCV is required for previewing video frames. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ??? tip "OpenCV installation from source"

            You can also follow online tutorials for building & installing OpenCV on [Windows](https://www.learnopencv.com/install-opencv3-on-windows/), [Linux](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/), [MacOS](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) and [Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) machines manually from its source. 

            :warning: Make sure not to install both *pip* and *source* version together. Otherwise installation will fail to work!

        ??? info "Other OpenCV binaries"

            OpenCV maintainers also provide additional binaries via pip that contains both main modules and contrib/extra modules [`opencv-contrib-python`](https://pypi.org/project/opencv-contrib-python/), and for server (headless) environments like [`opencv-python-headless`](https://pypi.org/project/opencv-python-headless/) and [`opencv-contrib-python-headless`](https://pypi.org/project/opencv-contrib-python-headless/). You can also install ==any one of them== in similar manner. More information can be found [here](https://github.com/opencv/opencv-python#installation-and-usage).


        ```sh
        pip install opencv-python       
        ```


!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;


## Capturing and Previewing frames from a HTTPs Stream

In this example we will decode live **BGR24** video frames from a HTTPs protocol Stream in FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method.


```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# initialize and formulate the decoder for BGR24 pixel format output
decoder = FFdecoder("https://abhitronix.github.io/html/Big_Buck_Bunny_1080_10s_1MB.mp4", frame_format="bgr24").formulate()

# grab the BGR24 frames from decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}
    
    # Show output window
    cv2.imshow("Output", frame)

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

## Decoding a specific rendition from a HLS Stream

> A HLS **master playlist** _(`.m3u8`)_ usually carries several renditions of the same video at different resolutions, which FFmpeg exposes as **embedded video streams of one input**. Without a selection, FFdecoder decodes the **first** rendition in playlist order _(often the lowest quality)_ and logs a warning. So ==select the rendition explicitly== with FFdecoder API's [`-default_stream_indexes`](../../reference/ffdecoder/params/#b-exclusive-parameters) exclusive parameter.

In this example we will list the renditions of a HLS master playlist _(say `https://example.com/master.m3u8`)_ with Sourcer API, and then decode **BGR24** frames from the second one.

!!! info "Renditions are counted in playlist order: `(1, 0)` selects the second video stream _(FFmpeg's `0:v:1`)_, and `source_video_streams` metadata gives their number."

```python
# import the necessary packages
from deffcode import FFdecoder, Sourcer
import cv2

# define HLS master playlist URL
source = "https://example.com/master.m3u8"

# list each rendition's resolution
sourcer = Sourcer(source)
count = sourcer.probe_stream().retrieve_metadata()["source_video_streams"]
for index in range(count):
    metadata = sourcer.probe_stream(default_stream_indexes=(index, 0)).retrieve_metadata()
    print(index, metadata["source_video_resolution"])

# select the second rendition (applies `-map 0:v:1` automatically)
ffparams = {"-default_stream_indexes": (1, 0)}

# initialize and formulate the decoder for BGR24 pixel format output
decoder = FFdecoder(source, frame_format="bgr24", **ffparams).formulate()

# grab the BGR24 frames from decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # Show output window
    cv2.imshow("Output", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# terminate the decoder
decoder.terminate()
```

!!! tip "Sourcer API logs a warning when an index is out of range _(and falls back to the first stream)_, so you'll know when you've run past the last rendition. FFdecoder also warns when a multi-rendition source is decoded without selecting one."

&nbsp;

## Capturing and Previewing frames from a RTSP/RTP Stream

In this example we will decode live **BGR24** video frames from RTSP/RTP protocol Streams in FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method.

!!! alert "This example assume you already have a RSTP Server running at specified RSTP address with syntax `rtsp://[RTSP_ADDRESS]:[RTSP_PORT]/[RTSP_PATH]` and video data already being published to it."

!!! tip "For creating your own RSTP Server locally and publishing video data to it, You can refer this [WriteGear API's bonus example ➶](https://abhitronix.github.io/vidgear/dev/help/writegear_ex/#using-writegears-compression-mode-for-rtsprtp-live-streaming)"

!!! danger "Make sure to change RSTP address `rtsp://localhost:8554/mystream` with yours in following code before running"

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define suitable parameters
ffparams = {"-rtsp_transport": "tcp"}

# initialize and formulate the decoder with RTSP protocol source for BGR24 output
# [WARNING] Change your RSTP address `rtsp://localhost:8554/mystream` with yours!
decoder = FFdecoder("rtsp://localhost:8554/mystream", frame_format="bgr24", verbose=True, **ffparams).formulate()

# grab the BGR24 frames from decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}
    
    # Show output window
    cv2.imshow("Output", frame)

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