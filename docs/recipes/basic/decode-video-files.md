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

# :material-file-eye: Decoding Video files

> DeFFcode's FFdecoder API readily supports multimedia Video files path as input to its [`source`](../../reference/sourcer/params/#source) parameter. And with its [`frame_format`](../../reference/sourcer/params/#frame_format) parameter, you can easily decode video frames in any pixel format(s) that are readily supported by all well known Computer Vision libraries _(such as OpenCV)_.  

We'll discuss its video files support and pixel format capabilities briefly in the following recipes:

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


## Accessing RGB frames from a video file


!!! abstract "The default function of FFdecoder API is to **decode 24-bit RGB video frames** from the given source."

> FFdecoder API's [`generateFrame()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.generateFrame) function can be used in multiple methods to access RGB frames from a given source, such as **as a Generator** _(Recommended Approach)_, **calling `with` Statement**, and **as a Iterator**. 

In this example we will decode the default **RGB24** video frames from a given Video file _(say `foo.mp4`)_ using above mentioned  accessing methods:


=== "As a Generator (Recommended)"

    !!! quote "This is a recommended approach for faster and error-proof access of decoded frames. We'll use it throughout the recipes."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder

    # initialize and formulate the decoder
    decoder = FFdecoder("foo.mp4").formulate()

    # grab RGB24(default) frame from decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}

        # lets print its shape
        print(frame.shape) # for e.g. (1080, 1920, 3)

    # terminate the decoder
    decoder.terminate()
    ```

=== "Calling `with` Statement"

    !!! quote "Calling `with` Statement approach can be used to make the code easier, cleaner, and much more readable. This approach also automatically handles management of `formulate()` and `terminate()` methods in FFdecoder API, so don't need to explicitly call them. See [PEP343 -- The 'with' statement'](https://peps.python.org/pep-0343/) for more information on this approach."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # initialize and formulate the decoder
    with FFdecoder("foo.mp4") as decoder:

        # grab the BGR24 frames from decoder
        for frame in decoder.generateFrame():

            # check if frame is None
            if frame is None:
                break

            # {do something with the frame here}

            # lets print its shape
            print(frame.shape)  # for e.g. (1080, 1920, 3)
    ```

=== "As a Iterator"

    !!! quote "This Iterator Approach bears a close resemblance to **OpenCV-Python** _(Python API for OpenCV)_ coding syntax, thereby easier to learn and remember."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder

    # initialize and formulate the decoder
    decoder = FFdecoder("foo.mp4").formulate()

    # loop over frames
    while True:

        # grab RGB24(default) frames from decoder
        frame = next(decoder.generateFrame(), None)

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}
        
        # lets print its shape
        print(frame.shape) # for e.g. (1080, 1920, 3)

    # terminate the decoder
    decoder.terminate()
    ```



&nbsp;

## Decoding a specific video stream from a multi-stream file

> Some sources carry **several embedded video streams** in a single input _(such as an `.mkv` with two video tracks, or an HLS playlist with several renditions)_. By default, FFdecoder decodes the **first** video stream _(skipping cover art)_ and logs a warning, instead of the one [FFmpeg would pick automatically](https://ffmpeg.org/ffmpeg.html#Automatic-stream-selection) _(`default` disposition, otherwise the highest resolution)_.

In this example we will first inspect the second video stream of a source with Sourcer API, and then decode only that stream with FFdecoder API's [`-default_stream_indexes`](../../reference/ffdecoder/params/#b-exclusive-parameters) exclusive parameter. To keep it runnable anywhere, the source is a [`lavfi`](https://ffmpeg.org/ffmpeg-devices.html#lavfi) graph that produces **one input with two video streams** _(red `320x240` and blue `160x120`)_. A file path such as `foo.mkv` works the same way.

!!! info "Stream indexes are **per type**: `1` means the second **video** stream _(same as FFmpeg's `0:v:1` specifier)_, not the absolute `Stream #0:1`. So audio streams placed before the video ones don't shift it."

