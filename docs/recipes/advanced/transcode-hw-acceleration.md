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

??? abstract "What exactly is Transcoding?"

    Before heading directly into recipes we have to talk about Transcoding: 
    
    > Transcoding is the technique of transforming one media encoding format into another. 

    This is typically done for compatibility purposes, such as when a media source provides a format that the intended target is not able to process; an in-between adaptation step is required:

    - **Decode** media from its originally encoded state into raw, uncompressed information.
    - **Encode** the raw data back, using a different codec that is supported by end user.

> DeFFcode's FFdecoder API in conjunction with VidGear's WriteGear API creates a high-level **High-performance Lossless FFmpeg Transcoding _(Decoding & Encoding respectively)_ Pipeline :fire:** that is able to exploit almost any FFmpeg parameter for achieving anything imaginable with multimedia video data all while allow us to manipulate the real-time video frames with immense flexibility. Both these APIs are capable of utilizing the potential of GPU supported fully-accelerated **Hardware based video Decoding(FFdecoder API with hardware decoder) and Encoding (WriteGear API with hardware encoder)**, thus dramatically improving the performance of the end-to-end transcoding.

We'll discuss its Hardware-Accelerated Video Transcoding capabilities using these APIs briefly in the following recipes:

&thinsp;


!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

???+ info "Additional Python Dependencies for following recipes"

    Following recipes requires additional python dependencies which can be installed easily as below:

    - [x] **VidGear:** VidGear is required for lossless encoding of video frames into file/stream. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ```sh
        pip install vidgear[core]       
        ```

!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

!!! danger "==WriteGear's Compression Mode support for FFdecoder API is currently in beta so you can expect much higher than usual CPU utilization!=="

&thinsp;

## GPU-accelerated Hardware-based Video Transcoding with WriteGear API 

???+ alert "Example Assumptions"

    **Please note that following recipe explicitly assumes:**

    - You're running :fontawesome-brands-windows: Windows operating system with a [**supported NVIDIA GPU**](https://developer.nvidia.com/nvidia-video-codec-sdk).
    - You're using FFmpeg 4.4 or newer, configured with atleast `--enable-nonfree --enable-libx264 --enable-cuda --enable-nvenc --enable-nvdec --enable-cuda-nvcc --enable-libnpp` options during compilation.  For manual compilation follow [these instructions ➶](https://docs.nvidia.com/video-technologies/video-codec-sdk/ffmpeg-with-nvidia-gpu/#prerequisites)
    - You already have appropriate Nvidia video drivers and related softwares installed on your machine.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.


??? danger "Limitation: Bottleneck in Hardware-Accelerated Video Transcoding Performance"

    Generally, adding the `–hwaccel cuvid`/`–hwaccel cuda -hwaccel_output_format cuda` options means the raw decoded frames will not be copied between system and GPU memory _(via the PCIe bus)_, and the transcoding will be faster and use less system resources, and may even result in up to 2x the throughput compared to the unoptimized calls:

    <figure markdown>
      ![HW Acceleration](../../../assets/images/hw_accel.png){ width="350" }
      <figcaption>General Memory Flow with Hardware Acceleration</figcaption>
    </figure>
    
    But unfortunately, for processing real-time frames in our python script with FFdecoder and WriteGear APIs, we're bound to sacrifice this performance gained by explicitly copying raw decoded frames between System and GPU memory via the PCIe bus, thereby creating self-made latency in transfer time and increasing PCIe bandwidth occupancy due to overheads in communication over the bus. Also, given PCIe bandwidth limits, copying uncompressed image data would quickly saturate the PCIe bus. 

    <figure markdown>
      ![HW Acceleration Limitation](../../../assets/images/hw_accel_limitation.png){ width="350" }
      <figcaption>Memory Flow with Hardware Acceleration <br>and Real-time Processing</figcaption>
    </figure>

    On the bright side however, GPU supported hardware based encoding/decoding is inherently faster and more efficient _(do not use much CPU resources)_ thus freeing up the CPU for other tasks, as compared to software based encoding/decoding that is generally known to be quite CPU intensive. Plus scaling, deinterlacing, filtering, and other post-processing tasks will be faster than usual using these hardware based decoders/encoders with same equivalent output to software ones, and will use less power and CPU to do so. 

    !!! summary "On the whole, You don't have to worry about it as you're getting to manipulate the real-time video frames with immense speed and flexibility which is impossible to do otherwise."

