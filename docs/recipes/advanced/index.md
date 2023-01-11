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

# Advanced Recipes :croissant:


The following challenging recipes will take your skills to the next level and will give access to new DeFFcode techniques, tricky examples, and advanced FFmpeg parameters:

<figure>
<img src="https://c.tenor.com/x-5ZtqDFt6sAAAAC/challenge-accepted-let-the-challenge-commence.gif" loading="lazy" alt="challenge-accepted-let-the-challenge-commence" />
<figcaption>Courtesy - <a href="https://tenor.com/view/challenge-accepted-let-the-challenge-commence-elmo-on-fire-flaming-gif-17013941">tenor</a></figcaption>
</figure>


!!! alert "Refer Basic Recipes first!"

    If you're just getting started, check out the Beginner's [**Basic Recipes :cake:**](../basic) first before trying these advanced recipes.

??? tip "Any proficiency with OpenCV-Python will be Helpful"
    
    Any proficiency with [**OpenCV-Python**](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) _(Python API for OpenCV)_ surely help you with these recipes. 

??? question "Wanna suggest any improvements or additional recipes?"

    Please feel free to suggest any improvements or additional recipes on our [**Gitter community channel ➶**][gitter]


&thinsp;

## Advanced :material-movie-play: Decoding Recipes
- [x] **[:material-file-hidden: Decoding Live Virtual Sources](../advanced/decode-live-virtual-sources/#decoding-live-virtual-sources)**
    - [Generate and Decode frames from Sierpinski pattern](../advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-sierpinski-pattern)
    - [Generate and Decode frames from Test Source pattern](../advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-test-source-pattern)
    - [Generate and Decode frames from Gradients with custom Text effect](../advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-gradients-with-custom-text-effect)
    - [Generate and Decode frames from Mandelbrot test pattern with vectorscope & waveforms](../advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-mandelbrot-test-pattern-with-vectorscope-waveforms)
    - [Generate and Decode frames from Game of Life Visualization](../advanced/decode-live-virtual-sources/#generate-and-decode-frames-from-game-of-life-visualization)
- [x] **[:material-camera-iris: Decoding Live Feed Devices](../advanced/decode-live-feed-devices)**
    - [Capturing and Previewing frames from a Webcam using Custom Demuxer](../advanced/decode-live-feed-devices/#capturing-and-previewing-frames-from-a-webcam-using-custom-demuxer)
    - [Capturing and Previewing frames from your Desktop](../advanced/decode-live-feed-devices/#capturing-and-previewing-frames-from-your-desktop) _(Screen Recording)_
- [x] **[:octicons-cpu-16: Hardware-Accelerated Video Decoding](../advanced/decode-hw-acceleration/#hardware-accelerated-video-decoding)**
    - [CUVID-accelerated Hardware-based Video Decoding and Previewing](../advanced/decode-hw-acceleration/#cuvid-accelerated-hardware-based-video-decoding-and-previewing)
    - [CUDA-accelerated Hardware-based Video Decoding and Previewing](../advanced/decode-hw-acceleration/#cuda-accelerated-hardware-based-video-decoding-and-previewing)

<div class="spacer"></div>

## Advanced :material-movie-edit: Transcoding Recipes

- [x] **[:fontawesome-solid-wand-magic-sparkles: Transcoding Live Complex Filtergraphs](../advanced/transcode-live-frames-complexgraphs/#transcoding-live-complex-filtergraphs)**
    - [Transcoding video with Live Custom watermark image overlay](../advanced/transcode-live-frames-complexgraphs/#transcoding-video-with-live-custom-watermark-image-overlay)
    - [Transcoding video from sequence of Images with additional filtering](../advanced/transcode-live-frames-complexgraphs/#transcoding-video-from-sequence-of-images-with-additional-filtering)
- [x] **[:fontawesome-solid-paintbrush: Transcoding Video Art with Filtergraphs](../advanced/transcode-art-filtergraphs/#transcoding-video-art-with-filtergraphs)**
    - [Transcoding video art with YUV Bitplane Visualization](../advanced/transcode-art-filtergraphs/#transcoding-video-art-with-yuv-bitplane-visualization)
    - [Transcoding video art with Jetcolor effect](../advanced/transcode-art-filtergraphs/#transcoding-video-art-with-jetcolor-effect) 
    - [Transcoding video art with Ghosting effect](../advanced/transcode-art-filtergraphs/#transcoding-video-art-with-ghosting-effect)
    - [Transcoding video art with Pixelation effect](../advanced/transcode-art-filtergraphs/#transcoding-video-art-with-pixelation-effect)
- [x] **[:fontawesome-solid-microchip: Hardware-Accelerated Video Transcoding](../advanced/transcode-hw-acceleration/#hardware-accelerated-video-transcoding)**
    - [CUDA-accelerated Video Transcoding with OpenCV's VideoWriter API](../advanced/transcode-hw-acceleration/#cuda-accelerated-video-transcoding-with-opencvs-videowriter-api)
    - [CUDA-NVENC-accelerated Video Transcoding with WriteGear API](../advanced/transcode-hw-acceleration/#cuda-nvenc-accelerated-video-transcoding-with-writegear-api)
    - [CUDA-NVENC-accelerated End-to-end Lossless Video Transcoding with WriteGear API](../advanced/transcode-hw-acceleration/#cuda-nvenc-accelerated-end-to-end-lossless-video-transcoding-with-writegear-api)

<div class="spacer"></div>

## Advanced :material-movie-search: Metadata Recipes

- [x] **[:material-cog-refresh: Updating Video Metadata](../advanced/update-metadata/#updating-video-metadata)**
    - [Added new attributes to metadata in FFdecoder API](../advanced/update-metadata/#added-new-attributes-to-metadata-in-ffdecoder-api)
    - [Overriding source video metadata in FFdecoder API](../advanced/update-metadata/#overriding-source-video-metadata-in-ffdecoder-api)


&thinsp;


<!--
External URLs
-->
[gitter]: https://gitter.im/deffcode-python/community
[ffmpeg]:https://www.ffmpeg.org/