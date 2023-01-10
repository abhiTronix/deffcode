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

# :octicons-cpu-16: Hardware-Accelerated Video Decoding

!!! abstract "FFmpeg offer access to dedicated GPU hardware with varying support on different platforms for performing a range of video-related tasks to be completed faster or using less of other resources (particularly CPU)."

> By default, DeFFcode's FFdecoder API uses the Input Source's video-decoder _(extracted using Sourcer API)_ itself for decoding its input. However, you could easily change the video-decoder to your desired specific **supported Video-Decoder** using FFmpeg options by way of its [`ffparams`](../../reference/ffdecoder/params/#ffparams) dictionary parameter. This feature provides easy access to GPU Accelerated Hardware Decoder in FFdecoder API that will generate faster video frames:zap: while using little to no CPU power, as opposed to CPU intensive Software Decoders.

We'll discuss its Hardware-Accelerated Video Decoding capabilities briefly in the following recipes:

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

## CUVID-accelerated Hardware-based Video Decoding and Previewing

???+ alert "Example Assumptions"

    **Please note that following recipe explicitly assumes:**

    - You're running :fontawesome-brands-linux: Linux operating system with a [**supported NVIDIA GPU**](https://developer.nvidia.com/nvidia-video-codec-sdk).
    - You're using FFmpeg 4.4 or newer, configured with at least ` --enable-nonfree --enable-cuda-nvcc --enable-libnpp --enable-cuvid --enable-nvenc` configuration flags during compilation. For compilation follow [these instructions ➶](https://docs.nvidia.com/video-technologies/video-codec-sdk/ffmpeg-with-nvidia-gpu/#prerequisites)

    - [x] **Using `h264_cuvid` decoder**: Remember to check if your FFmpeg compiled with H.264 CUVID decoder support by executing following one-liner command in your terminal, and observing if output contains something similar as follows:

        ??? danger "Verifying H.264 CUVID decoder support in FFmpeg"
            ```sh
            $ ffmpeg  -hide_banner -decoders | grep cuvid

            V..... av1_cuvid            Nvidia CUVID AV1 decoder (codec av1)
            V..... h264_cuvid           Nvidia CUVID H264 decoder (codec h264)
            V..... hevc_cuvid           Nvidia CUVID HEVC decoder (codec hevc)
            V..... mjpeg_cuvid          Nvidia CUVID MJPEG decoder (codec mjpeg)
            V..... mpeg1_cuvid          Nvidia CUVID MPEG1VIDEO decoder (codec mpeg1video)
            V..... mpeg2_cuvid          Nvidia CUVID MPEG2VIDEO decoder (codec mpeg2video)
            V..... mpeg4_cuvid          Nvidia CUVID MPEG4 decoder (codec mpeg4)
            V..... vc1_cuvid            Nvidia CUVID VC1 decoder (codec vc1)
            V..... vp8_cuvid            Nvidia CUVID VP8 decoder (codec vp8)
            V..... vp9_cuvid            Nvidia CUVID VP9 decoder (codec vp9)
            ```

            !!! note "You can also use any of above decoder in the similar way, if supported."
            !!! tip "Use `#!sh ffmpeg -decoders` terminal command to lists all FFmpeg supported decoders."

    - You already have appropriate Nvidia video drivers and related softwares installed on your machine.
    - If the stream is not decodable in hardware (for example, it is an unsupported codec or profile) then it will still be decoded in software automatically, but hardware filters won't be applicable.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.

In this example, we will be using Nvidia's **H.264 CUVID Video decoder** in FFdecoder API to achieve GPU-accelerated hardware video decoding of **YUV420p** frames from a given Video file _(say `foo.mp4`)_, and preview them using OpenCV Library's `cv2.imshow()` method.

!!! note "With FFdecoder API, frames extracted with YUV pixel formats _(`yuv420p`, `yuv444p`, `nv12`, `nv21` etc.)_ are generally incompatible with OpenCV APIs such as `imshow()`. But you can make them easily compatible by using exclusive [`-enforce_cv_patch`](../../reference/ffdecoder/params/#b-exclusive-parameters) boolean attribute of its `ffparam` dictionary parameter."

!!! info "More information on Nvidia's CUVID can be found [here ➶](https://developer.nvidia.com/blog/nvidia-ffmpeg-transcoding-guide/)"

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define suitable FFmpeg parameter
ffparams = {
    "-vcodec": "h264_cuvid",  # use H.264 CUVID Video-decoder
    "-enforce_cv_patch": True # enable OpenCV patch for YUV(YUV420p) frames
}

# initialize and formulate the decoder with `foo.mp4` source
decoder = FFdecoder(
    "foo.mp4",
    frame_format="yuv420p",  # use YUV420p frame pixel format
    verbose=True, # enable verbose output
    **ffparams # apply various params and custom filters
).formulate()

# grab the YUV420p frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # convert it to `BGR` pixel format,
    # since imshow() method only accepts `BGR` frames
    frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)

    # {do something with the BGR frame here}

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

## CUDA-accelerated Hardware-based Video Decoding and Previewing

