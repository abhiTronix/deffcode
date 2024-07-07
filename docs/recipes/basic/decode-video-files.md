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

=== "Decode YUV frames"

    !!! quote "With FFdecoder API, frames extracted with YUV pixel formats _(`yuv420p`, `yuv444p`, `nv12`, `nv21` etc.)_ are generally incompatible with OpenCV APIs. But you can make them easily compatible by using exclusive [`-enforce_cv_patch`](../../reference/ffdecoder/params/#b-exclusive-parameters) boolean attribute of its `ffparam` dictionary parameter."

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
