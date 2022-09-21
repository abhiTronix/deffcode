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

> By default, DeFFcode's FFdecoder API uses the Input Source's video-decoder _(extracted using Sourcer API)_ itself for decoding its input. However, you could easily change the video-decoder to your desired specific **supported Video-Decoder** using FFmpeg options by way of its [`ffparams`](../../reference/ffdecoder/params/#ffparams) dictionary parameter. This means easy access to GPU Accelerated Hardware Decoder to get better playback and accelerated video decoding on GPUs that will generate equivalent output to software decoders, but may use less power and CPU to do so.

!!! tip "Use `#!sh ffmpeg -decoders` terminal command to lists all FFmpeg supported decoders."

We'll discuss its Hardware-Accelerated Video Decoding capabilities briefly in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.


!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

??? danger "Never name your python script `deffcode.py`"

    When trying out these recipes, never name your python script `deffcode.py` otherwise it will result in `ModuleNotFound` error.

&thinsp;

## GPU-accelerated Hardware-based Video Decoding

???+ alert "Example Assumptions"

    **Please note that following recipe explicitly assumes:**

    - You're running :fontawesome-brands-windows: Windows operating system with a [**supported NVIDIA GPU**](https://developer.nvidia.com/nvidia-video-codec-sdk).
    - You're using FFmpeg 4.4 or newer, configured with atleast `--enable-nonfree --enable-libx264 --enable-cuda --enable-cuvid --enable-cuda-nvcc` options during compilation. For manual compilation follow [these instructions ➶](https://docs.nvidia.com/video-technologies/video-codec-sdk/ffmpeg-with-nvidia-gpu/#prerequisites)
    - You already have appropriate Nvidia video drivers and related softwares installed on your machine.

    These assumptions **MAY/MAY NOT** suit your current setup. Kindly use suitable parameters based your system platform and hardware settings only.


In this example, we will be using Nvidia's Hardware Accerlated **CUDA Video-decoder(`cuda`)** in FFdecoder API to automatically detect NV-accelerated video codec and achieve GPU-accelerated hardware video decoding of **YUV420p** frames from a given Video file _(say `foo.mp4`)_ on :fontawesome-brands-windows: Windows Machine.

!!! info "More information on Nvidia's CUVID can be found [here ➶](https://developer.nvidia.com/blog/nvidia-ffmpeg-transcoding-guide/)"

!!! warning "YUV video-frames decoded with DeFFcode APIs are not yet supported by OpenCV methods."
    Currently, there's no way to use DeFFcode APIs decoded YUV video-frames in OpenCV methods, and also you cannot change pixel format to any other due to NV-accelerated video codec supporting only few pixel-formats.

!!! note "To learn about exclusive `-ffprefixes` parameter. See [Exclusive Parameters ➶](../../reference/ffdecoder/params/#b-exclusive-parameters)"

```python
# import the necessary packages
from deffcode import FFdecoder
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

# grab the YUV420 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

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
<!--#TODO
    # Show output window
    cv2.imshow("Output", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
-->


&nbsp;