???+ alert "Example Assumptions"

    **Please note that following recipe explicitly assumes:**

    - You're running :fontawesome-brands-linux: Linux operating system with a [**supported NVIDIA GPU**](https://developer.nvidia.com/nvidia-video-codec-sdk).
    - You're using FFmpeg 4.4 or newer, configured with at least ` --enable-nonfree --enable-cuda-nvcc --enable-libnpp  --enable-cuvid --enable-nvenc` configuration flags during compilation. For compilation follow [these instructions ➶](https://docs.nvidia.com/video-technologies/video-codec-sdk/ffmpeg-with-nvidia-gpu/#prerequisites)

        ??? danger "Verifying NVDEC/CUDA support in FFmpeg"

            To use CUDA Video-decoder(`cuda`), remember to check if your FFmpeg compiled with it by executing following commands in your terminal, and observing if output contains something similar as follows:

            ```sh
            $ ffmpeg  -hide_banner -pix_fmts | grep cuda
            ..H.. cuda                   0              0      0
            
            $ ffmpeg  -hide_banner -filters | egrep "cuda|npp"
            ... bilateral_cuda    V->V       GPU accelerated bilateral filter
            ... chromakey_cuda    V->V       GPU accelerated chromakey filter
            ... colorspace_cuda   V->V       CUDA accelerated video color converter
            ... hwupload_cuda     V->V       Upload a system memory frame to a CUDA device.
            ... overlay_cuda      VV->V      Overlay one video on top of another using CUDA
            ... scale_cuda        V->V       GPU accelerated video resizer
            ... scale_npp         V->V       NVIDIA Performance Primitives video scaling and format conversion
            ... scale2ref_npp     VV->VV     NVIDIA Performance Primitives video scaling and format conversion to the given reference.
            ... sharpen_npp       V->V       NVIDIA Performance Primitives video sharpening filter.
            ... thumbnail_cuda    V->V       Select the most representative frame in a given sequence of consecutive frames.
            ... transpose_npp     V->V       NVIDIA Performance Primitives video transpose
            T.. yadif_cuda        V->V       Deinterlace CUDA frames
            ```

    - You already have appropriate Nvidia video drivers and related softwares installed on your machine.
    - If the stream is not decodable in hardware (for example, it is an unsupported codec or profile) then it will still be decoded in software automatically, but hardware filters won't be applicable.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.


In this example, we will be using Nvidia's **CUDA Internal hwaccel Video decoder(`cuda`)** in FFdecoder API to automatically detect best NV-accelerated video codec and keeping video frames in GPU memory _(for applying hardware filters)_, thereby achieving GPU-accelerated decoding of **NV12** pixel-format frames from a given video file _(say `foo.mp4`)_, and preview them using OpenCV Library's `cv2.imshow()` method.

??? warning "`NV12`(for `4:2:0` input) and `NV21`(for `4:4:4` input) are the only supported pixel format. You cannot change pixel format to any other since NV-accelerated video codec supports only them."
    
    NV12 is a biplanar format with a full sized Y plane followed by a single chroma plane with weaved U and V values. NV21 is the same but with weaved V and U values. The 12 in NV12 refers to 12 bits per pixel. NV12 has a half width and half height chroma channel, and therefore is a 420 subsampling. NV16 is 16 bits per pixel, with half width and full height. aka 422. NV24 is 24 bits per pixel with full sized chroma channel. aka 444. Most NV12 functions allow the destination Y pointer to be NULL.

!!! info "With FFdecoder API, frames extracted with YUV pixel formats _(`yuv420p`, `yuv444p`, `nv12`, `nv21` etc.)_ are generally incompatible with OpenCV APIs such as `imshow()`. But you can make them easily compatible by using exclusive [`-enforce_cv_patch`](../../reference/ffdecoder/params/#b-exclusive-parameters) boolean attribute of its `ffparam` dictionary parameter."

!!! note "More information on Nvidia's GPU Accelerated Decoding can be found [here ➶](https://developer.nvidia.com/blog/nvidia-ffmpeg-transcoding-guide/)"

```python
# import the necessary packages
from deffcode import FFdecoder
import cv2

# define suitable FFmpeg parameter
ffparams = {
    "-vcodec": None,  # skip source decoder and let FFmpeg chose
    "-enforce_cv_patch": True # enable OpenCV patch for YUV(NV12) frames
    "-ffprefixes": [
        "-vsync",
        "0",  # prevent duplicate frames
        "-hwaccel",
        "cuda",  # accelerator
        "-hwaccel_output_format",
        "cuda",  # output accelerator
    ],
    "-custom_resolution": "null",  # discard source `-custom_resolution`
    "-framerate": "null",  # discard source `-framerate`
    "-vf": "scale_cuda=640:360,"  # scale to 640x360 in GPU memory
    + "fps=60.0,"  # framerate 60.0fps in GPU memory
    + "hwdownload,"  # download hardware frames to system memory
    + "format=nv12",  # convert downloaded frames to NV12 pixel format
}

# initialize and formulate the decoder with `foo.mp4` source
decoder = FFdecoder(
    "foo.mp4",
    frame_format="null",  # discard source frame pixel format
    verbose=True, # enable verbose output
    **ffparams # apply various params and custom filters
).formulate()

# grab the NV12 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # convert it to `BGR` pixel format,
    # since imshow() method only accepts `BGR` frames
    frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV12)

    # {do something with the BGR frame here}

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
<!--#TODO
???+ danger "Remember to check H.264 CUVID Video-decoder support in FFmpeg"

    To use `h264_cuvid` decoder, remember to check if your FFmpeg compiled with H.264 CUVID decoder support. You can easily do this by executing following one-liner command in your terminal, and observing if output contains something similar as follows:

    ```sh
    $ ffmpeg  -hide_banner -decoders | grep h264 

    VFS..D h264                 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10
    V....D h264_qsv             H264 video (Intel Quick Sync Video acceleration) (codec h264)
    V..... h264_cuvid           Nvidia CUVID H264 decoder (codec h264)
    ```

    !!! tip "You can also use optimized HEVC CUVID Video-decoder(`hevc_cuvid`) in the similar way, if supported."
-->


&nbsp;