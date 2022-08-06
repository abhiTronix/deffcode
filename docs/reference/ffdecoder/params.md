<!--
===============================================
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
===============================================
-->

# FFdecoder API Parameters 


## **`source`**

This parameter defines the input source (`-i`) for decoding real-time frames.

!!! warning "FFdecoder API will throw `Assertion` if `source` provided is invalid or missing."

!!! danger "FFdecoder API checks for _`video bitrate`_ or _`frame-size` and `framerate`_ in video's metadata to ensure given input `source` has usable video stream available. Thereby, it will throw `ValueError` if it fails to find those parameters."

!!! info "Multiple video inputs are not yet supported!"

**Data-Type:** String.

Its valid input can be one of the following: 

- [x] **Filepath:** _Valid path of the video file, for e.g `"/home/foo.mp4"` as follows:_

    ```python
    # initialize and formulate the decoder with `foo.mp4` source
    decoder = FFdecoder('/home/foo.mp4').formulate()
    ```

    !!! example "Related usage recipes :material-pot-steam: can found [here ➶](../../../recipes/basic/decode-video-files/#decoding-video-files)"

- [x] **Image Sequence:** _Valid image sequence such as sequential(`'img%03d.png'`) or glob pattern(`'*.png'`) or single (looping) image as input:_

    
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
        # initialize and formulate the decoder
        decoder = FFdecoder('img%03d.png').formulate()
        ```

    === "Glob pattern"

        !!! abstract "Bash-style globbing _(`*` represents any number of any characters)_ is useful if your images are sequential but not necessarily in a numerically sequential order."

        !!! warning "The glob pattern is not available on Windows builds."

        ```python
        # define `-pattern_type glob` for accepting glob pattern
        sourcer_params = {"-ffprefixes":["-pattern_type", "glob"]}

        # initialize and formulate the decoder with define parameters
        decoder = FFdecoder('img*.png', verbose=True, **sourcer_params).formulate()
        ```

    === "Single (loop) image"

        ```python
        # define `-loop 1` for looping
        ffparams = {"-ffprefixes":["-loop", "1"]}

        # initialize and formulate the decoder with define parameters
        decoder = FFdecoder('img.jpg', verbose=True, **ffparams).formulate()
        ```

    !!! example "Related usage recipes :material-pot-steam: can found [here ➶](../../../recipes/basic/decode-image-sequences/#decoding-image-sequences)"

- [x] **Network Address:** _Valid (`http(s)`, `rtp`, `rstp`, `rtmp`, `mms`, etc.) incoming network stream address such as `'rtsp://xx:yy@192.168.1.ee:fd/av0_0'` as input:_

    ```python
    # define `rtsp_transport` or necessary parameters 
    ffparams = {"-ffprefixes":["-rtsp_transport", "tcp"]}

    # initialize and formulate the decoder with define parameters
    decoder = FFdecoder('rtsp://xx:yy@192.168.1.ee:fd/av0_0', verbose=True, **ffparams).formulate()
    ```

    !!! example "Related usage recipes :material-pot-steam: can found [here ➶](../../../recipes/basic/decode-network-streams/#decoding-network-streams)"

- [x] **Video Capture Devices (Webcams):** Valid video capture device's name _(e.g. `"USB2.0 Camera"`)_ or its path _(e.g. `"/dev/video0"` on linux)_ or its index _(e.g. `"0"`)_ as input  w.r.t [`source_demuxer`](#source_demuxer) parameter value in use. For example, for capturing `"USB2.0 Camera"` named device with `dshow` source demuxer on :fontawesome-brands-windows: Windows, we can do as follows in FFdecoder API: 

    ??? tip "Identifying and Specifying Device name/path/index and suitable Demuxer on different OSes"

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
    # initialize and formulate the decoder with "USB2.0 Camera" source for BGR24 output
    decoder = FFdecoder("USB2.0 Camera", source_demuxer="dshow", frame_format="bgr24", verbose=True).formulate()
    ```

    !!! example "Related usage recipe :material-pot-mix: can found [here ➶](../../../recipes/basic/decode-live-feed-devices/#capturing-and-previewing-frames-from-a-webcam)"

