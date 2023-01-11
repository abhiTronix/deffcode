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

# :material-image-multiple: Decoding Image sequences

> DeFFcode's FFdecoder API supports a wide-ranging media streams as input to its [`source`](../../reference/sourcer/params/#source) parameter, which also includes **Image Sequences** such as Sequential(`img%03d.png`) and Glob pattern(`*.png`) as well as **Single looping image**. 

We'll discuss both briefly in the following recipes:

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

## Capturing and Previewing frames from Sequence of images

In this example we will capture video frames from a given Image Sequence using FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method in real-time.

!!! alert "OpenCV expects `BGR` format frames in its `cv2.imshow()` method."


??? tip "Extracting Image Sequences from a video"
    
    **You can use following FFmpeg command to extract sequences of images from a video file `foo.mp4`:**
    
    ```sh
    $ ffmpeg -i foo.mp4 /path/to/image-%03d.png
    ```

    The default framerate is `25` fps, therefore this command will extract `25 images/sec` from the video file, and save them as sequences of images _(starting from `image-000.png`, `image-001.png`, `image-002.png` up to `image-999.png`)_. 

    !!! info "If there are more than `1000` frames then the last image will be overwritten with the remaining frames leaving only the last frame."

    The default images width and height is same as the video.

=== "Sequential"

    ??? question "How to start with specific number image?"
        You can use `-start_number` FFmpeg parameter if you want to start with specific number image:

        ```python
        # define `-start_number` such as `5`
        ffparams = {"-ffprefixes":["-start_number", "5"]}

        # initialize and formulate the decoder with define parameters
        decoder = FFdecoder('img%03d.png', verbose=True, **ffparams).formulate()
        ```

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # initialize and formulate the decoder with suitable source
    decoder = FFdecoder("/path/to/pngs/img%03d.png", frame_format="bgr24", verbose=True).formulate()

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

=== "Glob pattern"

    !!! abstract "Bash-style globbing _(`*` represents any number of any characters)_ is useful if your images are sequential but not necessarily in a numerically sequential order."

    !!! warning "The glob pattern is not available on Windows FFmpeg builds."

    !!! note "To learn more about exclusive `-ffprefixes` parameter. See [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)"

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # define `-pattern_type glob` for accepting glob pattern
    ffparams = {"-ffprefixes":["-pattern_type", "glob"]}

    # initialize and formulate the decoder with suitable source
    decoder = FFdecoder("/path/to/pngs/img*.png", frame_format="bgr24", verbose=True, **ffparams).formulate()


    # grab the GRAYSCALE frame from the decoder
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

## Capturing and Previewing frames from Single looping image

In this example we will capture video frames from a Single Looping image using FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method in real-time.

!!! alert "By default, OpenCV expects `BGR` format frames in its `cv2.imshow()` method."

!!! note "To learn more about exclusive `-ffprefixes` parameter. See [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)"

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define `-loop 1` for infinite looping
ffparams = {"-ffprefixes":["-loop", "1"]}

# initialize and formulate the decoder with suitable source
decoder = FFdecoder("img.png", frame_format="bgr24", verbose=True, **ffparams).formulate()

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