In this example, we will be using Nvidia's Hardware Accerlated **CUDA Video-decoder(`cuda`)** in FFdecoder API to decode and keep decoded **YUV420p** frames from a given Video file _(say `foo.mp4`)_ within GPU, all while rescaling _(with nvcuvid's `resize`)_ as well as encoding them in real-time with WriteGear API using Nvidia's hardware accelerated **H.264 NVENC Video-encoder(`h264_nvenc`)** into lossless video file within GPU. 

??? note "Remember to check H.264 NVENC encoder support in FFmpeg"

    - [x] **Using `h264_nvenc` encoder**: Remember to check if your FFmpeg compiled with H.264 NVENC encoder support. You can easily do this by executing following one-liner command in your terminal, and observing if output contains something similar as follows:

        ```sh
        $ ffmpeg  -hide_banner -encoders | grep nvenc 

        V....D h264_amf             AMD AMF H.264 Encoder (codec h264)
        V....D h264_mf              H264 via MediaFoundation (codec h264)
        V....D h264_nvenc           NVIDIA NVENC H.264 encoder (codec h264)
        ```

        !!! note "You can also use optimized HEVC NVENC encoder(`hevc_nvenc`) in the similar way, if supported."

!!! info "Additional Parameters in WriteGear API"
    
    WriteGear API only requires a valid Output filename _(e.g. `output_foo.mp4`)_ as input, but you can easily control any output specifications _(such as bitrate, codec, framerate, resolution, subtitles, etc.)_ supported by FFmpeg _(in use)_.

!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate."


!!! warning "YUV video-frames decoded with DeFFcode APIs are not yet supported by OpenCV methods."
    Currently, there's no way to use DeFFcode APIs decoded YUV video-frames in OpenCV methods, and also you cannot change pixel format to any other due to NV-accelerated video codec supporting only few pixel-formats.


```python
# import the necessary packages
from deffcode import FFdecoder
from vidgear.gears import WriteGear
import json

# define suitable FFmpeg parameter
ffparams = {
    "-vcodec": None,  # skip any decoder and let FFmpeg chose
    "-ffprefixes": [
        "-vsync",
        "0",
        "-hwaccel", # chooses appropriate HW accelerator
        "cuda",
        "-hwaccel_output_format", # keeps the decoded frames in GPU memory
        "cuda",
    ],
    "-custom_resolution": "null",  # discard `-custom_resolution`
    "-framerate": "null",  # discard `-framerate`
    "-vf": "scale_npp=format=yuv420p,hwdownload,format=yuv420p,fps=30.0",  # define your filters
}

# initialize and formulate the decoder with params and custom filters
decoder = FFdecoder(
    "foo.mp4", frame_format="null", verbose=True, **ffparams  # discard frame_format
).formulate()

# retrieve framerate from JSON Metadata and pass it as 
# `-input_framerate` parameter for controlled framerate
# and add input pixfmt as yuv420p also
output_params = {
    "-input_framerate": json.loads(decoder.metadata)["output_framerate"],
    "-vcodec": "h264_nvenc",
    "-input_pixfmt": "yuv420p"
}

# Define writer with default parameters and suitable
# output filename for e.g. `output_foo_yuv.mp4`
writer = WriteGear(output_filename="output_foo_yuv.mp4", **output_params)

# grab the YUV420 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing YUV420 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.close()
```

&nbsp;