!!! tip "Per-stream details can be listed with `ffprobe -show_streams foo.mkv`, or with Sourcer API's `verbose=True`."

```python
# import the necessary packages
from deffcode import FFdecoder, Sourcer
import cv2

# one input with two embedded video streams (or use e.g. "foo.mkv")
source = "color=c=red:s=320x240:r=25:d=5[out0];color=c=blue:s=160x120:r=30:d=5[out1]"

# inspect second video stream (and first audio stream) metadata
metadata = (
    Sourcer(source, source_demuxer="lavfi")
    .probe_stream(default_stream_indexes=(1, 0))
    .retrieve_metadata()
)
print(metadata["source_video_streams"])  # 2
print(metadata["source_video_resolution"])  # [160, 120]

# select second video stream (`-map 0:v:1` is applied automatically)
ffparams = {"-default_stream_indexes": (1, 0)}

# initialize and formulate the decoder for BGR24 output
decoder = FFdecoder(
    source, source_demuxer="lavfi", frame_format="bgr24", **ffparams
).formulate()

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

!!! tip "A plain `-map 0:v:1`, or a `-filter_complex` using only `[0:v:1]` _(e.g. `[0:v:1]hflip`)_, selects the stream too. When a filtergraph uses several streams, frame count and framerate follow `-default_stream_indexes` _(stream `0` by default)_."

!!! note "The number of decoded frames may differ by ±1 between FFmpeg versions _(FFmpeg < 8.1 repeats the last frame)_, so treat `approx_video_nframes` as approximate."

&nbsp;

## Decoding anamorphic and HDR video files

> Some sources store **non-square pixels** _(anamorphic DVD, HDV or broadcast video, e.g. `1440x1080` shown as `1920x1080`)_ or **HDR** video _(PQ/HLG transfer)_. FFdecoder decodes their pixels as stored, so frames look **squeezed** or **washed out**, and it logs a warning about each.

In this example we will check a video file _(say `foo.mkv`)_ for both, using Sourcer API's `source_video_sar` and `source_video_color_transfer` metadata, and add the matching FFmpeg filters through FFdecoder API's `-vf` parameter, before previewing BGR24 frames with OpenCV.

!!! warning "Tone-mapping uses the `zscale` filter, so it needs FFmpeg built with `libzimg` _(included in most static builds)_."

!!! info "Color metadata is `\"\"` when the source doesn't tag it, and some FFmpeg versions report `unknown` _(also `\"\"`)_ for tags other versions print."

```python
# import the necessary packages
from deffcode import FFdecoder, Sourcer
import cv2

# probe source metadata
metadata = Sourcer("foo.mkv").probe_stream().retrieve_metadata()
print(metadata["source_video_resolution"])  # [1440, 1080]
print(metadata["source_video_sar"], metadata["source_video_dar"])  # [4, 3] [16, 9]
print(metadata["source_video_color_transfer"])  # smpte2084

filters = []
# tone-map HDR (PQ or HLG) to SDR BT.709
if metadata["source_video_color_transfer"] in ("smpte2084", "arib-std-b67"):
    filters.append(
        "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
        "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
    )
# stretch non-square pixels to display aspect ratio (here 1920x1080)
if metadata["source_video_sar"] != [1, 1]:
    filters.append("scale=iw*sar:ih,setsar=1")
ffparams = {"-vf": ",".join(filters)} if filters else {}

# initialize and formulate the decoder for BGR24 output
decoder = FFdecoder("foo.mkv", frame_format="bgr24", **ffparams).formulate()

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

## Capturing and Previewing BGR frames from a video file

In this example we will decode **OpenCV supported** live **BGR24** video frames from a given Video file _(say `foo.mp4`)_ in FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method.

!!! alert "By default, OpenCV expects `BGR` format frames in its `cv2.imshow()` method by using two accessing methods."

=== "As a Generator (Recommended)"

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # initialize and formulate the decoder for BGR24 pixel format output
    decoder = FFdecoder("foo.mp4", frame_format="bgr24").formulate()

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

=== "Calling `with` Statement"

    !!! quote "Calling `with` Statement approach can be used to make the code easier, cleaner, and much more readable. This approach also automatically handles management of `formulate()` and `terminate()` methods in FFdecoder API, so don't need to explicitly call them. See [PEP343 -- The 'with' statement'](https://peps.python.org/pep-0343/) for more information on this approach."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # initialize and formulate the decoder for BGR24 pixel format output
    with FFdecoder("foo.mp4", frame_format="bgr24") as decoder:

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
    ```

