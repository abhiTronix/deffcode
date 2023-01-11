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

# :material-camera-iris: Decoding Live Feed Devices

> DeFFcode's FFdecoder API provide effortless support for any Live Feed Devices using two parameters: [`source`](../../reference/sourcer/params/#source) parameter which accepts device name or its path, and [`source_demuxer`](../../reference/sourcer/params/#source_demuxer) parameter to specify demuxer for the given input device. 

We'll discuss the Live Feed Devices support using both these parameters briefly in the following recipes:

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

## Capturing and Previewing frames from a Webcam using Custom Demuxer

???+ alert "Example Assumptions"

    FFmpeg provide set of specific Demuxers on different platforms to read the multimedia streams from a particular type of Video Capture source/device. Please note that following recipe explicitly assumes: 

    - You're running Linux Machine with USB webcam connected to it at node/path `/dev/video0`. 
    - You already have appropriate Linux video drivers and related softwares installed on your machine.
    - You machine uses FFmpeg binaries built with `--enable-libv4l2` flag to support `video4linux2, v4l2` demuxer. BTW, you can list all supported demuxers using the `#!sh ffmpeg --list-demuxers` terminal command.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.


In this example we will decode **BGR24** video frames from a USB webcam device connected at path `/dev/video0` on a Linux Machine with `video4linux2` _(or simply `v4l2`)_ demuxer, and preview them using OpenCV Library's `cv2.imshow()` method.


