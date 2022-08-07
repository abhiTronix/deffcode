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

# :fontawesome-solid-wand-magic-sparkles: Transcoding Live Complex Filtergraphs

??? abstract "What are Complex filtergraphs?"

    Before heading straight into recipes we will talk about Complex filtergraphs: 
    
    > Complex filtergraphs are those which cannot be described as simply a linear processing chain applied to one stream.  

    Complex filtergraphs are configured with the `-filter_complex` global option. 

    !!! note "The `-lavfi` option is equivalent to `-filter_complex`."

    A trivial example of a complex filtergraph is the `overlay` filter, which has two video inputs and one video output, containing one video overlaid on top of the other.


> DeFFcode's FFdecoder API seamlessly supports processing multiple input streams including real-time frames through multiple filter chains combined into a filtergraph _(via. `-filter_complex` FFmpeg parameter)_, and use their outputs as inputs for other filter chains. 

We'll discuss the transcoding of live complex filtergraphs in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../installation/ffmpeg_install/) for its installation.

???+ info "Additional Python Dependencies for following recipes"

    Following recipes requires additional python dependencies which can be installed easily as below:

    - [x] **OpenCV:** OpenCV is required for previewing and encoding video frames. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ??? tip "OpenCV installation from source"

            You can also follow online tutorials for building & installing OpenCV on [Windows](https://www.learnopencv.com/install-opencv3-on-windows/), [Linux](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/), [MacOS](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) and [Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) machines manually from its source. 

            :warning: Make sure not to install both *pip* and *source* version together. Otherwise installation will fail to work!

        ??? info "Other OpenCV binaries"

            OpenCV mainainers also provide additional binaries via pip that contains both main modules and contrib/extra modules [`opencv-contrib-python`](https://pypi.org/project/opencv-contrib-python/), and for server (headless) environments like [`opencv-python-headless`](https://pypi.org/project/opencv-python-headless/) and [`opencv-contrib-python-headless`](https://pypi.org/project/opencv-contrib-python-headless/). You can also install ==any one of them== in similar manner. More information can be found [here](https://github.com/opencv/opencv-python#installation-and-usage).


        ```sh
        pip install opencv-python       
        ```

    - [x] **VidGear:** VidGear is required for lossless encoding of video frames into file/stream. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ```sh
        pip install vidgear[core]       
        ```

!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."


&thinsp;

## Transcoding video with Live Custom watermark image overlay

<figure markdown>
  ![Big Buck Bunny with watermark](../../../assets/gifs/watermark_overlay.gif)
  <figcaption>Big Buck Bunny with custom watermark</figcaption>
</figure>


In this example we will apply a watermark image _(say `watermark.png` with transparent background)_ overlay to the `10` seconds of video file _(say `foo.mp4`)_ using FFmpeg's `overlay` filter with some additional filtering, , and decode live **BGR24** video frames in FFdecoder API. We'll also be encoding those decoded frames in real-time into lossless video file using WriteGear API with controlled framerate.

!!! info "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps Source Metadata as JSON to retrieve source framerate and frame-size."

!!! tip "To learn about exclusive `-ffprefixes` & `-clones` parameter. See [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)"

```python
# import the necessary packages
from deffcode import FFdecoder
from vidgear.gears import WriteGear
import json, cv2

# define the Complex Video Filter with additional `watermark.png` image input
ffparams = {
    "-ffprefixes": ["-t", "10"],  # playback time of 10 seconds
    "-clones": [
        "-i",
        "watermark.png",  # !!! [WARNING] define your `watermark.png` here.
    ],
    "-filter_complex": "[1]format=rgba,"  # change 2nd(image) input format to yuv444p
    + "colorchannelmixer=aa=0.7[logo];"  # apply colorchannelmixer to image for controlling alpha [logo]
    + "[0][logo]overlay=W-w-{pixel}:H-h-{pixel}:format=auto,".format(  # apply overlay to 1st(video) with [logo]
        pixel=5  # at 5 pixels from the bottom right corner of the input video
    )
    + "format=bgr24",  # change output format to `yuv422p10le`
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "foo.mp4", frame_format="bgr24", verbose=True, **ffparams
).formulate()

# retrieve framerate from source JSON Metadata and pass it as `-input_framerate`
# parameter for controlled framerate and define other parameters
output_params = {
    "-input_framerate": json.loads(decoder.metadata)["source_video_framerate"],
}

# Define writer with default parameters and suitable
# output filename for e.g. `output_foo.mp4`
writer = WriteGear(output_filename="output_foo.mp4", logging=True, **output_params)

# grab the BGR24 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing BGR24 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.close()
```

&nbsp;

## Transcoding video from sequence of Images with additional filtering

<figure markdown>
  ![mandelbrot test pattern](../../../assets/gifs/fish_mandelbrot.gif)
  <figcaption>Mandelbrot pattern blend with Fish school video</figcaption>
</figure>

??? info "Available blend mode options" 

    **Other blend mode options for `blend` filter include:** `addition`, `addition128`, `grainmerge`, `and`, `average`, `burn`, `darken`, `difference`, `difference128`, `grainextract`, `divide`, `dodge`, `freeze`, `exclusion`, `extremity`, `glow`, `hardlight`, `hardmix`, `heat`, `lighten`, `linearlight`, `multiply`, `multiply128`, `negation`, `normal`, `or`, `overlay`, `phoenix`, `pinlight`, `reflect`, `screen`, `softlight`, `subtract`, `vividlight`, `xor`


In this example we will blend **`10` seconds of Mandelbrot test pattern** _(generated using `lavfi` input virtual device)_ that serves as the "top" layer with **`10` seconds of Image Sequence** that serves as the "bottom" layer, using `blend` filter _(with `heat` blend mode)_, and decode live **BGR24** video frames in FFdecoder API. We'll also be encoding those decoded frames in real-time into lossless video file using WriteGear API with controlled framerate.

!!! danger "==WriteGear's Compression Mode support for FFdecoder API is currently in beta so you can expect much higher than usual CPU utilization!=="

??? tip "Extracting Image Sequences from a video"
    
    **You can use following FFmpeg command to extract sequences of images from a video file `foo.mp4` _(restricted to 12 seconds)_:**
    
    ```sh
    $ ffmpeg -t 12 -i foo.mp4 /path/to/image-%03d.png
    ```

    The default framerate is `25` fps, therefore this command will extract `25 images/sec` from the video file, and save them as sequences of images _(starting from `image-000.png`, `image-001.png`, `image-002.png` up to `image-999.png`)_. 

    !!! info "If there are more than `1000` frames then the last image will be overwritten with the remaining frames leaving only the last frame."

    The default images width and height is same as the video.

??? question "How to start with specific number image?"
    You can use `-start_number` FFmpeg parameter if you want to start with specific number image:

    ```python
    # define `-start_number` such as `5`
    ffparams = {"-ffprefixes":["-start_number", "5"]}

    # initialize and formulate the decoder with define parameters
    decoder = FFdecoder('/path/to/img%03d.png', verbose=True, **ffparams).formulate()
    ```

!!! note "FFdecoder API also accepts Glob pattern(`*.png`) as well Single looping image as as input to its [`source`](../../reference/sourcer/params/#source) parameter. See this [Basic Recipe :material-pot-steam: ➶](../../basic/decode-image-sequences/#decoding-image-sequences) for more information."

```python
# import the necessary packages
from deffcode import FFdecoder
from vidgear.gears import WriteGear
import cv2, json

# define mandelbrot pattern generator
# and the Video Filter definition
ffparams = {
    "-ffprefixes": [
        "-t", "10", # playback time of 10 seconds for mandelbrot pattern
        "-f", "lavfi", # use input virtual device
        "-i", "mandelbrot=rate=25", # create mandelbrot pattern at 25 fps
        "-t", "10", # playback time of 10 seconds for video
    ],  
    "-custom_resolution": (1280, 720), # resize to 1280x720
    "-filter_complex":"[1:v]format=yuv444p[v1];" # change 2nd(video) input format to yuv444p
        + "[0:v]format=gbrp10le[v0];" # change 1st(mandelbrot pattern) input format to gbrp10le
        + "[v1][v0]scale2ref[v1][v0];" # resize the 1st(mandelbrot pattern), based on a 2nd(video).
        + "[v0][v1]blend=all_mode='heat'," # apply heat blend mode to output
        + "format=yuv422p10le[v]", # change output format to `yuv422p10le`
    "-map": "[v]", # map the output
}

# initialize and formulate the decoder with suitable source
decoder = FFdecoder(
    "/path/to/image-%03d.png", frame_format="bgr24", verbose=True, **ffparams
).formulate()

# define your parameters
# [WARNING] framerate must match original source framerate !!!
output_params = {
    "-input_framerate": 25,  # Default
}

# Define writer with default parameters and suitable
# output filename for e.g. `output_foo.mp4`
writer = WriteGear(output_filename="output_foo.mp4", logging=True, **output_params)

# grab the BGR24 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing BGR24 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.close()
```

&nbsp;