&nbsp;

## Playing with any other FFmpeg pixel formats

!!! abstract "Similar to BGR, you can input any pixel format _(supported by installed FFmpeg)_ by way of `frame_format` parameter of FFdecoder API for the desired video frame format."

In this example we will decode live **Grayscale** and **YUV** video frames from a given Video file _(say `foo.mp4`)_ in FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method.

!!! tip "Use `#!sh ffmpeg -pix_fmts` terminal command to lists all FFmpeg supported pixel formats."

=== "Decode Grayscale"

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # initialize and formulate the decoder for GRAYSCALE output
    decoder = FFdecoder("input_foo.mp4", frame_format="gray", verbose=True).formulate()

    # grab the GRAYSCALE frames from the decoder
    for gray in decoder.generateFrame():

        # check if frame is None
        if gray is None:
            break

        # {do something with the gray frame here}
        
        # Show output window
        cv2.imshow("Gray Output", gray)

        # check for 'q' key if pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # close output window
    cv2.destroyAllWindows()

    # terminate the decoder
    decoder.terminate()
    ```

=== "Decode Grayscale via YUV (fastest)"

    !!! success ":zap: Fastest RAW-to-Grayscale via `-extract_luma`"

        Every YUV/NV bytestream stores the **Luma (Y) plane** uncompressed at the top of each frame. The exclusive [`-extract_luma`](../../reference/ffdecoder/params/#b-exclusive-parameters) boolean attribute makes FFdecoder slice that Y-plane directly and hand back a 2D `(H, W)` grayscale ndarray — **no colorspace conversion in FFmpeg, no `cv2.cvtColor` in Python**. This is strictly faster than `frame_format="gray"`, which still asks FFmpeg to do a `yuv→gray` conversion on every frame.

        Combined with the reduced pipe-bytes of YUV 4:2:0 ingest, this is the fastest grayscale pipeline the API can produce.

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # enable direct Luma (Y-plane) extraction
    ffparams = {"-extract_luma": True}

    # initialize the decoder with a YUV pixel-format
    decoder = FFdecoder(
        "input_foo.mp4", frame_format="yuv420p", verbose=True, **ffparams
    ).formulate()

    # grab the 2D (H, W) grayscale frames from the decoder
    for gray in decoder.generateFrame():

        # check if frame is None
        if gray is None:
            break

        # {do something with the gray frame here}

        # Show output window
        cv2.imshow("Gray Output", gray)

        # check for 'q' key if pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # close output window
    cv2.destroyAllWindows()

    # terminate the decoder
    decoder.terminate()
    ```

