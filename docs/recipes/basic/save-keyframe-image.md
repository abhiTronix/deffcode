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

# :material-fast-forward-60: Saving Key-frames as Image


> DeFFcode's FFdecoder API provide effortless and precise **Frame Seeking** with `-ss` FFmpeg parameter that enable us to save any frame from a specific part of our input source.  

We'll discuss aboout it briefly in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

???+ info "Additional Python Dependencies for following recipes"

    Following recipes requires additional python dependencies which can be installed easily as below:

    - [x] **OpenCV:** OpenCV is required for saving video frames. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ??? tip "OpenCV installation from source"

            You can also follow online tutorials for building & installing OpenCV on [Windows](https://www.learnopencv.com/install-opencv3-on-windows/), [Linux](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/), [MacOS](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) and [Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) machines manually from its source. 

            :warning: Make sure not to install both *pip* and *source* version together. Otherwise installation will fail to work!

        ??? info "Other OpenCV binaries"

            OpenCV mainainers also provide additional binaries via pip that contains both main modules and contrib/extra modules [`opencv-contrib-python`](https://pypi.org/project/opencv-contrib-python/), and for server (headless) environments like [`opencv-python-headless`](https://pypi.org/project/opencv-python-headless/) and [`opencv-contrib-python-headless`](https://pypi.org/project/opencv-contrib-python-headless/). You can also install ==any one of them== in similar manner. More information can be found [here](https://github.com/opencv/opencv-python#installation-and-usage).


        ```sh
        pip install opencv-python       
        ```

    - [x] **Pillow:** Pillow is a Imaging Library required for saving frame as Image. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ```sh
        pip install Pillow     
        ```

    - [x] **Matplotlib:** Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations, also required for saving frame as Image. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ```sh
        pip install matplotlib   
        ```

    - [x] **Imageio:** Imageio is a Library for reading and writing a wide range of image, video, scientific, and volumetric data formats, also required for saving frame as Image. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ```sh
        pip install imageio      
        ```


!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## Extracting Key-frames as PNG image

In this example we will seek to `00:00:01.45`_(or 1045msec)_ in time and decode one single frame in FFdecoder API, and thereby saving it as PNG image using few prominent Image processing python libraries by providing valid filename _(e.g. `foo_image.png`)_.

??? tip "Time unit syntax in `-ss` FFmpeg parameter"
    
    You can use two different time unit formats with `-ss` FFmpeg parameter: 
    - [x] **Sexagesimal(in seconds):** Uses *(HOURS:MM:SS.MILLISECONDS)*, such as in `01:23:45.678`
    - [x] **Fractional:** such as in `02:30.05`, this is interpreted as 2 minutes, 30 seconds, and a half a second, which would be the same as using 150.5 in seconds.

=== "Using Pillow"

    In Pillow, the `fromarray()` function can be used to create an image memory from an **RGB** frame:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from PIL import Image

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec)
    # in time and get one single frame
    ffparams = {"-ss": "00:00:01.45", "-frames:v": 1}

    # initialize and formulate the decoder with suitable source
    decoder = FFdecoder("foo.mp4", **ffparams).formulate()

    # grab the RGB24(default) frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not (frame is None):
        # Convert to Image
        im = Image.fromarray(frame)
        # Save Image as PNG
        im.save("foo_image.png")
    else:
        raise ValueError("Something is wrong!")

    # terminate the decoder
    decoder.terminate()
    ```

=== "Using OpenCV"

    In OpenCV, the `imwrite()` function can export **BGR** frame as an image file:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec) 
    # in time and get one single frame
    ffparams = {"-ss": "00:00:01.45", "-frames:v":1}

    # initialize and formulate the decoder for BGR24 outputwith suitable source
    decoder = FFdecoder("foo.mp4", frame_format="bgr24", **ffparams).formulate()

    # grab the BGR24 frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not(frame is None):
        # Save our image as PNG
        cv2.imwrite('foo_image.png', frame)
    else:
        raise ValueError("Something is wrong!")

    # terminate the decoder
    decoder.terminate()
    ```

=== "Using Matplotlib"

    In Matplotlib, the `imsave()` function can save an **RGB** frame as an image file:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import matplotlib.pyplot as plt

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec) 
    # in time and get one single frame
    ffparams = {"-ss": "00:00:01.45", "-frames:v":1}

    # initialize and formulate the decoder with suitable source
    decoder = FFdecoder("foo.mp4", **ffparams).formulate()

    # grab the RGB24(default) frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not(frame is None):
        # Save our image as PNG
        plt.imsave('foo_image.png', frame)
    else:
        raise ValueError("Something is wrong!")

    # terminate the decoder
    decoder.terminate()
    ```

=== "Using Imageio"

    In Imageio, the `imwrite()` function can be used to create an image memory from an **RGB** frame:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import imageio

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec) 
    # in time and get one single frame
    ffparams = {"-ss": "00:00:01.45", "-frames:v":1}

    # initialize and formulate the decoder with suitable source
    decoder = FFdecoder("foo.mp4", **ffparams).formulate()

    # grab the RGB24(default) frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not(frame is None):
        # Save our output
        imageio.imwrite('foo_image.jpeg', frame)
    else:
        raise ValueError("Something is wrong!")

    # terminate the decoder
    decoder.terminate()
    ```

