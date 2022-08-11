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

# Basic Recipes :cake:


The following recipes should be reasonably accessible to beginners of any skill level to get started with DeFFcode APIs:


<figure>
<img src="https://c.tenor.com/uYqsM9uIyuYAAAAC/simple-easy.gif" loading="lazy" alt="easy-easy-game-easy-life-deal-with-it" />
<figcaption>Courtesy - <a href="https://tenor.com/view/simple-easy-easy-game-easy-life-deal-with-it-gif-9276124">tenor</a></figcaption>
</figure>

!!! alert "Refer Installation doc first!"

    If this is your first time using DeFFcode, head straight to the **[Installation Notes](../../installation/#installation-notes) to install DeFFcode with required prerequisites on your machine**.


??? tip "Any proficiency with OpenCV-Python will be Helpful"
    
    If you've any proficiency with [**OpenCV-Python**](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) _(Python API for OpenCV)_, you will find these recipes really easy. 

??? question "Wanna suggest any improvements or additional recipes?"

    Please feel free to suggest any improvements or additional recipes on our [**Gitter community channel ➶**][gitter]

??? info "Frames are actually 3D Numpy arrays"
    
    In python, "**Frames**" are actually three-dimensional :material-video-3d: [NumPy `ndarray`](https://numpy.org/doc/stable/reference/arrays.ndarray.html) composed of 3 nested levels of arrays, one for each dimension.


&thinsp;

## Basic :material-movie-play: Decoding Recipes

- [x] **[:material-file-eye: Decoding Video files](../basic/decode-video-files/#decoding-video-files)**
    - [Accessing RGB frames from a video file](../basic/decode-video-files/#accessing-rgb-frames-from-a-video-file)
    - [Capturing and Previewing BGR frames from a video file](../basic/decode-video-files/#capturing-and-previewing-bgr-frames-from-a-video-file) _(OpenCV Support)_
    - [Playing with any other FFmpeg pixel formats](../basic/decode-video-files/#capturing-and-previewing-bgr-frames-from-a-video-file)
- [x] **[:material-webcam: Decoding Live Feed Devices](../basic/decode-live-feed-devices/#decoding-live-feed-devices)**
    - [Capturing and Previewing frames from a Webcam](../basic/decode-live-feed-devices/#capturing-and-previewing-frames-from-a-webcam)
    - [Capturing and Previewing frames from your Desktop](../basic/decode-live-feed-devices/#capturing-and-previewing-frames-from-your-desktop) _(Screen Recording)_
- [x] **[:fontawesome-solid-cloud-arrow-down: Decoding Network Streams](../basic/decode-network-streams/#decoding-network-streams)**
    - [Capturing and Previewing frames from a HTTPs Stream](../basic/decode-network-streams/#capturing-and-previewing-frames-from-a-https-stream)
    - [Capturing and Previewing frames from a RTSP/RTP Stream](../basic/decode-network-streams/#capturing-and-previewing-frames-from-a-rtsprtp-stream)
- [x] **[:material-image-multiple: Decoding Image sequences](../basic/decode-image-sequences/#decoding-image-sequences)**
    - [Capturing and Previewing frames from Sequence of images](../basic/decode-image-sequences/#capturing-and-previewing-frames-from-sequence-of-images)
    - [Capturing and Previewing frames from Single looping image](../basic/decode-image-sequences/#capturing-and-previewing-frames-from-single-looping-image)

<div class="spacer"></div>

## Basic :material-movie-edit: Transcoding Recipes

- [x] **[:material-video-image: Transcoding Live frames](../basic/transcode-live-frames/)**
    - [Transcoding video using OpenCV VideoWriter API](../basic/transcode-live-frames/#transcoding-video-using-opencv-videowriter-api)
    - [Transcoding lossless video using WriteGear API](../basic/transcode-live-frames/#transcoding-lossless-video-using-writegear-api)
- [x] **[:material-movie-filter: Transcoding Live Simple Filtergraphs](../basic/transcode-live-frames-simplegraphs/#transcoding-live-simple-filtergraphs)**
    - [Transcoding Trimmed and Reversed video](../basic/transcode-live-frames-simplegraphs/#transcoding-trimmed-and-reversed-video)
    - [Transcoding Cropped video](../basic/transcode-live-frames-simplegraphs/#transcoding-cropped-video)
    - [Transcoding Rotated video (with `rotate` filter)](../basic/transcode-live-frames-simplegraphs/#transcoding-rotated-video-with-rotate-filter)
    - [Transcoding Rotated video (with `transpose` filter)](../basic/transcode-live-frames-simplegraphs/#transcoding-rotated-video-with-transpose-filter)   
    - [Transcoding Horizontally flipped and Scaled video](../basic/transcode-live-frames-simplegraphs/#transcoding-horizontally-flipped-and-scaled-video)
- [x] **[:material-fast-forward-60: Saving Key-frames as Image](../basic/save-keyframe-image/#saving-key-frames-as-image)** _(Image processing)_
    - [Extracting Key-frames as PNG image](../basic/save-keyframe-image/#extracting-key-frames-as-png-image)
    - [Generating Thumbnail with a Fancy filter](../basic/save-keyframe-image/#generating-thumbnail-with-a-fancy-filter)

<div class="spacer"></div>

## Basic :material-movie-search: Metadata Recipes

- [x] **[:material-file-cog: Extracting Video Metadata](../basic/extract-video-metadata/#extracting-video-metadata)**
    - [Extracting video metadata using Sourcer API](../basic/extract-video-metadata/#extracting-video-metadata-using-sourcer-api)
    - [Extracting video metadata using FFdecoder API](../basic/extract-video-metadata/#extracting-video-metadata-using-ffdecoder-api)



&thinsp;


## What's next?

!!! success "Done already! Let's checkout [Advanced Recipes :croissant:](../advanced) to level up :fontawesome-solid-arrow-up-wide-short: your skills! " 


&thinsp;


<!--
External URLs
-->
[gitter]: https://gitter.im/deffcode-python/community
[ffmpeg]:https://www.ffmpeg.org/