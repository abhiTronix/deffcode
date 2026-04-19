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

# :material-timer-sync: Per-Frame Metadata Extraction

> Each raw numpy frame handed to you by FFdecoder normally loses its temporal context — it's just a matrix of pixels with no notion of _when_ it should appear (PTS) or _how_ it was encoded (Keyframe vs. Predictive frame). The [`-extract_metadata`](../../reference/ffdecoder/params/#exclusive-parameters) exclusive parameter closes that gap: when enabled, [`generateFrame()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.generateFrame) yields `(frame, meta)` tuples, where `meta` is a python dict parsed from FFmpeg's [`showinfo`](https://ffmpeg.org/ffmpeg-filters.html#showinfo) filter — emitted on stderr and consumed asynchronously by a background daemon thread so the main `stdout` frame pipe is never throttled.

The metadata dict contains the following keys:

- **`frame_num`** _(int)_: monotonic frame index as emitted by FFmpeg.
- **`pts_time`** _(float)_: presentation timestamp in seconds.
- **`is_keyframe`** _(bool)_: `True` if the frame is a keyframe _(I-frame)_.
- **`frame_type`** _(str)_: one of `"I"` _(keyframe)_, `"P"` _(predictive)_, `"B"` _(bi-predictive)_, `"?"` _(unknown)_.

We'll walk through two flagship optimizations this unlocks in the recipes below.

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

!!! warning "Incompatible with `-filter_complex`"

    `-extract_metadata` cannot be combined with the `-filter_complex` attribute (graph-label routing is ambiguous). If both are supplied, a warning is logged and metadata extraction is silently disabled. A pre-existing `-vf` is fine — `showinfo` is automatically comma-chained onto it.

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## Smart Keyframe-only decoding for heavy AI inference

> Many Computer Vision workflows — perceptual hashing, scene-change detection, video summarisation, heavyweight AI-model inference _(YOLO, ResNet, etc.)_ — only really care about **Keyframes (I-frames)**. On a 60 FPS source with a typical GOP size, that's ~1-2 frames per second worth looking at. Without `-extract_metadata` you'd still decode and run your model on every single P/B frame and waste 98%+ of your compute on nearly-identical predictive frames.

With `meta["is_keyframe"]` in hand, you can skip those frames entirely:

```python
# import the necessary packages
from deffcode import FFdecoder

# instantiate the decoder with per-frame metadata extraction enabled
decoder = FFdecoder(
    "foo.mp4",
    frame_format="bgr24",
    **{"-extract_metadata": True},
).formulate()

# grab (frame, meta) pairs from the generator
for frame, meta in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # OPTIMIZATION: skip processing entirely if it is not a keyframe
    if not meta["is_keyframe"]:
        continue

    # now run your heavy AI model on ~1-2 frames per second only
    results = heavy_ai_model.predict(frame)

# terminate the decoder
decoder.terminate()
```

!!! success "Depending on the source's GOP (Group-of-Pictures) size, this pattern reduces downstream processing time by 10–50× without skipping any scene-boundary information."

&thinsp;

## Variable-Frame-Rate (VFR) synchronization via `pts_time`

> Most modern video sources — smartphones, screen recordings, webcams, browser captures — are **Variable-Frame-Rate**. The gap between frame 1 and 2 might be 16 ms while the gap between frame 2 and 3 is 40 ms. If you are measuring motion for sports analytics, computing velocity vectors, or keeping OpenCV bounding boxes synchronised with an audio track, _assuming a constant frame rate will drift out of sync very quickly_.

With `meta["pts_time"]` you know the **exact presentation timestamp** of every frame:

```python
# import the necessary packages
from deffcode import FFdecoder

# instantiate decoder for a VFR source
decoder = FFdecoder(
    "screen_recording.mp4",
    frame_format="bgr24",
    **{"-extract_metadata": True},
).formulate()

prev_pts = None
for frame, meta in decoder.generateFrame():
    if frame is None:
        break

    # exact presentation timestamp in seconds
    pts = meta["pts_time"]

    # compute real inter-frame delta (not the nominal 1/fps value)
    delta_ms = None if prev_pts is None else (pts - prev_pts) * 1000.0
    prev_pts = pts

    # use real delta for per-frame motion/velocity calculations
    # e.g. velocity = displacement_px / delta_ms

# terminate the decoder
decoder.terminate()
```

!!! tip "The same `pts_time` stream is what you need to keep processed frames locked to an audio track when re-muxing downstream."

&thinsp;

## Implementation notes

- The `showinfo` filter is appended _(not overwritten)_ to any user-supplied `-vf` filter via comma-concatenation, so your existing filter graph is preserved.
- FFmpeg's stderr is captured with `subprocess.PIPE` regardless of the `verbose` flag — otherwise a verbose pipeline would let stderr leak to the parent tty and starve the metadata reader.
- The background reader thread is a **daemon**; on [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) the stderr pipe is closed, a stop-event is signalled, and the thread is joined with a 2-second timeout so no pipeline ever outlives the decoder object.
- `metadata_queue.get()` uses a bounded 10-second timeout. If `showinfo` ever stops emitting lines (e.g. an exotic filter chain drops frames), the consumer logs a warning and yields the frame with `meta=None` rather than deadlocking.

&thinsp;

<!--
External URLs
-->
[ffmpeg]:https://www.ffmpeg.org/
