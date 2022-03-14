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

!!! warning "FFdecoder API will throw `RuntimeError` if `source` provided is invalid or missing."


This parameter defines the default input source.


**Data-Type:** String.

Its valid input can be one of the following: 

- [x] **Filepath:** _Valid path of the video file, for e.g `"/home/foo.mp4"` as follows:_

    !!! alert "Multiple video file paths are not yet support!"

    ```python
    decoder = FFdecoder('/home/foo.mp4').formulate()
    ```

- [x] **Image Sequence:** _Valid image sequence such as sequential `'img%03d.png'` or `'*.png'` glob pattern or even single(loop) image as input:_

    
    === "Sequential"

        ```python
        # initialize and formulate the decoder
        decoder = FFdecoder('img%03d.png').formulate()
        ```

        You can use `-start_number` FFmpeg parameter if you want to start with specific number:

        ```python
        # define `-start_number` such as `5`
        extraparams = {"-ffpostfixes":["-start_number", "5"]}

        # initialize and formulate the decoder with define parameters
        decoder = FFdecoder('img%03d.png', verbose=True, **extraparams).formulate()
        ```

    === "Glob pattern"

        Bash-style globbing _(`*` represents any number of any characters)_ is useful if your images are sequential but not necessarily in a numerically sequential order. You can do it as follows:

        !!! warning "The glob pattern is not available on Windows builds."

        ```python
        # define `-pattern_type glob` for accepting glob pattern
        extraparams = {"-ffprefixes":["-pattern_type", "glob"]}

        # initialize and formulate the decoder with define parameters
        decoder = FFdecoder('img*.png', verbose=True, **extraparams).formulate()
        ```

    === "Single image"

        You can use a single looping image as follows:

        ```python
        # define `-loop 1` for looping
        extraparams = {"-ffprefixes":["-loop", "1"]}

        # initialize and formulate the decoder with define parameters
        decoder = FFdecoder('img.jpg', verbose=True, **extraparams).formulate()
        ```

- [x] **Network Address:** _Valid (`http(s)`, `rtp`, `rstp`, `rtmp`, `mms`, etc.) incoming network stream address such as `'rtsp://xx:yy@192.168.1.ee:fd/av0_0'` as input:_

    ```python
    # define `rtsp_transport` or necessary parameters 
    extraparams = {"-ffpostfixes":["-rtsp_transport", "tcp"]}

    # initialize and formulate the decoder with define parameters
    decoder = FFdecoder('rtsp://xx:yy@192.168.1.ee:fd/av0_0', verbose=True, **extraparams).formulate()
    ```

- [ ] **Video Input devices:** _(Yet to be supported)_

- [ ] **Screen Capture:** _(Yet to be supported)_





&nbsp;


## **`frame_format`** 


This parameter select pixel format of the output frames, such as `gray` for grayscale output. If not specified, its value is defaults to `rgb24` _(24-bit RGB)_.

!!! warning "Any invalid or unsupported value to `frame_format` parameter will discarded!"

!!! tip "Supported Decoders"

    All the pixel formats that are compiled with FFmpeg in use, are supported by FFdecoder API. You can easily check the compiled pixel formats by running following command in your terminal:

    ```sh
    # for checking pixel formats
    ffmpeg -pix_fmts           # use `ffmpeg.exe -pix_fmts` on windows
    ``` 

**Data-Type:** String

**Default Value:** Its default value is `rgb24`

**Usage:**

```python
# initialize and formulate the decoder for grayscale frames
decoder = FFdecoder("foo.mp4", frame_format="gray").formulate()
```



&nbsp; 


## **`custom_ffmpeg`**

This parameter assigns the custom _path/directory_ where the custom/downloaded FFmpeg executables are located.

!!! info "Behavior on Windows"
    
    If a custom FFmpeg executable's path | directory is not provided through `custom_ffmpeg` parameter on Windows machine, then FFdecoder API will ==automatically attempt to download and extract suitable Static FFmpeg binaries at suitable location on your windows machine==. More information can be found [here ➶](../ffmpeg_install/#a-auto-installation).

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


## **`extraparams`**

