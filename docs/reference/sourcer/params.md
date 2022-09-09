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

# Sourcer API Parameters 

## **`source`**

This parameter defines the input source (`-i`) for probing.

!!! warning "Sourcer API will throw `AssertionError` if `source` provided is invalid or missing."

!!! danger "Sourcer API checks for _`video bitrate`_ or _`frame-size` and `framerate`_ in video's metadata to ensure given input `source` has usable video stream available. Thereby, it will throw `ValueError` if it fails to find those parameters."

!!! info "Multiple video inputs are not yet supported!"

**Data-Type:** String.

Its valid input can be one of the following: 

- [x] **Filepath:** _Valid path of the video file, for e.g `"/home/foo.mp4"` as follows:_

    ```python
    # initialize the sourcer and probe it
    sourcer = Sourcer('/home/foo.mp4').probe_stream()
    ```

- [x] **Image Sequence:** _Valid image sequence such as sequential(`'img%03d.png'`) or glob pattern(`'*.png'`) or single (looping) image as input:_

    
    === "Sequential"

        ??? question "How to start with specific number image?"
        
            You can use `-start_number` FFmpeg parameter if you want to start with specific number image:

            ```python
            # define `-start_number` such as `5`
            sourcer_params = {"-ffprefixes":["-start_number", "5"]}

            # initialize the sourcer with define parameters
            sourcer = Sourcer('img%03d.png', verbose=True, **sourcer_params).probe_stream()
            ```

        ```python
        # initialize the sourcer and probe it
        sourcer = Sourcer('img%03d.png', verbose=True).probe_stream()
        ```

    === "Glob pattern"

        !!! abstract "Bash-style globbing _(`*` represents any number of any characters)_ is useful if your images are sequential but not necessarily in a numerically sequential order."

        !!! warning "The glob pattern is not available on Windows builds."

        ```python
        # define `-pattern_type glob` for accepting glob pattern
        sourcer_params = {"-ffprefixes":["-pattern_type", "glob"]}

        # initialize the sourcer with define parameters and probe it
        sourcer = Sourcer('img*.png', verbose=True, **sourcer_params).probe_stream()
        ```

    === "Single (loop) image"

        ```python
        # define `-loop 1` for looping
        sourcer_params = {"-ffprefixes":["-loop", "1"]}

        # initialize the sourcer with define parameters and probe it
        sourcer = Sourcer('img.jpg', verbose=True, **sourcer_params).probe_stream()
        ```


- [x] **Network Address:** _Valid (`http(s)`, `rtp`, `rstp`, `rtmp`, `mms`, etc.) incoming network stream address such as `'rtsp://xx:yy@192.168.1.ee:fd/av0_0'` as input:_

    ```python
    # define `rtsp_transport` or necessary parameters 
    sourcer_params = {"-ffprefixes":["-rtsp_transport", "tcp"]}

    # initialize the sourcer with define parameters and probe it
    sourcer = Sourcer('rtsp://xx:yy@192.168.1.ee:fd/av0_0', verbose=True, **sourcer_params).probe_stream()
    ```

