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

# :material-video-image: Transcoding Live frames

??? abstract "What exactly is Transcoding?"

    Before heading directly into recipes we have to talk about Transcoding: 
    
    > Transcoding is the technique of transforming one media encoding format into another. 

    This is typically done for compatibility purposes, such as when a media source provides a format that the intended target is not able to process; an in-between adaptation step is required:

    - **Decode** media from its originally encoded state into raw, uncompressed information.
    - **Encode** the raw data back, using a different codec that is supported by end user.


> While decoding media into video frames is purely managed by DeFFcode's FFdecoder API, you can easily encode those video frames back into multimedia files using any well-known video processing library such as OpenCV and VidGear. 

We'll discuss transcoding using both these libraries briefly in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

??? info "Additional Python Dependencies for following recipes"

    Following recipes requires additional python dependencies which can be installed easily as below:

    - [x] **OpenCV:** OpenCV is required for previewing and encoding video frames. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ??? tip "OpenCV installation from source"

            You can also follow online tutorials for building & installing OpenCV on [Windows](https://www.learnopencv.com/install-opencv3-on-windows/), [Linux](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/), [MacOS](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) and [Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) machines manually from its source. 

            :warning: Make sure not to install both *pip* and *source* version together. Otherwise installation will fail to work!

        ??? info "Other OpenCV binaries"

            OpenCV maintainers also provide additional binaries via pip that contains both main modules and contrib/extra modules [`opencv-contrib-python`](https://pypi.org/project/opencv-contrib-python/), and for server (headless) environments like [`opencv-python-headless`](https://pypi.org/project/opencv-python-headless/) and [`opencv-contrib-python-headless`](https://pypi.org/project/opencv-contrib-python-headless/). You can also install ==any one of them== in similar manner. More information can be found [here](https://github.com/opencv/opencv-python#installation-and-usage).


        ```sh
        pip install opencv-python       
        ```

    - [x] **VidGear:** VidGear is required for lossless encoding of video frames into file/stream. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ```sh
        pip install vidgear[core]       
        ```



!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## Transcoding video using OpenCV VideoWriter API

!!! quote "OpenCV's' [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) class can be used directly with DeFFcode's FFdecoder API to encode video frames into a multimedia video file but it lacks the ability to control output quality, bitrate, compression, and other important features which are only available with VidGear's WriteGear API."

In this example we will decode different pixel formats video frames from a given Video file _(say `foo.mp4`)_ in FFdecoder API, and encode them using OpenCV Library's `VideoWriter()` method in real-time. 

!!! info "OpenCV's `VideoWriter()` class requires a valid Output filename _(e.g. output_foo.avi)_, [FourCC](https://www.fourcc.org/fourcc.php) code, framerate, and resolution as input."

!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve output framerate and resolution."

=== "BGR frames"

    By default, OpenCV expects `BGR` format frames in its `cv2.write()` method.

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import json, cv2

    # initialize and formulate the decoder for BGR24 pixel format output
    decoder = FFdecoder("foo.mp4", frame_format="bgr24").formulate()

    # retrieve JSON Metadata and convert it to dict
    metadata_dict = json.loads(decoder.metadata)

    # prepare OpenCV parameters
    FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
    FRAMERATE = metadata_dict["output_framerate"]
    FRAMESIZE = tuple(metadata_dict["output_frames_resolution"])

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

         # let's also show output window
        cv2.imshow("Output", frame)

        # check for 'q' key if pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # close output window
    cv2.destroyAllWindows()

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.release()
    ```

=== "RGB frames"

    Since OpenCV expects `BGR` format frames in its `cv2.write()` method, therefore we need to convert `RGB` frames into `BGR` before encoding as follows:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import json, cv2

    # initialize and formulate the decoder for RGB24 pixel format output
    decoder = FFdecoder("foo.mp4").formulate()

    # retrieve JSON Metadata and convert it to dict
    metadata_dict = json.loads(decoder.metadata)

    # prepare OpenCV parameters
    FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
    FRAMERATE = metadata_dict["output_framerate"]
    FRAMESIZE = tuple(metadata_dict["output_frames_resolution"])

    # Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
    writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

    # grab the RGB24 frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}

        # converting RGB24 to BGR24 frame
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # writing BGR24 frame to writer
        writer.write(frame_bgr)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.release()
    ```

=== "GRAYSCALE frames"

    OpenCV also directly consumes `GRAYSCALE` frames in its `cv2.write()` method.

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import json, cv2

    # initialize and formulate the decoder for GRAYSCALE output
    decoder = FFdecoder("foo.mp4", frame_format="gray", verbose=True).formulate()

    # retrieve JSON Metadata and convert it to dict
    metadata_dict = json.loads(decoder.metadata)

    # prepare OpenCV parameters
    FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
    FRAMERATE = metadata_dict["output_framerate"]
    FRAMESIZE = tuple(metadata_dict["output_frames_resolution"])

    # Define writer with parameters and suitable output filename for e.g. `output_foo_gray.avi`
    writer = cv2.VideoWriter("output_foo_gray.avi", FOURCC, FRAMERATE, FRAMESIZE)

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
    writer.release()
    ```

=== "YUV frames"

    !!! abstract "With FFdecoder API, frames extracted with YUV pixel formats _(`yuv420p`, `yuv444p`, `nv12`, `nv21` etc.)_ are generally incompatible with OpenCV APIs. But you can make them easily compatible by using exclusive [`-enforce_cv_patch`](../../reference/ffdecoder/params/#b-exclusive-parameters) boolean attribute of its `ffparam` dictionary parameter."

    Let's try encoding YUV420p pixel-format frames with OpenCV's `write()` method in following python code:

    !!! info "You can also use other YUV pixel-formats such `yuv422p`(4:2:2 subsampling) or `yuv444p`(4:4:4 subsampling) etc. instead for more higher dynamic range in the similar manner."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import json, cv2

    # enable OpenCV patch for YUV frames
    ffparams = {"-enforce_cv_patch": True}

    # initialize and formulate the decoder for YUV420p output
    decoder = FFdecoder(
        "input_foo.mp4", frame_format="yuv420p", verbose=True, **ffparams
    ).formulate()

    # retrieve JSON Metadata and convert it to dict
    metadata_dict = json.loads(decoder.metadata)

    # prepare OpenCV parameters
    FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
    FRAMERATE = metadata_dict["output_framerate"]
    FRAMESIZE = tuple(metadata_dict["output_frames_resolution"])

    # Define writer with parameters and suitable output filename for e.g. `output_foo_gray.avi`
    writer = cv2.VideoWriter("output_foo_gray.avi", FOURCC, FRAMERATE, FRAMESIZE)

    # grab the yuv420p frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # convert it to `BGR` pixel format,
        # since imshow() method only accepts `BGR` frames
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

        # {do something with the BGR frame here}

        # writing BGR frame to writer
        writer.write(frame)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.release()
    ```

&nbsp;

## Transcoding lossless video using WriteGear API

!!! danger "==WriteGear's Compression Mode support for FFdecoder API is currently in beta so you can expect much higher than usual CPU utilization!=="

???+ quote "Lossless transcoding  with FFdecoder and WriteGear API"
    
    VidGear's [**WriteGear API**](https://abhitronix.github.io/vidgear/latest/gears/writegear/introduction/) implements a complete, flexible, and robust wrapper around FFmpeg in [compression mode](https://abhitronix.github.io/vidgear/latest/gears/writegear/compression/overview/) for encoding real-time video frames to a lossless compressed multimedia output file(s)/stream(s). 

    DeFFcode's FFdecoder API in conjunction with WriteGear API creates a high-level **High-performance Lossless FFmpeg Transcoding _(Decoding + Encoding)_ Pipeline :fire:** that is able to exploit almost any FFmpeg parameter for achieving anything imaginable with multimedia video data all while allow us to manipulate the real-time video frames with immense flexibility. 

In this example we will decode different pixel formats video frames from a given Video file _(say `foo.mp4`)_ in FFdecoder API, and encode them into lossless video file with controlled framerate using WriteGear API in real-time. 

!!! info "Additional Parameters in WriteGear API"
    
    WriteGear API only requires a valid Output filename _(e.g. `output_foo.mp4`)_ as input, but you can easily control any output specifications _(such as bitrate, codec, framerate, resolution, subtitles, etc.)_ supported by FFmpeg _(in use)_.

!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate."

=== "BGR frames"

    WriteGear API by default expects `BGR` format frames in its `write()` class method.

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json

    # initialize and formulate the decoder for BGR24 output
    decoder = FFdecoder("foo.mp4", frame_format="bgr24", verbose=True).formulate()

    # retrieve framerate from source JSON Metadata and pass it as `-input_framerate` 
    # parameter for controlled framerate
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

=== "RGB frames"

    In WriteGear API, you can use [`rgb_mode`](https://abhitronix.github.io/vidgear/latest/bonus/reference/writegear/#vidgear.gears.writegear.WriteGear.write) parameter in  `write()` class method to write `RGB` format frames instead of default `BGR` as follows:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json

    # initialize and formulate the decoder
    decoder = FFdecoder("foo.mp4", verbose=True).formulate()

    # retrieve framerate from source JSON Metadata and pass it as `-input_framerate` 
    # parameter for controlled framerate
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

=== "GRAYSCALE frames"

    WriteGear API also directly consumes `GRAYSCALE` format frames in its `write()` class method. 

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json

    # initialize and formulate the decoder for GRAYSCALE output
    decoder = FFdecoder("foo.mp4", frame_format="gray", verbose=True).formulate()

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

=== "YUV frames"

    WriteGear API also directly consume `YUV` _(or basically any other supported pixel format)_ frames in its `write()` class method with its `-input_pixfmt` attribute in compression mode. For its  non-compression mode, see [above example](#transcoding-video-using-opencv-videowriter-api).

    !!! note "You can also use `yuv422p`(4:2:2 subsampling) or `yuv444p`(4:4:4 subsampling) instead for more higher dynamic ranges."

    !!! alert "In WriteGear API, the support for `-input_pixfmt` attribute in `output_params` dictionary parameter was added in `v0.3.0`."

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json

    # initialize and formulate the decoder for YUV420 output
    decoder = FFdecoder("foo.mp4", frame_format="yuv420p").formulate()

    # retrieve framerate from source JSON Metadata and pass it as 
    # `-input_framerate` parameter for controlled framerate
    # and add input pixfmt as yuv420p also
    output_params = {
        "-input_framerate": json.loads(decoder.metadata)["output_framerate"],
        "-input_pixfmt": "yuv420p"
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo_yuv.mp4`
    writer = WriteGear(output_filename="output_foo_yuv.mp4", logging=True, **output_params)

    # grab the YUV420 frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the frame here}

        # writing YUV420 frame to writer
        writer.write(frame)

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```

&nbsp;