This parameter accepts to all [supported parameters](#supported-parameters) formatted as as its attributes:

!!! danger "Kindly read [**FFmpeg Docs**](https://ffmpeg.org/documentation.html) carefully before passing any additional values to `extraparams` parameter. Wrong invalid values may result in undesired errors or no output at all."


**Data-Type:** Dictionary

**Default Value:** Its default value is `{}`.


### Supported Parameters

#### A. FFmpeg Parameters 

Almost any FFmpeg parameter _(supported by installed FFmpeg)_  can be passed as dictionary attributes in `extraparams`. But make sure to read [**FFmpeg Docs**](https://ffmpeg.org/documentation.html) carefully first.

Let's assume we're using `h264_nvenc` NVDEC/CUVID decoder to produce faster frames with low memory footprints, then we can pass required FFmpeg parameters as dictionary attributes as follows:

!!! tip "Kindly check [NVDEC/CUVID doc ➶](https://trac.ffmpeg.org/wiki/HWAccelIntro) and other [FFmpeg Docs ➶](https://ffmpeg.org/documentation.html) for more information on these parameters"


!!! error "All ffmpeg parameters are case-sensitive. Remember to double check every parameter if any error occurs."

```python
extraparams = {"-vcodec":"h264_nvenc", "-ffpostfixes":["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]} 
```

&thinsp;

#### B. Exclusive Parameters

In addition to FFmpeg parameters, FFdecoder API also supports few Exclusive Parameters to flexibly alter its internal properties as well as handle some special FFmpeg parameters. These parameters are discussed below:


* **`-vcodec`** _(str)_ : works similiar to `-vcodec` FFmpeg parameter for specifying [supported decoders](#supported-decoders). If not specified, it derived from source video. Its usage is as follows: 

    !!! info "To remove `-vcodec` forcefully from FFmpeg Pipeline, assign its value Nonetype as `#!py3 {"-vcodec":None}` in extraparams"

    ```python
    extraparams = {"-vcodec": "h264"} # set decoder to `h264`
    ```

&ensp;


* **`-framerate`** _(float/int)_ : works similiar to `-framerate` FFmpeg parameter for generating video-frames at specified framerate. If not specified, it calculated from source video framerate. Its usage is as follows: 

    ```python
    extraparams = {"-framerate": 60.0} # set input video source framerate to 60fps
    ```

&ensp;

* **`-custom_resolution`** _(tuple/list)_ : sets the custom resolution/size/dimensions of the output frames. Its value can either be a **tuple** => `(width,height)` or a **list** => `[width, height]`. If not specified, it calculated from source video resolution. Its usage is as follows: 
    
    ```python
    extraparams = {"-output_dimensions": (1280,720)} # to produce a 1280x720 resolution/scale output video
    ```

&ensp;

* **`-ffprefixes`** _(list)_: sets the special FFmpeg parameters(at the beginning) that are repeated more than once or occurs in a specific order in the FFmpeg command. Its value can be of datatype **`list`** only and its usage is as follows: 

    ??? alert "This parameter is different from `-ffpostfixes` and `-clones`"
        All three `-clones`, `-ffpostfixes`, and `-ffprefixes` parameters even tho fundamentally work the same, they're meant to serve at different places in the FFmpeg command. Normally, FFdecoder API pipeline looks something like following with all three parameters in place:
        ```sh
        ffmpeg {{-ffprefixes FFmpeg params}} -vcodec h264 {{-ffpostfixes FFmpeg params}} -i foo.mp4 -pix_fmt rgb24 -s 1280x720 -framerate 25.0 {{-clones FFmpeg params}} -f rawvideo -
        ```

    !!! tip "Turn on verbose([`verbose = True`](#verbose)) to see the FFmpeg command that is being executed in FFdecoder's pipeline. This helps you debug/address any issues and make adjustments accordingly."
        
    ```python
    extraparams = {"-ffprefixes": ['-re']} # executes as `ffmpeg -re <rest of command>`
    ```

&ensp;


* **`-ffpostfixes`** _(list)_: sets the special FFmpeg parameters(in the middle) that are repeated more than once or occurs in a specific order in the FFmpeg command. Its value can be of datatype **`list`** only and its usage is as follows: 

    ??? alert "This parameter is different from `-clones` and `-ffprefixes`"
        All three `-clones`, `-ffpostfixes`, and `-ffprefixes` parameters even tho fundamentally work the same, they're meant to serve at different places in the FFmpeg command. Normally, FFdecoder API pipeline looks something like following with all three parameters in place:
        ```sh
        ffmpeg {{-ffprefixes FFmpeg params}} -vcodec h264 {{-ffpostfixes FFmpeg params}} -i foo.mp4 -pix_fmt rgb24 -s 1280x720 -framerate 25.0 {{-clones FFmpeg params}} -f rawvideo -
        ```

    !!! tip "Turn on verbose([`verbose = True`](#verbose)) to see the FFmpeg command that is being executed in FFdecoder's pipeline. This helps you debug/address any issues and make adjustments accordingly."
        
    ```python
    extraparams = {"-ffpostfixes": ['-preset', 'fast']} # executes as `ffmpeg -vcodec h264 -preset fast <rest of command>`
    ```

&ensp;

* **`-clones`** _(list)_: sets the special FFmpeg parameters(at the end) that are repeated more than once or occurs in a specific order in the FFmpeg command. Its value can be of datatype **`list`** only and its usage is as follows: 

    ??? alert "This parameter is different from `-ffpostfixes` and `-ffprefixes`"
        All three `-clones`, `-ffpostfixes`, and `-ffprefixes` parameters even tho fundamentally work the same, they're meant to serve at different places in the FFmpeg command. Normally, FFdecoder API pipeline looks something like following with all three parameters in place:
        ```sh
        ffmpeg {{-ffprefixes FFmpeg params}} -vcodec h264 {{-ffpostfixes FFmpeg params}} -i foo.mp4 -pix_fmt rgb24 -s 1280x720 -framerate 25.0 {{-clones FFmpeg params}} -f rawvideo -
        ```

    !!! tip "Turn on verbose([`verbose = True`](#verbose)) to see the FFmpeg command that is being executed in FFdecoder's pipeline. This helps you debug/address any issues and make adjustments accordingly."

    ```python
    extraparams = {"-clones": ['-map', '0:v:0', '-map', '1:a?']} 
    # executes as `ffmpeg -vcodec -i foo.mp4 -pix_fmt rgb24 -s 1280x720 -framerate 25.0 -map 0:v:0 -map 1:a -f rawvideo -
    ```

&ensp;

* **`-custom_sourcer_params`** _(dict)_ : assigns values to Sourcer API's [`source_params`](../../sourcer/params/#sourcer_params) dictionary parameter directly through FFdecoder API. Its usage is as follows: 
    
    ```python
    extraparams = {"-custom_sourcer_params": {"-ffmpeg_download_path": "C:/User/foo/foo1"}}
    # will be assigned to Sourcer API's `source_params` directly
    ```

&ensp;

* **`-passthrough_audio`** _(bool/list)_ : _(Yet to be supported)_

&ensp;


### Supported Decoders

All the decoders that are compiled with FFmpeg in use, are supported by FFdecoder API. You can easily check the compiled decoders by running following command in your terminal:

```sh
# for checking decoders
ffmpeg -decoders           # use `ffmpeg.exe -decoders` on windows
``` 

&nbsp; 