&nbsp;


## Generating Thumbnail with a Fancy filter

<figure>
<img src="../../../assets/images/fancy_thumbnail.jpg" loading="lazy" alt="fancy_thumbnail.jpg" title="fancy_thumbnail.jpg" />
<figcaption><code>fancy_thumbnail.jpg</code> (Courtesy - <a href="https://peach.blender.org/trailer-page/">BigBuckBunny</a>)</figcaption>
</figure>

In this example we first apply FFmpeg’s `tblend` filter  with an `hardmix` blend mode _(cool stuff)_ and then seek to `00:00:25.917`_(or 25.917sec)_ in time to retrieve our single frame thumbnail, and thereby save it as JPEG image with valid filename _(e.g. `fancy_thumbnail.jpg`)_ using Pillow library.

??? tip "Time unit syntax in `-ss` FFmpeg parameter"
    
    You can use two different time unit formats with `-ss` FFmpeg parameter: 
    - [x] **Sexagesimal(in seconds):** Uses *(HOURS:MM:SS.MILLISECONDS)*, such as in `01:23:45.678`
    - [x] **Fractional:** such as in `02:30.05`, this is interpreted as 2 minutes, 30 seconds, and a half a second, which would be the same as using 150.5 in seconds.

??? info "Available blend mode options" 

    **Other blend mode options for `tblend` filter include:** `addition`, `addition128`, `grainmerge`, `and`, `average`, `burn`, `darken`, `difference`, `difference128`, `grainextract`, `divide`, `dodge`, `freeze`, `exclusion`, `extremity`, `glow`, `hardlight`, `hardmix`, `heat`, `lighten`, `linearlight`, `multiply`, `multiply128`, `negation`, `normal`, `or`, `overlay`, `phoenix`, `pinlight`, `reflect`, `screen`, `softlight`, `subtract`, `vividlight`, `xor`

```python
# import the necessary packages
from deffcode import FFdecoder
from PIL import Image

# define the FFmpeg parameter to
ffparams = {
    "-vf": "tblend=all_mode='hardmix'",  # trim and reverse
    "-ss": "00:00:25.917",  # seek to 00:00:25.917(or 25s 917msec)
    "-frames:v": 1,  # get one single frame
}

# initialize and formulate the decoder with suitable source
decoder = FFdecoder("BigBuckBunny.mp4", **ffparams).formulate()

# grab the RGB24(default) frame from the decoder
frame = next(decoder.generateFrame(), None)

# check if frame is None
if not (frame is None):
    # Convert to Image
    im = Image.fromarray(frame)
    # Save Image as JPEG
    im.save("fancy_thumbnail.jpg")
else:
    raise ValueError("Something is wrong!")

# terminate the decoder
decoder.terminate()

```

&nbsp;