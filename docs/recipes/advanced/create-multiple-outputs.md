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

# :material-call-split: Creating Multiple Outputs

> FFmpeg can write [any number of outputs](https://trac.ffmpeg.org/wiki/Creating%20multiple%20outputs) from a single process, decoding the source only **once**. The [`-extra_outputs`](../../reference/ffdecoder/params/#b-exclusive-parameters) exclusive parameter brings this to FFdecoder: you keep receiving frames in Python, while the same FFmpeg pipeline records to files, transcodes or streams to servers in parallel.

Its values are appended **after** the rawvideo pipe output, so they form outputs `#1..N` of the pipeline, and never alter the frames delivered to Python:

```sh
ffmpeg ... -i foo.mp4 -pix_fmt rgb24 -s 1280x720 -framerate 25.0 -f rawvideo - {{-extra_outputs FFmpeg params}}
#                     └──────────── output #0: frames → Python ─────────────┘ └──── outputs #1..N ────┘
```

We'll discuss its usage in the recipes below.

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

!!! tip "Turn on `verbose=True` to see the full FFmpeg command executed in FFdecoder's pipeline, along with any error FFmpeg reports for an extra output."

&thinsp;

## Recording while decoding

> In this example we will decode frames in Python while the same pipeline copies the source streams _(no re-encoding)_ into a `.mkv` file.

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define extra output: copy all source streams into `recording.mkv`
ffparams = {"-extra_outputs": ["-y", "-map", "0", "-c", "copy", "recording.mkv"]}

# initialize and formulate the decoder
decoder = FFdecoder("foo.mp4", frame_format="bgr24", **ffparams).formulate()

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

&thinsp;

## Same filtering for all outputs

> In this example we will deinterlace the source once with `yadif`, then `split` it: frames scaled to 720p go to Python, while a 480p copy is encoded into a `.mp4` file.

Label the `-filter_complex` outputs, select the one for Python with `-map`, and consume the others inside `-extra_outputs`:

```python
# import the necessary packages
from deffcode import FFdecoder

# define filtergraph with labeled outputs
ffparams = {
    "-filter_complex": "[0:v]yadif,split=2[main][rec];[main]scale=-2:720[main];[rec]scale=-2:480[rec]",
    "-map": "[main]",  # frames for Python
    "-extra_outputs": [
        "-y",
        "-map", "[rec]", "-map", "0:a?",  # filtered video + source audio (if any)
        "-c:v", "libx264", "-crf", 23, "-c:a", "aac",
        "output_480p.mp4",
    ],
}

# initialize and formulate the decoder
decoder = FFdecoder("foo.mp4", frame_format="bgr24", **ffparams).formulate()

# grab the 720p BGR24 frames from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

# terminate the decoder
decoder.terminate()
```

&thinsp;

## Different filtering for each output

> In this example, Python receives blurred frames while a negated copy is written to a file.

```python
# import the necessary packages
from deffcode import FFdecoder

# one filter chain per labeled output
ffparams = {
    "-filter_complex": "[0:v]split=2[in1][in2];[in1]boxblur=5[out1];[in2]negate[out2]",
    "-map": "[out1]",  # blurred frames for Python
    "-extra_outputs": ["-y", "-map", "[out2]", "-c:v", "libx264", "negated.mp4"],
}

# initialize and formulate the decoder
decoder = FFdecoder("foo.mp4", frame_format="bgr24", **ffparams).formulate()

# grab the BGR24 frames from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

# terminate the decoder
decoder.terminate()
```

&thinsp;

## Encode once, duplicate to file and stream

> The [`tee`](https://ffmpeg.org/ffmpeg-formats.html#tee-1) muxer encodes **once** and writes the same packets to several destinations. In this example we will save a `.mkv` file and stream MPEG-TS over UDP at the same time.

```python
# import the necessary packages
from deffcode import FFdecoder

ffparams = {
    "-extra_outputs": [
        "-y",
        "-map", "0:v", "-map", "0:a?",
        "-c:v", "libx264", "-c:a", "aac",
        "-flags", "+global_header",  # required by tee for mkv/flv
        "-f", "tee",
        # `onfail=ignore` keeps decoding alive if the stream fails
        "archive.mkv|[f=mpegts:onfail=ignore]udp://127.0.0.1:1234",
    ],
}

# initialize and formulate the decoder
decoder = FFdecoder("foo.mp4", frame_format="bgr24", **ffparams).formulate()

# grab the BGR24 frames from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

# terminate the decoder
decoder.terminate()
```

&thinsp;

## Caveats

!!! danger "Things to keep in mind with `-extra_outputs`"

    | Caveat | Cause | Remedy |
    |---|---|---|
    | No frames are decoded if an output file already exists | FFmpeg exits on its overwrite prompt | Always add `"-y"` to `-extra_outputs` |
    | Any failing extra output kills frame decoding too | FFmpeg aborts all outputs on a muxer error | Use `-f tee` with `[onfail=ignore]` for fragile outputs |
    | Extra outputs run at the speed of your Python loop | FFmpeg blocks until Python reads each frame | Keep the frame loop fast |
    | `-frames:v`/`-t` in `ffparams` only limit frames sent to Python | They are output options of the rawvideo pipe | Repeat them inside `-extra_outputs` for each output |
    | `tee` fails with header errors on `.mkv`/`.flv` | Those formats need a global header | Add `"-flags", "+global_header"` |
    | Calling `terminate()` early truncates extra outputs | By design | Outputs are finalized gracefully; for live sources prefer `.mkv`/`.ts` over `.mp4` |

!!! info "Need several raw frame streams _(e.g. 720p and 240p)_ in Python at once? Combine them into one frame with `hstack`/`vstack` filters and slice the array, or run two FFdecoder instances."

&thinsp;