- [x] **Camera Device Index:** Valid "device index" or "camera index" of the connected Camera Device. For example, for using `"0"` index device as source on :fontawesome-brands-windows: Windows, we can do as follows in Sourcer API: 

    ??? danger "Requirement for using Camera Device as source in Sourcer API"

        - [x] **MUST have appropriate FFmpeg binaries, Drivers, and Softwares installed:**
            
            Internally, DeFFcode APIs achieves Index based Camera Device Capturing by employing some specific FFmpeg demuxers on different platforms(OSes). These platform specific demuxers are as follows:

            | Platform(OS) | Demuxer |
            |:------------:|:-------|
            | :fontawesome-brands-windows: Windows OS|[`dshow`](https://trac.ffmpeg.org/wiki/DirectShow) _(or DirectShow)_ |
            | :material-linux: Linux OS | [`video4linux2`](https://trac.ffmpeg.org/wiki/Capture/Webcam#Linux) _(or its alias `v4l2`)_ |
            | :material-apple: Mac OS | [`avfoundation`](https://ffmpeg.org/ffmpeg-devices.html#avfoundation) |

            **:warning: Important:** Kindly make sure your FFmpeg binaries support these platform specific demuxers as well as system have the appropriate video drivers and related softwares installed.

        - [x] The [`source`](#source) parameter value **MUST be any Camera Device index** that can be of either **integer** _(e.g. `-1`,`0`,`1`, etc.)_ or **string of integer** _(e.g. `"-1"`,`"0"`,`"1"`, etc.)_ type.

        - [x] The [`source_demuxer`](#source_demuxer) parameter value  **MUST be either `None`_(also means empty)_ or `"auto"`**. 

    ```python
    # initialize the sourcer with "0" index source and probe it
    sourcer = Sourcer("0", verbose=True).probe_stream()
    ```

- [x] **Video Capture Devices:** Valid video probe device's name _(e.g. `"USB2.0 Camera"`)_ or its path _(e.g. `"/dev/video0"` on linux)_ or its index _(e.g. `"0"`)_ as input  w.r.t [`source_demuxer`](#source_demuxer) parameter value in use. For example, for probing `"USB2.0 Camera"` named device with `dshow` source demuxer on :fontawesome-brands-windows: Windows, we can do as follows in Sourcer API: 

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

            - [x] **Specify Video Device's name:** Then, you can specify and initialize your located Video device's name in Sourcer API as follows:

                ```python
                # initialize the sourcer with "USB2.0 Camera" source and probe it
                sourcer = Sourcer("USB2.0 Camera", source_demuxer="dshow", verbose=True).probe_stream()
                ```

            - [x] **[OPTIONAL] Specify Video Device's index along with name:** If there are multiple Video devices with similar name, then you can use `-video_device_number` parameter to specify the arbitrary index of the particular device. For instance, to open second video device with name `"Camera"` you can do as follows:

                ```python
                # define video_device_number as 1 (numbering start from 0)
                sourcer_params = {"-ffprefixes":["-video_device_number", "1"]}

                # initialize the sourcer with "Camera" source and probe it
                sourcer = Sourcer("Camera", source_demuxer="dshow", verbose=True, **sourcer_params).probe_stream()
                ```

        === ":material-linux: Linux"

            Linux OS users can use the [`video4linux2`](https://trac.ffmpeg.org/wiki/Capture/Webcam#Linux) _(or its alias `v4l2`)_ to list to all video capture devices such as from an USB webcam. You can refer following steps to identify and specify your probe video device's path:

            - [x] **Identify Video Devices:** Linux systems tend to automatically create file device node/path when the device _(e.g. an USB webcam)_ is plugged into the system, and has a name of the kind `'/dev/videoN'`, where `N` is a index associated to the device. To get the list of all available file device node/path on your Linux machine, you can use the `v4l-ctl` command.

                !!! tip "You can use `#!sh sudo apt install v4l-utils` APT command to install `v4l-ctl` tool on Debian-based Linux distros."

                ```sh
                $ v4l2-ctl --list-devices

                USB2.0 PC CAMERA (usb-0000:00:1d.7-1):
                        /dev/video1

                UVC Camera (046d:0819) (usb-0000:00:1d.7-2):
                        /dev/video0
                ```

            - [x] **Specify Video Device's path:** Then, you can specify and initialize your located Video device's path in Sourcer API as follows:

                ```python
                # initialize the sourcer with "/dev/video0" source and probe it
                sourcer = Sourcer("/dev/video0", source_demuxer="v4l2", verbose=True).probe_stream()
                ```

        === ":material-apple: MacOS"

            MacOS users can use the [AVFoundation](https://ffmpeg.org/ffmpeg-devices.html#avfoundation) to list input devices and is the currently recommended framework by Apple for streamgrabbing on Mac OSX-10.7 (Lion) and later as well as on iOS. You can refer following steps to identify and specify your probe video device's name or index on MacOS/OSX machines:

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


            - [x] **Specify Video Device's name or index:** Then, you can specify and initialize your located Video device in Sourcer API using its either the name or the index shown in the device listing:

                === "Using device's index"

                    ```python
                    # initialize the sourcer with `1` index source and probe it
                    sourcer = Sourcer("1", source_demuxer="avfoundation", verbose=True).probe_stream()
                    ```

                === "Using device's name"

                    When specifying device's name, abbreviations using just the beginning of the device name are possible. Thus, to probe from a device named "Integrated iSight-camera" just "Integrated" is sufficient:

                    ```python
                    # initialize the sourcer with "Integrated iSight-camera" source 
                    sourcer = Sourcer("Integrated", source_demuxer="avfoundation", verbose=True).probe_stream()
                    ```

        !!! fail "If these steps doesn't work for you then reach us out on [Gitter ➶][gitter] Community channel"


    ```python
    # initialize the sourcer with "USB2.0 Camera" source 
    sourcer = Sourcer("USB2.0 Camera", source_demuxer="dshow", verbose=True).probe_stream()
    ```


- [x] **Screen Capturing/Recording:** Valid screen probe device's name _(e.g. `"desktop"`)_ or its index _(e.g. `":0.0"`)_ as input w.r.t [`source_demuxer`](#source_demuxer) parameter value in use. For example, for probing `"0:"` indexed device with `avfoundation` source demuxer on :material-apple: MacOS, we can do as follows in Sourcer API: 

    ??? tip "Specifying suitable Parameter(s) and Demuxer for Capturing your Desktop on different OSes"

        === ":fontawesome-brands-windows: Windows"

            Windows OS users can use the [gdigrab](https://ffmpeg.org/ffmpeg-devices.html#gdigrab) to grab video from the Windows screen. You can refer following steps to specify source for probing:

            !!! fail "For Windows OS users [`dshow`](https://github.com/rdp/screen-probe-recorder-to-video-windows-free) is also available for grabbing frames from your desktop. But it is highly unreliable and don't works most of the times."

            ```python
            # define framerate
            sourcer_params = {"-framerate": "30"}

            # initialize the sourcer with "desktop" source and probe it
            sourcer = Sourcer("desktop", source_demuxer="gdigrab", verbose=True, **sourcer_params).probe_stream()
            ```

        === ":material-linux: Linux"

            Linux OS users can use the [x11grab](https://ffmpeg.org/ffmpeg-devices.html#x11grab) to probe an X11 display. You can refer following steps to specify source for probing:

            ```python
            # initialize the sourcer with ":0.0" desktop source and probe it
            sourcer = Sourcer(":0.0", source_demuxer="x11grab", verbose=True).probe_stream()
            ```

        === ":material-apple: MacOS"

            MacOS users can use the [AVFoundation](https://ffmpeg.org/ffmpeg-devices.html#avfoundation) to list input devices and is the currently recommended framework by Apple for streamgrabbing on Mac OSX-10.7 (Lion) and later as well as on iOS. You can refer following steps to identify and specify your probe video device's name or index in Sourcer API:

            !!! note "QTKit is also available for streamgrabbing on Mac OS X 10.4 (Tiger) and later, but has been marked deprecated since OS X 10.7 (Lion) and may not be available on future releases."


            You can enumerate all the available input devices including screens ready to be probed using `avfoundation` as follows:

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

            Then, you can specify and initialize your located screens in Sourcer API using its index shown:

            ```python
            # initialize the sourcer with `0:` index desktop screen and probe it
            sourcer = Sourcer("0:", source_demuxer="avfoundation", verbose=True).probe_stream()
            ```

        !!! fail "If these steps doesn't work for you then reach us out on [Gitter ➶][gitter] Community channel"

    ```python
    # initialize the sourcer with "0:" source and probe it
    sourcer = Sourcer("0:", source_demuxer="avfoundation", verbose=True).probe_stream()
    ```


- [x] **Virtual Sources:** Valid filtergraph to use as input with [`lavfi`](http://underpop.online.fr/f/ffmpeg/help/lavfi.htm.gz) _(**Libavfilter** input virtual device)_ source that reads data from the open output pads of a libavfilter filtergraph. For example, for generating and probing [Mandelbrot](https://en.wikipedia.org/wiki/Mandelbrot_set) graph of `1280x720` frame size and `30` framerate using `lavfi` input virtual device, we can do as follows in Sourcer API: 

    ```python
    # initialize the sourcer with "mandelbrot" source of
    # `1280x720` frame size and `30` framerate and probe it
    sourcer = Sourcer(
        "mandelbrot=size=1280x720:rate=30",
        source_demuxer="lavfi",
        frame_format="bgr24",
    ).probe_stream()
    ```

    


&nbsp;


## **`source_demuxer`** 

This parameter specifies the demuxer(`-f`) for the input source _(such as `dshow`, `v4l2`, `gdigrab` etc.)_ to support Live Feed Devices, as well as `lavfi` _(Libavfilter input virtual device)_ that reads data from the open output pads of a libavfilter filtergraph. 

!!! warning "Any invalid or unsupported value to `source_demuxer` parameter value will raise `Assertion` error!"

!!! tip "Use `#!sh ffmpeg -demuxers` terminal command to lists all FFmpeg supported demuxers."

??? info "Specifying `source_demuxer` for using Camera Device Index as source in Sourcer API"
    
    For using Camera Device Index as source in Sourcer API, the `source_demuxer` parameter value  **MUST be either `None`_(also means empty)_ or `"auto"`:**
    
    === "`source_demuxer=None` _(Default and Recommended)_"
        ```python
        # initialize the sourcer with "0" index source and probe it
        sourcer = Sourcer("0").probe_stream()
        ```
    === "`source_demuxer="auto"`"
        ```python
        # initialize the sourcer with "0" index source and probe it
        sourcer = Sourcer("0", source_demuxer="auto).probe_stream()
        ```

**Data-Type:** String

**Default Value:** Its default value is `None`.

**Usage:**

```python
# initialize the sourcer with `dshow` demuxer and probe it
sourcer = Sourcer("foo.mp4", source_demuxer="dshow").probe_stream()
```


&nbsp; 

## **`custom_ffmpeg`**

This parameter can be used to manually assigns the system _file-path/directory_ where the custom or downloaded FFmpeg executable is located.

??? info "Behavior on Windows :fontawesome-brands-windows:"
    
    If custom FFmpeg executable binary _file-path/directory_ is not assigned through `custom_ffmpeg` parameter on Windows machine, then Sourcer API will ==automatically attempt to download and extract suitable Static FFmpeg binaries at suitable location on your windows machine==. More information can be found [here ➶](../ffmpeg_install/#a-auto-installation).

    ??? question "How to change FFmpeg Static Binaries download directory?"

        You can use [`-ffmpeg_download_path`](#exclusive-parameters) exclusive parameter in Sourcer API to set the custom directory for downloading FFmpeg Static Binaries during the [Auto-Installation](../../../installation/ffmpeg_install/#a-auto-installation) step on Windows Machines. If this parameter is not altered, then these binaries will auto-save to the default temporary directory (for e.g. `C:/User/temp`) on your windows machine. It can be used as follows in Sourcer API:

        ```python
        # # define suitable parameter to download at "C:/User/foo/foo1"
        sourcer_params = {"-ffmpeg_download_path": "C:/User/foo/foo1"}

        # initialize the sourcer
        Sourcer("foo.mp4", verbose=True, **sourcer_params).probe_stream()
        ```

!!! warning "If binaries were not found at the manually specified path, DeFFcode APIs will throw **RuntimeError**!"

**Data-Type:** String

**Default Value:** Its default value is `None`.

**Usage:**

```python
# If ffmpeg executables are located at "/foo/foo1/ffmpeg"
Sourcer("foo.mp4", custom_ffmpeg="/foo/foo1/ffmpeg").probe_stream()
```

&nbsp;


## **`verbose`**

This parameter enables verbose logs _(if `True`)_, essential for debugging. 

**Data-Type:** Boolean

**Default Value:** Its default value is `False`.

**Usage:**

```python
# initialize the sourcer with verbose logs
Sourcer("foo.mp4", verbose=True).probe_stream()
```

&nbsp; 


## **`sourcer_params`**

This dictionary parameter accepts all [Exclusive Parameters](#exclusive-parameters) formatted as its attributes:

???+ note "Additional FFmpeg parameters"
    
    In addition to Exclusive Parameters, Sourcer API supports almost any FFmpeg parameter _(supported by installed FFmpeg)_, and thereby can be passed as dictionary attributes in `sourcer_params` parameter.

    !!! danger "Kindly read [**FFmpeg Docs**](https://ffmpeg.org/documentation.html) carefully before passing any additional values to `sourcer_params` parameter. Wrong invalid values may result in undesired errors or no output at all."

    !!! alert "All FFmpeg parameters are case-sensitive. Remember to double check every parameter if any error(s) occurred."

**Data-Type:** Dictionary

**Default Value:** Its default value is `{}`.

### Exclusive Parameters

> Sourcer API supports few Exclusive Parameters to allow users to flexibly change its probing properties and handle some special FFmpeg parameters.

These parameters are discussed below:

* **`-ffprefixes`** _(list)_: This attribute sets the special FFmpeg parameters that generally occurs at the very beginning _(such as `-re`)_ before input (`-i`) source. The FFmpeg parameters defined with this attribute can repeated more than once and maintains its original order in the FFmpeg command. Its value can be of datatype **`list`** only and its usage is as follows: 

    !!! tip "Turn on [`verbose`](#verbose) parameter _(`verbose = True`)_ to see the FFmpeg command that is being executed in Sourcer's pipeline. This helps you debug/address any issues and make adjustments accordingly."
        
    ```python
    # define suitable parameter
    sourcer_params = {"-ffprefixes": ['-re']} # executes as `ffmpeg -re <rest of command>`
    ```

&ensp;

* **`-ffmpeg_download_path`** _(string)_: sets the custom directory for downloading FFmpeg Static Binaries in Compression Mode, during the [Auto-Installation](../ffmpeg_install/#a-auto-installation) on Windows Machines Only. If this parameter is not altered, then these binaries will auto-save to the default temporary directory (for e.g. `C:/User/temp`) on your windows machine. It can be used as follows: 

    ```python
    sourcer_params = {"-ffmpeg_download_path": "C:/User/foo/foo1"} # will be saved to "C:/User/foo/foo1"
    ```

&ensp;

* **`-force_validate_source`** _(bool)_: forcefully passes validation test for given `source` which is required for some special cases with unusual input. It can be used as follows: 

    ```python
    sourcer_params = {"-force_validate_source": True} # will pass validation test forcefully
    ```
&ensp;

<!--
External URLs
-->
[gitter]: https://gitter.im/deffcode-python/community