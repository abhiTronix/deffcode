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

# :material-webcam: Decoding Camera Devices using Indexes

> With DeFFcode APIs, we are able to probe and enumerate all Camera Devices names along with their respective "device indexes" or "camera indexes" no matter how many cameras are connected to your system. This makes Camera Devices decoding as simple as [**OpenCV**](https://opencv.org/), where one can effortlessly access a specific Camera Device just by the specifying the matching index of it. These indexes are much easier to read, memorize, and type, and one don't have to remember long Device names or worry about its Demuxer. 

We'll discuss the Decoding Camera Devices using Indexes briefly in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

???+ info "Additional Python Dependencies for following recipes"

    Following recipes requires additional python dependencies which can be installed easily as below:

    - [x] **OpenCV:** OpenCV is required for previewing video frames. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ??? tip "OpenCV installation from source"

            You can also follow online tutorials for building & installing OpenCV on [Windows](https://www.learnopencv.com/install-opencv3-on-windows/), [Linux](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/), [MacOS](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) and [Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) machines manually from its source. 

            :warning: Make sure not to install both *pip* and *source* version together. Otherwise installation will fail to work!

        ??? info "Other OpenCV binaries"

            OpenCV mainainers also provide additional binaries via pip that contains both main modules and contrib/extra modules [`opencv-contrib-python`](https://pypi.org/project/opencv-contrib-python/), and for server (headless) environments like [`opencv-python-headless`](https://pypi.org/project/opencv-python-headless/) and [`opencv-contrib-python-headless`](https://pypi.org/project/opencv-contrib-python-headless/). You can also install ==any one of them== in similar manner. More information can be found [here](https://github.com/opencv/opencv-python#installation-and-usage).


        ```sh
        pip install opencv-python       
        ```


!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## Enumerating all Camera Devices with Indexes

> In Sourcer API, you can easily use its [`enumerate_devices`](../../../reference/sourcer/#deffcode.sourcer.Sourcer.enumerate_devices) property object to enumerate all probed Camera Devices _(connected to your system)_ as **dictionary object** with device indexes as keys and device names as their respective values. 

??? danger "Requirement for Enumerating all Camera Devices in Sourcer API"

    - [x] **MUST have appropriate FFmpeg binaries, Drivers, and Softwares installed:**
        
        Internally, DeFFcode APIs achieves Index based Camera Device Capturing by employing some specific FFmpeg demuxers on different platforms(OSes). These platform specific demuxers are as follows:

        | Platform(OS) | Demuxer |
        |:------------:|:-------|
        | :fontawesome-brands-windows: Windows OS|[`dshow`](https://trac.ffmpeg.org/wiki/DirectShow) _(or DirectShow)_ |
        | :material-linux: Linux OS | [`video4linux2`](https://trac.ffmpeg.org/wiki/Capture/Webcam#Linux) _(or its alias `v4l2`)_ |
        | :material-apple: Mac OS | [`avfoundation`](https://ffmpeg.org/ffmpeg-devices.html#avfoundation) |

        **:warning: Important:** Kindly make sure your FFmpeg binaries support these platform specific demuxers as well as system have the appropriate video drivers and related softwares installed.

    - [x] The [`source`](../../../reference/sourcer/params/#source) parameter value **MUST be any Camera Device index** that can be of either **integer** _(e.g. `-1`,`0`,`1`, etc.)_ or **string of integer** _(e.g. `"-1"`,`"0"`,`"1"`, etc.)_ type.

    - [x] The [`source_demuxer`](../../../reference/sourcer/params/#source_demuxer) parameter value  **MUST be either `None`_(also means empty)_ or `"auto"`**. 

In this example we will enumerate all probed Camera Devices connected on a :fontawesome-brands-windows: Windows machine using [`enumerate_devices`](../../../reference/sourcer/#deffcode.sourcer.Sourcer.enumerate_devices) property object in Sourcer API, both as dictionary object and JSON string.

```python
# import the necessary packages
from deffcode import Sourcer
import json

# initialize and formulate the decoder
sourcer = Sourcer("0").probe_stream()

# enumerate probed devices as Dictionary object(`dict`)
print(sourcer.enumerate_devices)

# enumerate probed devices as JSON string(`json.dump`)
print(json.dumps(sourcer.enumerate_devices,indent=2))
```

???+ abstract "After running above python code, the resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"

    === "As Dictionary object"

        ```python
        {0: 'Integrated Camera', 1: 'USB2.0 Camera', 2: 'DroidCam Source'}
        ```
    
    === "As JSON string"

        ```json
        {
          "0": "Integrated Camera",
          "1": "USB2.0 Camera",
          "2": "DroidCam Source"
        }
        ```

&nbsp;

## Capturing and Previewing frames from a Camera using Indexes

> After knowing the index of Camera Device with Sourcer API, One can easily Capture desired Camera Device in FFdecoder API by specifying its matching index value either as **integer** or **string of integer** type to its `source` parameter.

??? danger "Requirement for Index based Camera Device Capturing in FFdecoder API"

    - [x] **MUST have appropriate FFmpeg binaries, Drivers, and Softwares installed:**
        
        Internally, DeFFcode APIs achieves Index based Camera Device Capturing by employing some specific FFmpeg demuxers on different platforms(OSes). These platform specific demuxers are as follows:

        | Platform(OS) | Demuxer |
        |:------------:|:-------|
        | :fontawesome-brands-windows: Windows OS|[`dshow`](https://trac.ffmpeg.org/wiki/DirectShow) _(or DirectShow)_ |
        | :material-linux: Linux OS | [`video4linux2`](https://trac.ffmpeg.org/wiki/Capture/Webcam#Linux) _(or its alias `v4l2`)_ |
        | :material-apple: Mac OS | [`avfoundation`](https://ffmpeg.org/ffmpeg-devices.html#avfoundation) |

        **:warning: Important:** Kindly make sure your FFmpeg binaries support these platform specific demuxers as well as system have the appropriate video drivers and related softwares installed.
    - [x] The [`source`](../../../reference/ffdecoder/params/#source) parameter value **MUST be exactly the probed Camera Device index** _(use Sourcer API's [`enumerate_devices`](../../../reference/sourcer/#deffcode.sourcer.Sourcer.enumerate_devices) to list them)_.
    - [x] The [`source_demuxer`](../../../reference/ffdecoder/params/#source_demuxer) parameter value  **MUST be either `None`_(also means empty)_ or `"auto"`**. 

In this example we will decode **BGR24** video frames from **Integrated Camera at index `0`** on a Windows Machine, and preview them using OpenCV Library's `cv2.imshow()` method.

??? tip "Important Facts related to Camera Device Indexing"
    - [x] **Camera Device indexes are 0-indexed**. So the first device is at `0`, second is at `1`, so on. So if the there are `n` devices, the last device is at `n-1`.
    - [x] **Camera Device indexes can be of either integer** _(e.g. `0`,`1`, etc.)_ or **string of integer** _(e.g. `"0"`,`"1"`, etc.)_ **type**.
    - [x] **Camera Device indexes can be negative** _(e.g. `-1`,`-2`, etc.)_, this means you can also start indexing from the end.
        * For example, If there are three devices: 
            ```python
            {0: 'Integrated Camera', 1: 'USB2.0 Camera', 2: 'DroidCam Source'}
            ```
        * Then, You can specify Positive Indexes and its Equivalent Negative Indexes as follows:

            | Positive Indexes | Equivalent Negative Indexes |
            |:------------:|:-------:|
            | `#!python FFdecoder("0").formulate()`| `#!python FFdecoder("-3").formulate()` |
            | `#!python FFdecoder("1").formulate()`| `#!python FFdecoder("-2").formulate()` |
            | `#!python FFdecoder("2").formulate()`| `#!python FFdecoder("-1").formulate()` |

    !!! warning "Out of Index Camera Device index values will raise `ValueError` in FFdecoder API"

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# initialize and formulate the decoder with "0" index source for BGR24 output
decoder = FFdecoder("0", frame_format="bgr24", verbose=True).formulate()

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

<!--
External URLs
-->
[gitter]: https://gitter.im/deffcode-python/community