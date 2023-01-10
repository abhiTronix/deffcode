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

# :fontawesome-solid-microchip: Hardware-Accelerated Video Transcoding

???+ abstract "What exactly is Transcoding?"

    > Transcoding is the technique of transforming one media encoding format into another. 

    This is typically done for compatibility purposes, such as when a media source provides a format that the intended target is not able to process; an in-between adaptation step is required:

    - **Decode** media from its originally encoded state into raw, uncompressed information.
    - **Encode** the raw data back, using a different codec that is supported by end user.

> DeFFcode's FFdecoder API in conjunction with VidGear's WriteGear API is able to exploit almost any FFmpeg parameter for achieving anything imaginable with multimedia video data all while **allowing us to process real-time video frames** with immense flexibility. Both these APIs are capable of utilizing the potential of GPU backed fully-accelerated **Hardware based video Decoding(FFdecoder API with hardware decoder) and Encoding (WriteGear API with hardware encoder)**, thus dramatically improving the transcoding performance. At same time, FFdecoder API Hardware-decoded frames are **fully compatible with OpenCV's VideoWriter API** for producing  high-quality output video in real-time. 

??? danger "Limitation: Bottleneck in Hardware-Accelerated Video Transcoding performance with Real-time Frame processing"

    As we know, using the `–hwaccel cuda -hwaccel_output_format cuda` flags in FFmpeg pipeline will keep video frames in GPU memory, and this ensures that the memory transfers (system memory to video memory and vice versa) are eliminated, and that transcoding is performed with the highest possible performance on the available GPU hardware.

    <figure markdown>
      ![HW Acceleration](../../../assets/images/hw_accel.png){ width="350" }
      <figcaption>General Memory Flow with Hardware Acceleration</figcaption>
    </figure>
    
    But unfortunately, for processing real-time frames in our python script with FFdecoder and WriteGear APIs, we're bound to sacrifice this performance gain by explicitly copying raw decoded frames between System and GPU memory _(via the PCIe bus)_, thereby creating self-made latency in transfer time and increasing PCIe bandwidth occupancy due to overheads in communication over the bus. Moreover, given PCIe bandwidth limits, copying uncompressed image data would quickly saturate the PCIe bus. 

    <figure markdown>
      ![HW Acceleration Limitation](../../../assets/images/hw_accel_limitation.png){ width="350" }
      <figcaption>Memory Flow with Hardware Acceleration <br>and Real-time Processing</figcaption>
    </figure>

    On the bright side, however, GPU enabled Hardware based encoding/decoding is inherently faster and more efficient _(do not use much CPU resources when frames in GPU)_ thus freeing up the CPU for other tasks, as compared to Software based encoding/decoding that is known to be completely CPU intensive. Plus scaling, de-interlacing, filtering, etc. tasks will be way faster and efficient than usual using these Hardware based decoders/encoders as oppose to Software ones.

    !!! summary "As you can see the pros definitely outweigh the cons and you're getting to process video frames in the real-time with immense speed and flexibility, which is impossible to do otherwise."

We'll discuss its Hardware-Accelerated Video Transcoding capabilities using these APIs briefly in the following recipes:

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

    - [x] **VidGear:** VidGear is required for lossless encoding of video frames into file/stream. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ```sh
        pip install vidgear[core]       
        ```

!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."


&thinsp;


## CUDA-accelerated Video Transcoding with OpenCV's VideoWriter API 

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

        ??? danger "Verifying H.264 NVENC encoder support in FFmpeg"

            To use NVENC Video-encoder(`cuda`), remember to check if your FFmpeg compiled with H.264 NVENC encoder support. You can easily do this by executing following one-liner command in your terminal, and observing if output contains something similar as follows:

            ```sh
            $ ffmpeg  -hide_banner -encoders | grep nvenc 

            V....D av1_nvenc            NVIDIA NVENC av1 encoder (codec av1)
            V....D h264_nvenc           NVIDIA NVENC H.264 encoder (codec h264)
            V....D hevc_nvenc           NVIDIA NVENC hevc encoder (codec hevc)
            ```

            !!! note "You can also use other NVENC encoder in the similar way, if supported."
        

    - You already have appropriate Nvidia video drivers and related softwares installed on your machine.
    - If the stream is not decodable in hardware (for example, it is an unsupported codec or profile) then it will still be decoded in software automatically, but hardware filters won't be applicable.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.


In this example, we will be: 

1. Using Nvidia's **CUDA Internal hwaccel Video decoder(`cuda`)** in FFdecoder API to automatically detect best NV-accelerated video codec and keeping video frames in GPU memory _(for applying hardware filters)_ for achieving GPU-accelerated decoding of a given video file _(say `foo.mp4`)_.
2. Scaling and Cropping decoded frames in GPU memory.
3. Downloading decoded frames into system memory as patched **NV12** frames.
4. Converting **NV12** frames into **BGR** pixel-format using OpenCV's `cvtcolor` method.
5. Encoding **BGR** frames with OpenCV's VideoWriter API.

