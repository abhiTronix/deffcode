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

# :material-play-box-multiple: Multi-Input Source Configurations

> DeFFcode's [Sourcer](../../reference/sourcer/) and [FFdecoder](../../reference/ffdecoder/) APIs accept their `source` and `source_demuxer` parameters as Python lists, ingesting multiple media streams simultaneously inside a single FFmpeg instance. This unlocks side-by-side composites, Picture-in-Picture (PiP) overlays, multi-camera comparisons, and custom video mixing — all driven natively by FFmpeg's filter graph, with no inter-process glue on your side.

We'll walk through Multi-Input Source Configurations in the recipes below:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

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

!!! warning "FFdecoder requires explicit stream routing in multi-input mode"

    With multiple `-i` inputs FFmpeg auto-selects only the "best" video stream when no routing is given, which is rarely what you want. To prevent ambiguous decoding, FFdecoder API **requires** you to pass either `-map` or `-filter_complex` whenever `source` is a list. If neither is present, [`formulate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.formulate) raises a **`ValueError`** at initialization time.

!!! danger "Multi-input pipeline limitations"

    1. **`-vcodec` is input-scoped to source 0.** A single `-vcodec` parameter only applies to the first `-i` input (FFmpeg's positional-options rule). To pin a decoder per input in a multi-decoder pipeline, route it explicitly via `-filter_complex` or use FFmpeg's per-input options inside `-ffprefixes`.
    2. **`-extract_metadata` is incompatible with `-filter_complex`.** The [`showinfo`](https://ffmpeg.org/ffmpeg-filters.html#showinfo) filter that backs per-frame metadata cannot share the graph with `-filter_complex`, so FFdecoder will warn and disable `-extract_metadata` in any multi-input pipeline that uses one.
    3. **Per-input lists must match `source` length.** If you pass `-ffprefixes` or `source_demuxer` as a list, its length must equal the `source` list length — otherwise DeFFcode raises `ValueError` immediately. Use an empty inner list (`[]`) or `None` for any input that needs no value.

!!! tip "To learn about exclusive `-ffprefixes` parameter and its multi-input list-of-lists shape, see [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)."

!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## Decoding multiple inputs as side-by-side composite

> The simplest multi-input workflow is binding two media streams together horizontally with FFmpeg's [`hstack`](https://ffmpeg.org/ffmpeg-filters.html#hstack) filter — useful for A/B comparisons, before/after diffs, or multi-camera views.

In this example we will decode two video files _(say `video_stream_1.mp4` and `video_stream_2.mp4`)_ as a single side-by-side BGR24 frame stream by passing them as a list to FFdecoder API and routing both inputs through `hstack` via the `-filter_complex` parameter, and preview the composited frames using OpenCV Library's `cv2.imshow()` method in real-time.

!!! alert "Both inputs must share the same height for `hstack` to succeed. Use a `scale` clause inside `-filter_complex` if your sources differ in resolution."

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define our two media paths to stack side-by-side
source = [
    "video_stream_1.mp4",  # first input  (-i #0)
    "video_stream_2.mp4",  # second input (-i #1)
]

# `-filter_complex` is mandatory in multi-input mode;
# `hstack=inputs=2` concatenates both streams horizontally
ffparams = {"-filter_complex": "hstack=inputs=2"}

# initialize and formulate the decoder for BGR24 output
decoder = FFdecoder(source, frame_format="bgr24", **ffparams).formulate()

# grab the BGR24 frame from the decoder
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

## Decoding multiple RTSP streams in parallel

> When ingesting multiple live network streams _(such as IP cameras over RTSP)_, you typically need transport-level options that differ per camera _(e.g. forcing TCP transport to reduce packet corruption)_. The `-ffprefixes` exclusive parameter accepts a **list of per-input lists** in source order so each `-i` group gets its own pre-input options.

In this example we will decode two live RTSP camera feeds, force TCP transport on both inputs through per-input `-ffprefixes`, route them side-by-side with `hstack`, and preview the multiplexed BGR24 frames using OpenCV Library's `cv2.imshow()` method in real-time.

!!! alert "Remember to replace the placeholder RTSP URLs with the credentials and addresses of your own cameras before using this recipe."

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define multiple RTSP camera streams as our source list
source = [
    "rtsp://admin:pass@192.168.1.10:554/stream1",
    "rtsp://admin:pass@192.168.1.11:554/stream2",
]

# define per-input prefixes: one inner list per source, in source order
ffparams = {
    "-ffprefixes": [
        ["-rtsp_transport", "tcp"],  # applies to source 0 only
        ["-rtsp_transport", "tcp"],  # applies to source 1 only
    ],
    # route both inputs side-by-side
    "-filter_complex": "hstack=inputs=2",
}

# initialize and formulate the decoder for BGR24 output
decoder = FFdecoder(source, frame_format="bgr24", **ffparams).formulate()

# grab the BGR24 frame from the decoder
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

## Decoding Picture-in-Picture overlay with per-input configuration

> Real-world multi-input pipelines almost always need _different_ per-input options — for instance, real-time pacing _(`-re`)_ on a live stream paired with infinite looping _(`-stream_loop -1`)_ on a local asset. With `-ffprefixes` shaped as a list-of-lists, every input is configured independently while still sharing a single FFmpeg pipeline.

In this example we will overlay a looping local video file _(say `local_file.mp4`)_ in the top-right corner of a paced live HLS stream _(say `network_stream_1.m3u8`)_ via FFmpeg's [`overlay`](https://ffmpeg.org/ffmpeg-filters.html#toc-overlay-1) filter inside `-filter_complex`, supply per-input prefixes for each, and preview the resulting Picture-in-Picture BGR24 frames using OpenCV Library's `cv2.imshow()` method in real-time.

!!! info "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property to inspect the per-source metadata under the `sources` key once the pipeline is formulated."

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define our multi-input sources
source = [
    "network_stream_1.m3u8",  # live HLS stream as the base layer
    "local_file.mp4",         # local asset overlaid in the top-right corner
]

# define per-input prefixes and the overlay filter graph
ffparams = {
    "-ffprefixes": [
        ["-re"],                  # pace input 0 at native frame rate
        ["-stream_loop", "-1"],   # loop input 1 infinitely
    ],
    # PiP overlay: input 1 anchored 10px from the top-right of input 0
    "-filter_complex": "[0:v][1:v]overlay=main_w-overlay_w-10:10",
}

# initialize and formulate the decoder for BGR24 output
decoder = FFdecoder(source, frame_format="bgr24", **ffparams).formulate()

# grab the BGR24 frame from the decoder
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

## Decoding mixed sources with different demuxers

> Inputs in a multi-input pipeline can also originate from completely different device classes — for instance, a Linux webcam captured via `v4l2` paired with a synthetically generated [`lavfi`](http://underpop.online.fr/f/ffmpeg/help/lavfi.htm.gz) source. The `source_demuxer` parameter accepts a list whose entries align positionally with `source`, so each input gets its own `-f` directive.

In this example we will combine a live webcam feed _(captured via `v4l2` on Linux)_ with a generated Mandelbrot pattern _(via `lavfi`)_, stack them side-by-side with `hstack`, and preview the composite BGR24 frames using OpenCV Library's `cv2.imshow()` method in real-time.

!!! alert "This recipe requires Linux for `v4l2`. On other operating systems substitute `dshow` (Windows) or `avfoundation` (MacOS) along with the platform-appropriate device path."

!!! tip "Use `None` for any inner entry of `source_demuxer` whose corresponding source does not need an explicit `-f` directive — DeFFcode will simply omit it for that input."

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# webcam + virtual mandelbrot source
source = [
    "/dev/video0",                       # v4l2 camera (Linux)
    "mandelbrot=size=1280x720:rate=30",  # libavfilter virtual source
]

# per-input demuxers, aligned positionally with source
source_demuxer = [
    "v4l2",   # for /dev/video0
    "lavfi",  # for the mandelbrot filtergraph
]

# stack the camera feed next to the generated mandelbrot
ffparams = {"-filter_complex": "hstack=inputs=2"}

# initialize and formulate the decoder for BGR24 output
decoder = FFdecoder(
    source, source_demuxer=source_demuxer, frame_format="bgr24", **ffparams
).formulate()

# grab the BGR24 frame from the decoder
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

## Probing multiple inputs with Sourcer API

> The [Sourcer API](../../reference/sourcer/) probes each source independently — no `-map` or `-filter_complex` is required because nothing is being decoded into a single stream. The primary input's flat metadata fields _(`source_video_resolution`, `source_video_framerate`, etc.)_ come from `source[0]` and remain in the same shape as a single-source probe, while a new `sources` key is appended carrying the per-input metadata dict for every input in order.

In this example we will probe two video files _(say `video1.mp4` and `video2.mp4`)_ as a single Sourcer call and pretty-print the per-source metadata list extracted from the `sources` key.

!!! info "The flat top-level fields _(e.g. `source_video_resolution`)_ always describe `source[0]` so existing single-source consumers keep working unchanged."

```python
# import the necessary packages
from deffcode import Sourcer
import json

# define our multi-input sources
source = ["video1.mp4", "video2.mp4"]

# initialize the sourcer and probe each source sequentially
sourcer = Sourcer(source).probe_stream()

# the returned metadata mirrors the single-input shape for source[0]
# and exposes per-source dicts under the `sources` key
metadata = sourcer.retrieve_metadata()

# pretty-print the per-source metadata list
print(json.dumps(metadata["sources"], indent=4))
```

&nbsp;