- [x] **Screen Capturing/Recording:** Valid screen capture device's name _(e.g. `"desktop"`)_ or its index _(e.g. `":0.0"`)_ as input w.r.t [`source_demuxer`](#source_demuxer) parameter value in use. You can also specify additional specifications _(such as limiting capture area to a region, setting capturing coordinates, whether to capture mouse pointer and clicks etc.)_. For example, for capturing `"0:"` indexed device with `avfoundation` source demuxer on :material-apple: MacOS along with mouse pointer and clicks, we can do as follows in FFdecoder API: 

    ??? tip "Specifying suitable Parameter(s) and Demuxer for Capturing your Desktop on different OSes"

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

    ```python
    # define specifications
    ffparams = {"-ffprefixes":["-capture_cursor", "1", "-capture_mouse_clicks", "0"]}

    # initialize and formulate the decoder with "0:" source for BGR24 output
    decoder = FFdecoder("0:", source_demuxer="avfoundation", frame_format="bgr24", verbose=True, **ffparams).formulate()
    ```

    !!! example "Related usage recipe :material-pot-mix: can found [here ➶](../../../recipes/basic/decode-live-feed-devices/#capturing-and-previewing-frames-from-your-desktop)"


- [x] **Virtual Sources:** Valid filtergraph to use as input with [`lavfi`](http://underpop.online.fr/f/ffmpeg/help/lavfi.htm.gz) _(**Libavfilter** input virtual device)_ source that reads data from the open output pads of a libavfilter filtergraph. For example, for generating and decoding [Mandelbrot](https://en.wikipedia.org/wiki/Mandelbrot_set) graph of `1280x720` frame size and `30` framerate using `lavfi` input virtual device, we can do as follows in FFdecoder API: 

    ```python
    # initialize and formulate the decoder with "mandelbrot" source of
    # `1280x720` frame size and `30` framerate for BGR24 output
    decoder = FFdecoder(
        "mandelbrot=size=1280x720:rate=30",
        source_demuxer="lavfi",
        frame_format="bgr24",
    ).formulate()
    ```

    !!! example "Related usage recipes :material-pot-steam: can found [here ➶](../../../recipes/advanced/decode-live-virtual-sources/#decoding-live-virtual-sources)"


&nbsp;


## **`source_demuxer`** 

This parameter specifies the demuxer(`-f`) for the input source _(such as `dshow`, `v4l2`, `gdigrab` etc.)_ to support Live Feed Devices, as well as `lavfi` _(Libavfilter input virtual device)_ that reads data from the open output pads of a libavfilter filtergraph. 

!!! warning "Any invalid or unsupported value to `source_demuxer` parameter value will raise `Assertion` error!"

!!! tip "Use `#!sh ffmpeg -demuxers` terminal command to lists all FFmpeg supported demuxers."

**Data-Type:** String

**Default Value:** Its default value is `None`.

**Usage:**

```python
# initialize and formulate the decoder with `dshow` demuxer
decoder = FFdecoder("foo.mp4", source_demuxer="dshow").formulate()
```


&nbsp; 


## **`frame_format`** 

This parameter select the pixel format for output video frames _(such as `gray` for grayscale output)_. If not specified, its value defaults to `rgb24` _(24-bit RGB)_.

!!! warning "Any invalid or unsupported value to `frame_format` parameter will discarded!"

!!! tip "Use `#!sh ffmpeg -pix_fmts` terminal command to lists all FFmpeg supported pixel formats."

**Data-Type:** String

**Default Value:** Its default value is `rgb24`

**Usage:**

```python
# initialize and formulate the decoder for grayscale frames
decoder = FFdecoder("foo.mp4", frame_format="gray").formulate()
```

!!! example "Various Pixel formats related usage recipes :material-pot-steam: can found [here ➶](../../../recipes/basic/decode-video-files/#capturing-and-previewing-bgr-frames-from-a-video-file)"

&nbsp; 

## **`custom_ffmpeg`**

This parameter can be used to manually assigns the system _file-path/directory_ where the custom or downloaded FFmpeg executable is located.

??? info "Behavior on Windows :fontawesome-brands-windows:"
    
    If custom FFmpeg executable binary _file-path/directory_ is not assigned through `custom_ffmpeg` parameter on Windows machine, then FFdecoder API will ==automatically attempt to download and extract suitable Static FFmpeg binaries at suitable location on your windows machine==. More information can be found [here ➶](../ffmpeg_install/#a-auto-installation).

    ??? question "How to change FFmpeg Static Binaries download directory?"

        You can use `-ffmpeg_download_path` _(via. [`-custom_sourcer_params`](#exclusive-parameters))_ exclusive parameter in FFdecoder API to set the custom directory for downloading FFmpeg Static Binaries during the [Auto-Installation](../../../installation/ffmpeg_install/#a-auto-installation) step on Windows Machines. If this parameter is not altered, then these binaries will auto-save to the default temporary directory (for e.g. `C:/User/temp`) on your windows machine. It can be used as follows in FFdecoder API:

        ```python
        # # define suitable parameter to download at "C:/User/foo/foo1"
        ffparams = {"-custom_sourcer_params": {"-ffmpeg_download_path": "C:/User/foo/foo1"}}

        # initialize and formulate the decoder
        FFdecoder("foo.mp4", verbose=True, **ffparams).formulate()
        ```

!!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"

**Data-Type:** String

**Default Value:** Its default value is `None`.

**Usage:**

```python
# If ffmpeg executables are located at "/foo/foo1/ffmpeg"
FFdecoder("foo.mp4", custom_ffmpeg="/foo/foo1/ffmpeg").formulate()
```

&nbsp;


## **`verbose`**

This parameter enables verbose _(if `True`)_, essential for debugging. 

**Data-Type:** Boolean

**Default Value:** Its default value is `False`.

**Usage:**

```python
FFdecoder("foo.mp4", verbose=True).formulate()
```

&nbsp; 


## **`ffparams`**

This dictionary parameter accepts all [supported parameters](#supported-parameters) formatted as its attributes:

**Data-Type:** Dictionary

**Default Value:** Its default value is `{}`.

### Supported Parameters

#### A. FFmpeg Parameters 

> Almost any FFmpeg parameter _(supported by installed FFmpeg)_  can be passed as dictionary attributes in `ffparams` parameter.

Let's assume we want to `00:00:01.45`_(or 1045msec)_ in time and decode one single frame from given source _(say `foo.mp4`)_ in FFdecoder API, then we can assign required FFmpeg parameters as dictionary attributes as follows:

!!! danger "Kindly read [**FFmpeg Docs**](https://ffmpeg.org/documentation.html) carefully before passing any additional values to `ffparams` parameter. Wrong invalid values may result in undesired errors or no output at all."

!!! alert "All FFmpeg parameters are case-sensitive. Remember to double check every parameter if any error(s) occurred."

```python
# define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec)
# in time and get one single frame
ffparams = {"-ss": "00:00:01.45", "-frames:v": 1}

# initialize and formulate decoder with suitable source and FFmpeg params
decoder = FFdecoder("foo.mp4", verbose=True, **ffparams).formulate()
```

&thinsp;

#### B. Exclusive Parameters

> In addition to FFmpeg parameters, FFdecoder API also supports few Exclusive Parameters, to allow users to flexibly change its internal pipeline, properties, and handle some special FFmpeg parameters _(such as repeated `map`)_ that cannot be assigned via. python dictionary. 

These parameters are discussed below:


* **`-vcodec`** _(str)_ : This attribute works similar to `-vcodec` FFmpeg parameter for specifying supported decoders that are compiled with FFmpeg in use. If not specified, it's value is derived from source video metadata. Its usage is as follows: 

    !!! tip "Use `#!sh ffmpeg -decoders` terminal command to lists all FFmpeg supported decoders."

    !!! info "To remove `-vcodec` forcefully from FFmpeg Pipeline, assign its value Nonetype as `#!py3 {"-vcodec":None}` in ffparams"

    ```python
    # define suitable parameter
    ffparams = {"-vcodec": "h264"} # set decoder to `h264`
    ```

&ensp;


* **`-framerate`** _(float/int)_ : This attribute works similar to `-framerate` FFmpeg parameter for generating video-frames at specified framerate. If not specified, it calculated from source video metadata. Its usage is as follows: 

    ```python
    # define suitable parameter
    ffparams = {"-framerate": 60.0} # set input video source framerate to 60fps
    ```

&ensp;

* **`-custom_resolution`** _(tuple/list)_ : This attribute sets the custom resolution/size/dimensions of the output frames. Its value can either be a **tuple** => `(width,height)` or a **list** => `[width, height]`. If not specified, it calculated from source video metadata. Its usage is as follows: 
    
    ```python
    # define suitable parameter
    ffparams = {"-output_dimensions": (1280,720)} # to produce a 1280x720 resolution/scale output video
    ```

&ensp;

* **`-ffprefixes`** _(list)_: This attribute sets the special FFmpeg parameters that generally occurs at the very beginning _(such as `-re`)_ before input (`-i`) source. The FFmpeg parameters defined with this attribute can repeated more than once and maintains its original order in the FFmpeg command. Its value can be of datatype **`list`** only and its usage is as follows: 

    ??? info "Difference from  `-clones` parameter"

        The `-clones` and `-ffprefixes` parameters even tho fundamentally work the same, they're meant to serve at different positions in the FFmpeg command. Normally, FFdecoder API pipeline looks something like following with these parameters in place:

        ```sh
        ffmpeg {{-ffprefixes FFmpeg params}} -vcodec h264 -i foo.mp4 -pix_fmt rgb24 -s 1280x720 -framerate 25.0 {{-clones FFmpeg params}} -f rawvideo -
        ```

    !!! tip "Turn on [`verbose`](#verbose) parameter _(`verbose = True`)_ to see the FFmpeg command that is being executed in FFdecoder's pipeline. This helps you debug/address any issues and make adjustments accordingly."
        
    ```python
    # define suitable parameter
    ffparams = {"-ffprefixes": ['-re']} # executes as `ffmpeg -re <rest of command>`
    ```

&ensp;

* **`-clones`** _(list)_:  This attribute sets the special FFmpeg parameters after that are repeated more than once or occurs in a specific order _(that cannot be altered)_ in the FFmpeg command. Its value can be of datatype **`list`** only and its usage is as follows: 

    !!! tip "Turn on [`verbose`](#verbose) parameter _(`verbose = True`)_ to see the FFmpeg command that is being executed in FFdecoder's pipeline. This helps you debug/address any issues and make adjustments accordingly."

    ```python
    # define suitable parameter
    ffparams = {"-clones": ['-map', '0:v:0', '-map', '1:a?']} 
    
    # NOTE: Will be format as `ffmpeg -vcodec -i foo.mp4 -pix_fmt rgb24 -s 1280x720 -framerate 25.0 -map 0:v:0 -map 1:a -f rawvideo -`
    ```

&ensp;

* **`-custom_sourcer_params`** _(dict)_ :  This attribute assigns parameter meant for Sourcer API's [`sourcer_params`](../../sourcer/params/#sourcer_params) dictionary parameter, directly through FFdecoder API. Its usage is as follows: 
    
    ```python
    # define suitable parameter meant for `sourcer_params`
    ffparams = {"-custom_sourcer_params": {"-ffmpeg_download_path": "C:/User/foo/foo1"}}
    ```

&ensp;

* **`-passthrough_audio`** _(bool/list)_ : _(Yet to be supported)_

&nbsp; 

<!--
External URLs
-->
[gitter]: https://gitter.im/deffcode-python/community