=== "Decode YUV frames"

    !!! quote "With FFdecoder API, frames extracted with YUV pixel formats _(`yuv420p`, `yuv444p`, `nv12`, `nv21` etc.)_ are generally incompatible with OpenCV APIs. But you can make them easily compatible by using exclusive [`-enforce_cv_patch`](../../reference/ffdecoder/params/#b-exclusive-parameters) boolean attribute of its `ffparam` dictionary parameter."

    !!! success "Performance Mode — :zap: Faster Decoding via YUV420p"

        Ingesting frames as 12-bit **YUV 4:2:0** instead of 24-bit **RGB/BGR** halves the bytes moving through the FFmpeg pipe, so the subprocess pipeline spends less time blocked on I/O. In community benchmarks on 1080p MP4 _(see [issue #15](https://github.com/abhiTronix/deffcode/issues/15))_, RAW ingest jumped from **~96 FPS (RGB24)** to **~213 FPS (YUV420p)**, and **~155 FPS** when converted to BGR inside Python via OpenCV — a **25–33% gain** over the RGB path for the majority of common video sources _(which are already YUV420 on disk)_.

        Use this mode when you're throughput-bound on decoding and can afford a single `cv2.cvtColor` call per frame. Skip it for scientific workloads where the implicit chroma subsampling of YUV 4:2:0 is unacceptable.

    Let's try decoding YUV420p pixel-format frames in following python code:

    !!! info "You can also use other YUV pixel formats such `yuv422p`(4:2:2 subsampling) or `yuv444p`(4:4:4 subsampling) etc. instead for more higher dynamic range in the similar manner."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # enable OpenCV patch for YUV frames
    ffparams = {"-enforce_cv_patch": True}

    # initialize and formulate the decoder for YUV420p output
    decoder = FFdecoder(
        "input_foo.mp4", frame_format="yuv420p", verbose=True, **ffparams
    ).formulate()

    # grab the YUV420p frames from the decoder
    for yuv in decoder.generateFrame():

        # check if frame is None
        if yuv is None:
            break

        # convert it to `BGR` pixel format,
        # since imshow() method only accepts `BGR` frames
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

        # {do something with the bgr frame here}

        # Show output window
        cv2.imshow("Output", bgr)

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

## Capturing and Previewing frames from a Looping Video

In this example we will decode live **BGR24** video frames from looping video using different means in FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method.

=== "Using `-stream_loop` option"

    The recommend way to loop video is to use `-stream_loop` option via. [`-ffprefixes`](../../reference/ffdecoder/params/#b-exclusive-parameters) list attribute of `ffparam` dictionary parameter in FFdecoder API. **Possible values are integer values:** `> 0` value of loop, `0` means no loop, `-1` means infinite loop.

    !!! note "Using `-stream_loop 3` will loop video `4` times."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # define `-stream_loop 3` for looping 4 times
    ffparams = {"-ffprefixes":["-stream_loop", "3"]}

    # initialize and formulate the decoder with suitable source
    decoder = FFdecoder("input.mp4", frame_format="bgr24", verbose=True, **ffparams).formulate()

    # print metadata as `json.dump`
    print(decoder.metadata)

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

=== "Using `loop` filter"

    Another way to loop video is to use `loop` complex filter via. `-filter_complex` FFmpeg flag as attribute of `ffparam` dictionary parameter in FFdecoder API. 

    !!! warning "This filter places all frames into memory(RAM), so applying [`trim`](https://ffmpeg.org/ffmpeg-filters.html#toc-trim) filter first is strongly recommended. Otherwise you might probably run Out of Memory."

    !!! tip "Using `loop` filter for looping video"
        The filter accepts the following options:
        
        - `loop`: Sets the number of loops for integer values `>0`. Setting this value to `-1` will result in infinite loops. Default is `0`(no loops).
        - `size`: Sets maximal size in number of frames. Default is `0`.
        - `start`: Sets first frame of loop. Default is `0`.

    !!! note "Using `loop=3` will loop video `4` times."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # define loop 4 times, each loop is 15 frames, each loop skips the first 25 frames
    ffparams = {
        "-filter_complex": "loop=loop=3:size=15:start=25" # Or use: `loop=3:15:25`
    }  

    # initialize and formulate the decoder with suitable source
    decoder = FFdecoder(
        "input.mp4", frame_format="bgr24", verbose=True, **ffparams
    ).formulate()

    # print metadata as `json.dump`
    print(decoder.metadata)

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
