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

# Advanced Recipes :microscope:


!!! quote "This is a continuation of the [Basic Recipes ➶](../basic/). Thereby, It's advised to first read through that before reading through this documentation."


!!! warning "Important Information"

    * DeFFcode APIs **MUST** requires FFmpeg executable present in path. Follow these dedicated [Installation Instructions ➶](../../installation/ffmpeg_install/) for its installation.

    * ==All DeFFcode APIs will raise `RuntimeError` if they fails to detect valid FFmpeg executable on your system!==

    * Always use [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) function at the end with FFdecoder API to avoid undesired behavior.

&thinsp;

## Generating Video with Complex Filter Applied

FFdecoder API also provides extensive support for [FFmpeg's Video Filter](http://www.ffmpeg.org/ffmpeg-filters.html#Video-Filters) through `-filter_complex` FFmpeg parameter to its real-time generated frames, thereby lets you build a **Complex Filtergraph**, applying different filter chains to different inputs and using their outputs as inputs for other filter chains.

In this example we will apply a Custom Watermark Image(`"watermark.png"`) Overlay with additional Video Filter definitions to real-time frames in FFdecoder API through `-filter_complex` FFmpeg parameter, and generate output video using OpenCV Library's `VideoWriter()` class.

!!! info "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps Source Metadata as JSON to retrieve source framerate and frame-size."

!!! alert "OpenCV expects `BGR` format frames in its `write(frame)` function."

!!! tip "To learn about exclusive `-clones` parameter. See [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)"

```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# define the Complex Video Filter with additional `watermark.png` image input
extraparams = {
    "-clones": ["-i", "watermark.png"],  # define your `watermark.png` here
    "-filter_complex": "[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=W-w-5:H-h-5:format=auto,format=bgr24"
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "input_foo.mp4", frame_format="bgr24", verbose=True, **extraparams
).formulate()

# retrieve JSON Metadata and convert it to dict
metadata_dict = json.loads(decoder.metadata)

# prepare OpenCV parameters
FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
FRAMERATE = metadata_dict["source_video_framerate"]
FRAMESIZE = tuple(metadata_dict["source_video_resolution"])

# Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

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
writer.release()
```

&nbsp;

## Generating Lossless Video using VidGear Library

!!! danger "==WriteGear's FFmpeg support for FFdecoder API is still in beta and can cause very high CPU usage.== Kindly use [**OpenCV's VideoWriter Class**](../basic/#generating-video-from-frames-using-opencv-library) until this issue is resolved."

??? abstract "Reasons to use VidGear and its WriteGear API?"
    >  [VidGear](https://abhitronix.github.io/vidgear/latest/) is a cross-platform High-Performance Video-Processing Framework for building complex real-time media applications in python 🔥 

    VidGear with its [**WriteGear API**](https://abhitronix.github.io/vidgear/latest/gears/writegear/introduction/) implements a complete, flexible, and robust wrapper around FFmpeg in [compression mode](https://abhitronix.github.io/vidgear/latest/gears/writegear/compression/overview/) that can process real-time NumPy frames into a lossless compressed video-files.

> DeFFcode's FFdecoder with WriteGear API creates **powerful high-level FFmpeg Transcoding(Decoding + Encoding) Pipeline :zap:** that provide us the freedom to do almost anything imaginable with multimedia data in real-time. 

FFdecoder is designed exclusively to work seamlessly with WriteGear API for encoding lossless compressed video-file with any suitable specifications _(such as bitrate, codec, framerate, resolution, subtitles, etc.)_. 

In this example we will generate lossless video with controlled framerate:


!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps Source Metadata as JSON to retrieve source framerate."

??? warning "Default `BGR` format in WriteGear API"
    WriteGear API by default expects `BGR` format frames in its `write(frame)` function. However you can use [`rgb_mode`](https://abhitronix.github.io/vidgear/latest/bonus/reference/writegear/#vidgear.gears.writegear.WriteGear.write) boolean parameter for **RGB Mode**, which when enabled _(i.e. `rgb_mode=True`)_, makes WriteGear API accept frames of `RGB` format instead.

=== "Save "BGR" Video"

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json

    # initialize and formulate the decoder for BGR24 output
    decoder = FFdecoder("input_foo.mp4", frame_format="bgr24", verbose=True).formulate()

    # retrieve framerate from source JSON Metadata and pass it as `-input_framerate` 
    # parameter for controlled output framerate
    output_params = {
        "-input_framerate": json.loads(decoder.metadata)["source_video_framerate"]
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo.mp4`
    writer = WriteGear(output_filename="output_foo.mp4", **output_params)

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

=== "Save "RGB" Video"

    !!! info "Use [`rgb_mode`](https://abhitronix.github.io/vidgear/latest/bonus/reference/writegear/#vidgear.gears.writegear.WriteGear.write) boolean parameter to write `RGB24` format in WriteGear API."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json

    # initialize and formulate the decoder
    decoder = FFdecoder("input_foo.mp4", verbose=True).formulate()

    # retrieve framerate from source JSON Metadata and pass it as `-input_framerate` 
    # parameter for controlled output framerate
    output_params = {
        "-input_framerate": json.loads(decoder.metadata)["source_video_framerate"]
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo.mp4`
    writer = WriteGear(output_filename="output_foo.mp4", **output_params)

    # grab the BGR24 frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}

        # writing RGB24 frame to writer
        writer.write(frame, rgb_mode=True)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```

=== "Save "GRAYSCALE" Video"

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json

    # initialize and formulate the decoder for GRAYSCALE output
    decoder = FFdecoder("input_foo.mp4", frame_format="gray", verbose=True).formulate()

    # retrieve framerate from source JSON Metadata and pass it as `-input_framerate` parameter
    # for controlled output framerate
    output_params = {
        "-input_framerate": json.loads(decoder.metadata)["source_video_framerate"]
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo_gray.mp4`
    writer = WriteGear(output_filename="output_foo_gray.mp4", **output_params)

    # grab the GRAYSCALE frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}

        # writing GRAYSCALE frame to writer
        writer.write(frame)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```

&nbsp;

## Generating Video from Image sequence

!!! danger "==WriteGear's FFmpeg support for FFdecoder API is still in beta and can cause very high CPU usage.== Kindly use [**OpenCV's VideoWriter Class**](../basic/#generating-video-from-frames-using-opencv-library) until this issue is resolved."

FFdecoder API provides out-of-the-box support for image sequence such as Sequential(`'img%03d.png'`), Glob pattern(`'*.png'`), and even Single(looping) image as input to its [`source`](../../reference/sourcer/params/#source) parameter.

In this example we will generate grayscale video from Image Sequence using FFdecoder(Decoder) and WriteGear(Encoder) APIs:

??? abstract "Reasons to use VidGear and its WriteGear API?"
    >  [VidGear](https://abhitronix.github.io/vidgear/latest/) is a cross-platform High-Performance Video-Processing Framework for building complex real-time media applications in python 🔥 

    VidGear with its [**WriteGear API**](https://abhitronix.github.io/vidgear/latest/gears/writegear/introduction/) implements a complete, flexible, and robust wrapper around FFmpeg in [compression mode](https://abhitronix.github.io/vidgear/latest/gears/writegear/compression/overview/) that can process real-time NumPy frames into a lossless compressed video-files.

??? tip "Extracting Image Sequence from a video"
    
    **You can use following command to extract frames from a given video:**
    
    ```sh
    ffmpeg -i foo.mp4 image-%03d.png
    ```
    This will extract `25` images per second from the file video.webm and save them as `image-000.png`, `image-001.png`, `image-002.png` up to `image-999.png`. If there are more than `1000` frames then the last image will be overwritten with the remaining frames leaving only the last frame. The encoding of the images and of the video is inferred from the extensions. The framerate is `25` fps by default. The images width and height is taken from the video.

    **Extract one image per second:**

    ```sh
    ffmpeg -i video.webm -framerate 1 image-%03d.png #
    ```

!!! note "To learn about exclusive `-ffprefixes` parameter. See [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)"

=== "Sequential"

    ??? tip "Start with specific number image"
        You can use `-start_number` FFmpeg parameter if you want to start with specific number image:

        ```python
        # define `-start_number` such as `5`
        extraparams = {"-ffpostfixes":["-start_number", "5"]}

        # initialize and formulate the decoder with define parameters
        decoder = FFdecoder('img%03d.png', verbose=True, **extraparams).formulate()
        ```

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import cv2

    # initialize and formulate the decode with suitable source
    decoder = FFdecoder("/path/to/pngs/img%03d.png", verbose=True).formulate()

    # pass controlled input framerate
    # `-framerate 25` means each image is taken at 1/25^th of a second
    # Or images are extracted from video at 25fps
    output_params = {
        "-ffpreheaders": ["-framerate", "25"], 
        "-clones": ["-shortest"],
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo_gray.mp4`
    writer = WriteGear(output_filename="output_foo_gray.mp4", **output_params)

    # grab the GRAYSCALE frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}
        # lets convert frame to gray for this example
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # writing GRAYSCALE frame to writer
        writer.write(gray)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```

    

=== "Glob pattern"

    !!! abstract "Bash-style globbing _(`*` represents any number of any characters)_ is useful if your images are sequential but not necessarily in a numerically sequential order."

    !!! warning "The glob pattern is not available on Windows builds."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import cv2

    # define `-pattern_type glob` for accepting glob pattern
    extraparams = {"-ffprefixes":["-pattern_type", "glob"]}

    # initialize and formulate the decode with suitable source
    decoder = FFdecoder("/path/to/pngs/img*.png", verbose=True, **extraparams).formulate()

    # pass controlled input framerate
    # `-framerate 25` means each image is taken at 1/25^th of a second
    # Or images are extracted from video at 25fps
    output_params = {
        "-ffpreheaders": ["-framerate", "25"], 
        "-clones": ["-shortest"],
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo_gray.mp4`
    writer = WriteGear(output_filename="output_foo_gray.mp4", **output_params)

    # grab the GRAYSCALE frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}
        # lets convert frame to gray for this example
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # writing GRAYSCALE frame to writer
        writer.write(gray)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```

=== "Single image(looping)"

    You can use a single looping image as follows:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import cv2

    # define `-loop 1` for looping
    extraparams = {"-ffprefixes":["-loop", "1"]}

    # initialize and formulate the decode with suitable source
    decoder = FFdecoder("img.png", verbose=True, **extraparams).formulate()

    # pass controlled input framerate
    # `-framerate 25` means each image is taken at 1/25^th of a second
    # Or images are extracted from video at 25fps
    output_params = {
        "-ffpreheaders": ["-framerate", "25"], 
        "-clones": ["-shortest"],
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo_gray.mp4`
    writer = WriteGear(output_filename="output_foo_gray.mp4", **output_params)

    # grab the GRAYSCALE frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}
        # lets convert frame to gray for this example
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # writing GRAYSCALE frame to writer
        writer.write(gray)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```


&nbsp;

## GPU enabled Hardware-Accelerated Decoding

By default, FFdecoder API uses **Source Video's decoder** _(extracted using Sourcer API)_ for decoding input. But you can easily change it to your suitable [**supported decoder**](../../reference/ffdecoder/params/#supported-decoders) through `-vcodec` FFmpeg parameter by passing it as an attribute with FFdecoder's [`extraparams`](../../reference/ffdecoder/params/#extraparams) dictionary parameter. In addition to this, you can also specify the additional properties/features of your system's GPU :octicons-cpu-16: easily. 

!!! warning "User Discretion Advised"

    This example is just conveying the idea on how to use FFmpeg's hardware decoders with FFdecoder API, which **MAY/MAY NOT** suit your system. Kindly use suitable parameters based your system hardware settings only.


In this example, we will be using NVIDIA's CUVID `"h264_cuvid"` as our hardware decoder and also optionally be specifying other features such as `–hwaccel cuvid` and filters like `-vf "fade,hwupload_cuda,scale_npp=1280:720"`. Thereby displaying the output frames with OpenCV's `imshow()`:

!!! info "More information on NVIDIA's CUVID can be found [here ➶](https://developer.nvidia.com/blog/nvidia-ffmpeg-transcoding-guide/)"

??? alert "Remember to check NVIDIA's CUVID support in FFmpeg"

    To use `h264_cuvid` decoder, remember to check if its available and your FFmpeg compiled with CUVID support. You can easily do this by executing following one-liner command in your terminal, and observing if output contains something similar as follows:

    ```sh
    ffmpeg  -hide_banner -encoders | grep h264 

    VFS..D h264                 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10
    V....D h264_qsv             H264 video (Intel Quick Sync Video acceleration) (codec h264)
    V..... h264_cuvid           Nvidia CUVID H264 decoder (codec h264)
    ```

!!! tip "To learn about exclusive `-ffprefixes` and `-ffpostfixes` parameters. See [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)"

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define suitable FFmpeg parameter
extraparams = {
    "-ffprefixes": ["–hwaccel", "cuvid"],
    "-ffpostfixes": ["-vf", "fade,hwupload_cuda,scale_npp=1280:720"],
}

# initialize and formulate the decode with suitable source and params
decoder = FFdecoder("foo.mp4", frame_format="bgr24", verbose=True, **extraparams).formulate()

# grab the RGB24(default) frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

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