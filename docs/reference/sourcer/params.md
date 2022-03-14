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

!!! warning "Sourcer API will throw `RuntimeError` if `source` provided is invalid or missing."


This parameter defines the default input source.


**Data-Type:** String.

Its valid input can be one of the following: 

- [x] **Filepath:** _Valid path of the video file, for e.g `"/home/foo.mp4"` as follows:_

    !!! alert "Multiple video file paths are not yet support!"

    ```python
    decoder = Sourcer('/home/foo.mp4').formulate()
    ```

- [x] **Image Sequence:** _Valid image sequence such as sequential `'img%03d.png'` or `'*.png'` glob pattern or even single(loop) image as input:_

    
    === "Sequential"

        ```python
        # initialize and formulate the decoder
        decoder = Sourcer('img%03d.png').formulate()
        ```

        You can use `-start_number` FFmpeg parameter if you want to start with specific number:

        ```python
        # define `-start_number` such as `5`
        sourcer_params = {"-ffpostfixes":["-start_number", "5"]}

        # initialize and formulate the decoder with define parameters
        decoder = Sourcer('img%03d.png', verbose=True, **sourcer_params).formulate()
        ```

    === "Glob pattern"

        Bash-style globbing _(`*` represents any number of any characters)_ is useful if your images are sequential but not necessarily in a numerically sequential order. You can do it as follows:

        !!! warning "The glob pattern is not available on Windows builds."

        ```python
        # define `-pattern_type glob` for accepting glob pattern
        sourcer_params = {"-ffprefixes":["-pattern_type", "glob"]}

        # initialize and formulate the decoder with define parameters
        decoder = Sourcer('img*.png', verbose=True, **sourcer_params).formulate()
        ```

    === "Single image"

        You can use a single looping image as follows:

        ```python
        # define `-loop 1` for looping
        sourcer_params = {"-ffprefixes":["-loop", "1"]}

        # initialize and formulate the decoder with define parameters
        decoder = Sourcer('img.jpg', verbose=True, **sourcer_params).formulate()
        ```

- [x] **Network Address:** _Valid (`http(s)`, `rtp`, `rstp`, `rtmp`, `mms`, etc.) incoming network stream address such as `'rtsp://xx:yy@192.168.1.ee:fd/av0_0'` as input:_

    ```python
    # define `rtsp_transport` or necessary parameters 
    sourcer_params = {"-ffpostfixes":["-rtsp_transport", "tcp"]}

    # initialize and formulate the decoder with define parameters
    decoder = Sourcer('rtsp://xx:yy@192.168.1.ee:fd/av0_0', verbose=True, **sourcer_params).formulate()
    ```

- [ ] **Video Input devices:** _(Yet to be supported)_

- [ ] **Screen Capture:** _(Yet to be supported)_


&nbsp;


## **`custom_ffmpeg`**

This parameter assigns the custom _path/directory_ where the custom/downloaded FFmpeg executables are located.

!!! info "Behavior on Windows"
    
    If a custom FFmpeg executable's path | directory is not provided through `custom_ffmpeg` parameter on Windows machine, then Sourcer API will ==automatically attempt to download and extract suitable Static FFmpeg binaries at suitable location on your windows machine==. More information can be found [here ➶](../ffmpeg_install/#a-auto-installation).

**Data-Type:** String

**Default Value:** Its default value is `None`.

**Usage:**

```python
# If ffmpeg executables are located at "/foo/foo1/ffmpeg"
Sourcer("foo.mp4", custom_ffmpeg="/foo/foo1/ffmpeg").formulate()
```

&nbsp;


## **`verbose`**

This parameter enables verbose _(if `True`)_, essential for debugging. 

**Data-Type:** Boolean

**Default Value:** Its default value is `False`.

**Usage:**

```python
Sourcer("foo.mp4", verbose=True).formulate()
```

&nbsp; 


## **`sourcer_params`**

This parameter accepts few [Exclusive Parameters](#exclusive-parameters) formatted as as its attributes:

!!! danger "Kindly read docs carefully before passing any additional values to `sourcer_params` parameter. Wrong invalid values may result in undesired errors or no output at all."


**Data-Type:** Dictionary

**Default Value:** Its default value is `{}`.


### Exclusive Parameters

Sourcer API supports only few Exclusive Parameters to flexibly alter its internal properties. These parameters are discussed below:

* **`-ffmpeg_download_path`** _(string)_: sets the custom directory for downloading FFmpeg Static Binaries in Compression Mode, during the [Auto-Installation](../ffmpeg_install/#a-auto-installation) on Windows Machines Only. If this parameter is not altered, then these binaries will auto-save to the default temporary directory (for e.g. `C:/User/temp`) on your windows machine. It can be used as follows: 

    ```python
    sourcer_params = {"-ffmpeg_download_path": "C:/User/foo/foo1"} # will be saved to "C:/User/foo/foo1"
    ```

* **`-force_validate_source`** _(bool)_: forcefully passes validation test for given `source` which is required for some special cases with unusual input. It can be used as follows: 

    ```python
    sourcer_params = {"-force_validate_source": True} # will pass validation test forcefully
    ```