??? tip "Identifying and Specifying Video Capture Device Name/Path/Index and suitable Demuxer on different OS platforms"

    === ":fontawesome-brands-windows: Windows"

        Windows OS users can use the [dshow](https://trac.ffmpeg.org/wiki/DirectShow) (DirectShow) to list video input device which is the preferred option for Windows users. You can refer following steps to identify and specify your input video device's name:

        - [x] **Identify Video Devices:** You can locate your video device's name _(already connected to your system)_ using `dshow` as follows:

            ```sh
            c:\> ffmpeg.exe -list_devices true -f dshow -i dummy
            
            ffmpeg version N-45279-g6b86dd5... --enable-runtime-cpudetect
              libavutil      51. 74.100 / 51. 74.100
              libavcodec     54. 65.100 / 54. 65.100
              libavformat    54. 31.100 / 54. 31.100
              libavdevice    54.  3.100 / 54.  3.100
              libavfilter     3. 19.102 /  3. 19.102
              libswscale      2.  1.101 /  2.  1.101
              libswresample   0. 16.100 /  0. 16.100
            [dshow @ 03ACF580] DirectShow video devices
            [dshow @ 03ACF580]  "Integrated Camera"
            [dshow @ 03ACF580]  "USB2.0 Camera"
            [dshow @ 03ACF580] DirectShow audio devices
            [dshow @ 03ACF580]  "Microphone (Realtek High Definition Audio)"
            [dshow @ 03ACF580]  "Microphone (USB2.0 Camera)"
            dummy: Immediate exit requested
            ```


        - [x] **Specify Video Device's name:** Then, you can specify and initialize your located Video device's name in FFdecoder API as follows:

            ```python
            # initialize and formulate the decoder with "USB2.0 Camera" source for BGR24 output
            decoder = FFdecoder("USB2.0 Camera", source_demuxer="dshow", frame_format="bgr24", verbose=True).formulate()
            ```

        - [x] **[OPTIONAL] Specify Video Device's index along with name:** If there are multiple Video devices with similar name, then you can use `-video_device_number` parameter to specify the arbitrary index of the particular device. For instance, to open second video device with name `"Camera"` you can do as follows:

            ```python
            # define video_device_number as 1 (numbering start from 0)
            ffparams = {"-ffprefixes":["-video_device_number", "1"]}

            # initialize and formulate the decoder with "Camera" source for BGR24 output
            decoder = FFdecoder("Camera", source_demuxer="dshow", frame_format="bgr24", verbose=True, **ffparams).formulate()
            ```

    === ":material-linux: Linux"

        Linux OS users can use the [`video4linux2`](https://trac.ffmpeg.org/wiki/Capture/Webcam#Linux) _(or its alias `v4l2`)_ to list to all capture video devices such as from an USB webcam. You can refer following steps to identify and specify your capture video device's path:

        - [x] **Identify Video Devices:** Linux systems tend to automatically create file device node/path when the device _(e.g. an USB webcam)_ is plugged into the system, and has a name of the kind `'/dev/videoN'`, where `N` is a index associated to the device. To get the list of all available file device node/path on your Linux machine, you can use the `v4l-ctl` command.

            !!! tip "You can use `#!sh sudo apt install v4l-utils` APT command to install `v4l-ctl` tool on Debian-based Linux distros."

            ```sh
            $ v4l2-ctl --list-devices

            USB2.0 PC CAMERA (usb-0000:00:1d.7-1):
                    /dev/video1

            UVC Camera (046d:0819) (usb-0000:00:1d.7-2):
                    /dev/video0
            ```

        - [x] **Specify Video Device's path:** Then, you can specify and initialize your located Video device's path in FFdecoder API as follows:

            ```python
            # initialize and formulate the decoder with "/dev/video0" source for BGR24 output
            decoder = FFdecoder("/dev/video0", source_demuxer="v4l2", frame_format="bgr24", verbose=True).formulate()
            ```

        - [x] **[OPTIONAL] Specify Video Device's additional specifications:** You can also specify additional specifications _(such as pixel format(s), video format(s), framerate, and frame dimensions)_ supported by your Video Device as follows:

            !!! tip "You can use `#!sh ffmpeg -f v4l2 -list_formats all -i /dev/video0` terminal command to list available specifications."

            ```python
            # define video device specifications
            ffparams = {"-ffprefixes":["-framerate", "25", "-video_size", "640x480"]}

            # initialize and formulate the decoder with "/dev/video0" source for BGR24 output
            decoder = FFdecoder("/dev/video0", source_demuxer="v4l2", frame_format="bgr24", verbose=True, **ffparams).formulate()
            ```

    === ":material-apple: MacOS"

        MacOS users can use the [AVFoundation](https://ffmpeg.org/ffmpeg-devices.html#avfoundation) to list input devices and is the currently recommended framework by Apple for streamgrabbing on Mac OSX-10.7 (Lion) and later as well as on iOS. You can refer following steps to identify and specify your capture video device's name or index on MacOS/OSX machines:

        !!! note "QTKit is also available for streamgrabbing on Mac OS X 10.4 (Tiger) and later, but has been marked deprecated since OS X 10.7 (Lion) and may not be available on future releases."


        - [x] **Identify Video Devices:** Then, You can locate your Video device's name and index using `avfoundation` as follows:

            ```sh
            $ ffmpeg -f avfoundation -list_devices true -i ""

            ffmpeg version N-45279-g6b86dd5... --enable-runtime-cpudetect
              libavutil      51. 74.100 / 51. 74.100
              libavcodec     54. 65.100 / 54. 65.100
              libavformat    54. 31.100 / 54. 31.100
              libavdevice    54.  3.100 / 54.  3.100
              libavfilter     3. 19.102 /  3. 19.102
              libswscale      2.  1.101 /  2.  1.101
              libswresample   0. 16.100 /  0. 16.100
            [AVFoundation input device @ 0x7f8e2540ef20] AVFoundation video devices:
            [AVFoundation input device @ 0x7f8e2540ef20] [0] FaceTime HD camera (built-in)
            [AVFoundation input device @ 0x7f8e2540ef20] [1] Capture screen 0
            [AVFoundation input device @ 0x7f8e2540ef20] AVFoundation audio devices:
            [AVFoundation input device @ 0x7f8e2540ef20] [0] Blackmagic Audio
            [AVFoundation input device @ 0x7f8e2540ef20] [1] Built-in Microphone
            ```


        - [x] **Specify Video Device's name or index:** Then, you can specify and initialize your located Video device in FFdecoder API using its either the name or the index shown in the device listing:

            === "Using device's index"

                ```python
                # initialize and formulate the decoder with `1` index source for BGR24 output
                decoder = FFdecoder("1", source_demuxer="avfoundation", frame_format="bgr24", verbose=True).formulate()
                ```

            === "Using device's name"

                When specifying device's name, abbreviations using just the beginning of the device name are possible. Thus, to capture from a device named "Integrated iSight-camera" just "Integrated" is sufficient:

                ```python
                # initialize and formulate the decoder with "Integrated iSight-camera" source for BGR24 output
                decoder = FFdecoder("Integrated", source_demuxer="avfoundation", frame_format="bgr24", verbose=True).formulate()
                ```

        - [x] **[OPTIONAL] Specify Default Video device:** You can also use the default device which is usually the first device in the listing by using "default" as source:

            ```python
            # initialize and formulate the decoder with "default" source for BGR24 output
            decoder = FFdecoder("default", source_demuxer="avfoundation", frame_format="bgr24", verbose=True).formulate()
            ```

    !!! fail "If these steps doesn't work for you then reach us out on [Gitter ➶][gitter] Community channel"



```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# initialize and formulate the decoder with "/dev/video0" source for BGR24 output
decoder = FFdecoder("/dev/video0", source_demuxer="v4l2", frame_format="bgr24", verbose=True).formulate()

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

## Capturing and Previewing frames from your Desktop 

???+ alert "Example Assumptions"

    Similar to Webcam capturing, FFmpeg provide set of specific Demuxers on different platforms for capturing your desktop _(Screen recording)_. Please note that following recipe explicitly assumes: 

    - You're running Linux Machine with `libxcb` module installed properly on your machine.
    - You machine uses FFmpeg binaries built with `--enable-libxcb` flag to support `x11grab` demuxer. BTW, you can list all supported demuxers using the `#!sh ffmpeg --list-demuxers` terminal command.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.

In this example we will decode live **BGR** video frames from your complete screen as well as a region in FFdecoder API, and preview them using OpenCV Library's `cv2.imshow()` method.

??? tip "Specifying suitable Parameter(s) and Demuxer for Capturing your Desktop on different OS platforms"

    === ":fontawesome-brands-windows: Windows"

        Windows OS users can use the [gdigrab](https://ffmpeg.org/ffmpeg-devices.html#gdigrab) to grab video from the Windows screen. You can refer following steps to specify source for capturing different regions of your display:

        !!! fail "For Windows OS users [`dshow`](https://github.com/rdp/screen-capture-recorder-to-video-windows-free) is also available for grabbing frames from your desktop. But it is highly unreliable and don't works most of the times."

        - [x] **Capturing entire desktop:** For capturing all your displays as one big contiguous display, you can specify source, suitable parameters and demuxers in FFdecoder API as follows:

            ```python
            # define framerate
            ffparams = {"-framerate": "30"}

            # initialize and formulate the decoder with "desktop" source for BGR24 output
            decoder = FFdecoder("desktop", source_demuxer="gdigrab", frame_format="bgr24", verbose=True, **ffparams).formulate()
            ```

        - [x] **Capturing a region:** If you want to limit capturing to a region, and show the area being grabbed, you can specify source and suitable parameters in FFdecoder API as follows:

            !!! info "`x_offset` and `y_offset` specify the offsets of the grabbed area with respect to the top-left border of the desktop screen. They default to `0`. "

            ```python
            # define suitable parameters
            ffparams = {
                "-framerate": "30", # input framerate
                "-ffprefixes": [
                    "-offset_x", "10", "-offset_y", "20", # grab at position 10,20
                    "-video_size", "640x480", # frame size
                    "-show_region", "1", # show only region
                ],
            }

            # initialize and formulate the decoder with "desktop" source for BGR24 output
            decoder = FFdecoder("desktop", source_demuxer="gdigrab", frame_format="bgr24", verbose=True, **ffparams).formulate()
            ```

    === ":material-linux: Linux"

        Linux OS users can use the [x11grab](https://ffmpeg.org/ffmpeg-devices.html#x11grab) to capture an X11 display. You can refer following steps to specify source for capturing different regions of your display:

        !!! note "For X11 display, the source input has the syntax: `"display_number.screen_number[+x_offset,y_offset]"`."

        - [x] **Capturing entire desktop:** For capturing all your displays as one big contiguous display, you can specify source, suitable parameters and demuxers in FFdecoder API as follows:

            ```python
            # define framerate
            ffparams = {"-framerate": "30"}

            # initialize and formulate the decoder with ":0.0" desktop source for BGR24 output
            decoder = FFdecoder(":0.0", source_demuxer="x11grab", frame_format="bgr24", verbose=True, **ffparams).formulate()
            ```

        - [x] **Capturing a region:** If you want to limit capturing to a region, and show the area being grabbed, you can specify source and suitable parameters in FFdecoder API as follows:

            !!! info "`x_offset` and `y_offset` specify the offsets of the grabbed area with respect to the top-left border of the X11 screen. They default to `0`. "

            ```python
            # define suitable parameters
            ffparams = {
                "-framerate": "30", # input framerate
                "-ffprefixes": [
                    "-video_size", "1024x768", # frame size
                ],
            }

            # initialize and formulate the decoder with ":0.0" desktop source(starting with the upper-left corner at x=10, y=20) 
            # for BGR24 output
            decoder = FFdecoder(":0.0+10,20", source_demuxer="x11grab", frame_format="bgr24", verbose=True, **ffparams).formulate()
            ```

    === ":material-apple: MacOS"

        MacOS users can use the [AVFoundation](https://ffmpeg.org/ffmpeg-devices.html#avfoundation) to list input devices and is the currently recommended framework by Apple for streamgrabbing on Mac OSX-10.7 (Lion) and later as well as on iOS. You can refer following steps to identify and specify your capture video device's name or index on MacOS/OSX machines:

        !!! note "QTKit is also available for streamgrabbing on Mac OS X 10.4 (Tiger) and later, but has been marked deprecated since OS X 10.7 (Lion) and may not be available on future releases."


        - [x] **Identify Video Devices:**  You can enumerate all the available input devices including screens ready to be captured using `avfoundation` as follows:

            ```sh
            $ ffmpeg -f avfoundation -list_devices true -i ""

            ffmpeg version N-45279-g6b86dd5... --enable-runtime-cpudetect
              libavutil      51. 74.100 / 51. 74.100
              libavcodec     54. 65.100 / 54. 65.100
              libavformat    54. 31.100 / 54. 31.100
              libavdevice    54.  3.100 / 54.  3.100
              libavfilter     3. 19.102 /  3. 19.102
              libswscale      2.  1.101 /  2.  1.101
              libswresample   0. 16.100 /  0. 16.100
            [AVFoundation input device @ 0x7f8e2540ef20] AVFoundation video devices:
            [AVFoundation input device @ 0x7f8e2540ef20] [0] FaceTime HD camera (built-in)
            [AVFoundation input device @ 0x7f8e2540ef20] [1] Capture screen 0
            [AVFoundation input device @ 0x7f8e2540ef20] AVFoundation audio devices:
            [AVFoundation input device @ 0x7f8e2540ef20] [0] Blackmagic Audio
            [AVFoundation input device @ 0x7f8e2540ef20] [1] Built-in Microphone
            ```


        - [x] **Capturing entire desktop:** Then, you can specify and initialize your located screens in FFdecoder API using its index shown:

            ```python
            # initialize and formulate the decoder with `0:` index desktop screen for BGR24 output
            decoder = FFdecoder("0:", source_demuxer="avfoundation", frame_format="bgr24", verbose=True).formulate()
            ```

        - [x] **[OPTIONAL] Capturing mouse:** You can also specify additional specifications to capture the mouse pointer and screen mouse clicks as follows:

            ```python
            # define specifications
            ffparams = {"-ffprefixes":["-capture_cursor", "1", "-capture_mouse_clicks", "0"]}

            # initialize and formulate the decoder with "0:" source for BGR24 output
            decoder = FFdecoder("0:", source_demuxer="avfoundation", frame_format="bgr24", verbose=True, **ffparams).formulate()
            ```

    !!! fail "If these steps doesn't work for you then reach us out on [Gitter ➶][gitter] Community channel"

=== "Capturing entire desktop" 

    For capturing all your displays as one big contiguous display in FFdecoder API:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # define framerate
    ffparams = {"-framerate": "30"}

    # initialize and formulate the decoder with ":0.0" desktop source for BGR24 output
    decoder = FFdecoder(":0.0", source_demuxer="x11grab", frame_format="bgr24", verbose=True, **ffparams).formulate()

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


=== "Capturing a region" 

    For limit capturing to a region, and show the area being grabbed:

    !!! info "`x_offset` and `y_offset` specify the offsets of the grabbed area with respect to the top-left border of the X11 screen. They default to `0`. "

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # define suitable parameters
    ffparams = {
        "-framerate": "30", # input framerate
        "-ffprefixes": [
            "-video_size", "1024x768", # frame size
        ],
    }

    # initialize and formulate the decoder with ":0.0" desktop source(starting with the upper-left corner at x=10, y=20) 
    # for BGR24 output
    decoder = FFdecoder(":0.0+10,20", source_demuxer="x11grab", frame_format="bgr24", verbose=True, **ffparams).formulate()

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