!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate."

!!! note "With FFdecoder API, frames extracted with YUV pixel formats _(`yuv420p`, `yuv444p`, `nv12`, `nv21` etc.)_ are generally incompatible with OpenCV APIs such as `imshow()`. But you can make them easily compatible by using exclusive [`-enforce_cv_patch`](../../reference/ffdecoder/params/#b-exclusive-parameters) boolean attribute of its `ffparam` dictionary parameter."

!!! info "More information on Nvidia's NVENC Encoder can be found [here ➶](https://developer.nvidia.com/blog/nvidia-ffmpeg-transcoding-guide/)"

```python
# import the necessary packages
from deffcode import FFdecoder
import json
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
    "-vf": "scale_cuda=640:360," # scale to 640x360 in GPU memory
    + "crop=80:60:200:100," # crop a 80×60 section from position (200, 100) in GPU memory
    + "hwdownload,"  # download hardware frames to system memory
    + "format=nv12",  # convert downloaded frames to NV12 pixel format
}

# initialize and formulate the decoder with `foo.mp4` source
decoder = FFdecoder(
    "foo.mp4",
    frame_format="null",  # discard source frame pixel format
    verbose = False, # to avoid too much clutter
    **ffparams # apply various params and custom filters
).formulate()

# retrieve JSON Metadata and convert it to dict
metadata_dict = json.loads(decoder.metadata)

# prepare OpenCV parameters
FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
FRAMERATE = metadata_dict["output_framerate"]
FRAMESIZE = tuple(metadata_dict["output_frames_resolution"])

# Define writer with parameters and suitable output filename for e.g. `output_foo_gray.avi`
writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

# grab the NV12 frames from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # convert it to `BGR` pixel format,
    # since write() method only accepts `BGR` frames
    frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV12)

    # {do something with the BGR frame here}

    # writing BGR frame to writer
    writer.write(frame)

# close output window
cv2.destroyAllWindows()

# terminate the decoder
decoder.terminate()

# safely close writer
writer.close()
```

&nbsp;


## CUDA-NVENC-accelerated Video Transcoding with WriteGear API 

!!! warning "==WriteGear's Compression Mode support for FFdecoder API is currently in beta so you can expect much higher than usual CPU utilization!=="

??? quote "Lossless transcoding  with FFdecoder and WriteGear API"
    
    VidGear's [**WriteGear API**](https://abhitronix.github.io/vidgear/latest/gears/writegear/introduction/) implements a complete, flexible, and robust wrapper around FFmpeg in [compression mode](https://abhitronix.github.io/vidgear/latest/gears/writegear/compression/overview/) for encoding real-time video frames to a lossless compressed multimedia output file(s)/stream(s). 

    DeFFcode's FFdecoder API in conjunction with WriteGear API creates a high-level **High-performance Lossless FFmpeg Transcoding _(Decoding + Encoding)_ Pipeline** :fire: that is able to exploit almost any FFmpeg parameter for achieving anything imaginable with multimedia video data all while allow us to manipulate the real-time video frames with immense flexibility.

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

        ??? danger "Verifying H.264 NVENC encoder support in FFmpeg"

            To use NVENC Video-encoder(`cuda`), remember to check if your FFmpeg compiled with H.264 NVENC encoder support. You can easily do this by executing following one-liner command in your terminal, and observing if output contains something similar as follows:

            ```sh
            $ ffmpeg  -hide_banner -encoders | grep nvenc 

            V....D av1_nvenc            NVIDIA NVENC av1 encoder (codec av1)
            V....D h264_nvenc           NVIDIA NVENC H.264 encoder (codec h264)
            V....D hevc_nvenc           NVIDIA NVENC hevc encoder (codec hevc)
            ```

            !!! note "You can also use other NVENC encoder in the similar way, if supported."
        

    - You already have appropriate Nvidia video drivers and related softwares installed on your machine.
    - If the stream is not decodable in hardware (for example, it is an unsupported codec or profile) then it will still be decoded in software automatically, but hardware filters won't be applicable.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.

??? info "Additional Parameters in WriteGear API"
    WriteGear API only requires a valid Output filename _(e.g. `output_foo.mp4`)_ as input, but you can easily control any output specifications _(such as bitrate, codec, framerate, resolution, subtitles, etc.)_ supported by FFmpeg _(in use)_.

!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate."

=== "Consuming `BGR` frames"

    In this example, we will be: 
    
    1. Using Nvidia's **CUDA Internal hwaccel Video decoder(`cuda`)** in FFdecoder API to automatically detect best NV-accelerated video codec and keeping video frames in GPU memory _(for applying hardware filters)_ for achieving GPU-accelerated decoding of a given video file _(say `foo.mp4`)_.
    2. Scaling and Cropping decoded frames in GPU memory.
    3. Downloading decoded frames into system memory as patched **NV12** frames.
    4. Converting patched **NV12** frames into **BGR** pixel-format using OpenCV's `cvtcolor` method.
    4. Encoding **BGR** frames with WriteGear API using Nvidia's Hardware accelerated **H.264 NVENC Video-encoder(`h264_nvenc`)** into lossless video file in the GPU memory. 
        

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json
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
        + "crop=80:60:200:100," # crop a 80×60 section from position (200, 100) in GPU memory
        + "hwdownload,"  # download hardware frames to system memory
        + "format=nv12",  # convert downloaded frames to NV12 pixel format
    }

    # initialize and formulate the decoder with `foo.mp4` source
    decoder = FFdecoder(
        "foo.mp4",
        frame_format="null",  # discard source frame pixel format
        verbose = False, # to avoid too much clutter
        **ffparams # apply various params and custom filters
    ).formulate()

    # retrieve framerate from JSON Metadata and pass it as
    # `-input_framerate` parameter for controlled framerate
    output_params = {
        "-input_framerate": json.loads(decoder.metadata)["output_framerate"],
        "-vcodec": "h264_nvenc", # H.264 NVENC Video-encoder

    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo.mp4`
    writer = WriteGear(output="output_foo.mp4", logging=True, **output_params)

    # grab the NV12 frames from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # convert it to `BGR` pixel format
        frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV12)

        # {do something with the BGR frame here}

        # writing BGR frame to writer
        writer.write(frame)

    # close output window
    cv2.destroyAllWindows()

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```
    
=== "Consuming `NV12` frames"

    In this example, we will be: 

    1. Using Nvidia's **CUDA Internal hwaccel Video decoder(`cuda`)** in FFdecoder API to automatically detect best NV-accelerated video codec and keeping video frames in GPU memory _(for applying hardware filters)_ for achieving GPU-accelerated decoding of a given video file _(say `foo.mp4`)_.
    2. Scaling and Cropping decoded frames in GPU memory.
    3. Downloading decoded frames into system memory as **NV12** frames.
    4. Encoding **NV12** frames directly with WriteGear API using Nvidia's Hardware accelerated **H.264 NVENC Video-encoder(`h264_nvenc`)** into lossless video file in the GPU memory. 

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from vidgear.gears import WriteGear
    import json
    import cv2

    # define suitable FFmpeg parameter
    ffparams = {
        "-vcodec": None,  # skip source decoder and let FFmpeg chose
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
        + "crop=80:60:200:100,"  # crop a 80×60 section from position (200, 100) in GPU memory
        + "hwdownload,"  # download hardware frames to system memory
        + "format=nv12",  # convert downloaded frames to NV12 pixel format
    }

    # initialize and formulate the decoder with `foo.mp4` source
    decoder = FFdecoder(
        "foo.mp4",
        frame_format="null",  # discard source frame pixel format
        verbose = False, # to avoid too much clutter
        **ffparams # apply various params and custom filters
    ).formulate()

    # retrieve framerate from JSON Metadata and pass it as
    # `-input_framerate` parameter for controlled framerate
    output_params = {
        "-input_framerate": json.loads(decoder.metadata)["output_framerate"],
        "-vcodec": "h264_nvenc", # H.264 NVENC Video-encoder
        "-input_pixfmt": "nv12", # input frames pixel format as `NV12`
    }

    # Define writer with default parameters and suitable
    # output filename for e.g. `output_foo.mp4`
    writer = WriteGear(output="output_foo.mp4", logging=True, **output_params)

    # grab the NV12 frames from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break

        # {do something with the NV12 frame here}

        # writing NV12 frame to writer
        writer.write(frame)

    # close output window
    cv2.destroyAllWindows()

    # terminate the decoder
    decoder.terminate()

    # safely close writer
    writer.close()
    ```

&nbsp;

## CUDA-NVENC-accelerated End-to-end Lossless Video Transcoding with WriteGear API 

> DeFFcode's FFdecoder API in conjunction with VidGear's WriteGear API creates a **High-performance Lossless FFmpeg Transcoding Pipeline :fire:**

<figure>
<img src="https://media.tenor.com/qHM65-yUyp4AAAAi/were-working-on-it-stan-marsh.gif" loading="lazy" alt="help-shouting" />
<figcaption>Courtesy - <a href="https://tenor.com/view/were-working-on-it-stan-marsh-south-park-clubhouses-s2e12-gif-21568854">tenor</a></figcaption>
</figure>



