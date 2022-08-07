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

# :material-movie-filter: Transcoding Live Simple Filtergraphs

??? abstract "What are Simple filtergraphs?"

    Before heading straight into recipes we will talk about Simple filtergraphs: 
    
    > Simple filtergraphs are those filters that have exactly one input and output, both of the same type. 

    They can be processed by simply inserting an additional step between decoding and encoding of video frames:

    ![Simple filtergraphs](../../../assets/images/simplefiltergraphs.png){ loading=lazy }

    Simple filtergraphs are configured with the per-stream `-filter` option _(with `-vf` for video)_. 


> DeFFcode's FFdecoder API handles a single chain of filtergraphs _(through `-vf` FFmpeg parameter)_ to the to real-time frames quite effortlessly. 

We'll discuss the transcoding of live simple filtergraphs in the following recipes:

&thinsp;

!!! warning "DeFFcode APIs requires FFmpeg executable"

    ==DeFFcode APIs **MUST** requires valid FFmpeg executable for all of its core functionality==, and any failure in detection will raise `RuntimeError` immediately. Follow dedicated [FFmpeg Installation doc ➶](../../../installation/ffmpeg_install/) for its installation.

???+ info "Additional Python Dependencies for following recipes"

    Following recipes requires additional python dependencies which can be installed easily as below:

    - [x] **OpenCV:** OpenCV is required for previewing and encoding video frames. You can easily install it directly via [`pip`](https://pypi.org/project/opencv-python/):

        ??? tip "OpenCV installation from source"

            You can also follow online tutorials for building & installing OpenCV on [Windows](https://www.learnopencv.com/install-opencv3-on-windows/), [Linux](https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/), [MacOS](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) and [Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) machines manually from its source. 

            :warning: Make sure not to install both *pip* and *source* version together. Otherwise installation will fail to work!

        ??? info "Other OpenCV binaries"

            OpenCV mainainers also provide additional binaries via pip that contains both main modules and contrib/extra modules [`opencv-contrib-python`](https://pypi.org/project/opencv-contrib-python/), and for server (headless) environments like [`opencv-python-headless`](https://pypi.org/project/opencv-python-headless/) and [`opencv-contrib-python-headless`](https://pypi.org/project/opencv-contrib-python-headless/). You can also install ==any one of them== in similar manner. More information can be found [here](https://github.com/opencv/opencv-python#installation-and-usage).


        ```sh
        pip install opencv-python       
        ```

!!! note "Always use FFdecoder API's [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) method at the end to avoid undesired behavior."

!!! alert "OpenCV's' [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) class lacks the ability to control output quality, bitrate, compression, and other important features which are only available with VidGear's WriteGear API."

&thinsp;


## Transcoding Trimmed and Reversed video

<figure markdown>
  ![Big Buck Bunny Reversed](../../../assets/gifs/bigbuckbunny_reversed.gif)
  <figcaption>Big Buck Bunny Reversed</figcaption>
</figure>


In this example we will take the first 5 seconds of a video clip _(using `trim` filter)_ and reverse it _(by applying `reverse` filter)_, and encode them using OpenCV Library's [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) method in real-time. 

!!! info "OpenCV's `VideoWriter()` class requires a valid Output filename _(e.g. output_foo.avi)_, [FourCC](https://www.fourcc.org/fourcc.php) code, framerate, and resolution as input."

!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate and resolution."

!!! alert "By default, OpenCV expects `BGR` format frames in its `cv2.write()` method."

```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# define the Video Filter definition
# trim 5 sec from end and reverse
ffparams = {
    "-vf": "trim=end=5,reverse" 
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "foo.mp4", frame_format="bgr24", verbose=True, **ffparams
).formulate()

# retrieve JSON Metadata and convert it to dict
metadata_dict = json.loads(decoder.metadata)

# prepare OpenCV parameters
FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
FRAMERATE = metadata_dict["source_video_framerate"]
FRAMESIZE = tuple(metadata_dict["source_video_resolution"])

# Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

# grab the BGR24 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing BGR24 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.release()
```

&nbsp;

## Transcoding Cropped video

<figure markdown>
  ![Big Buck Bunny Cropped](../../../assets/gifs/bigbuckbunny_cropped.gif)
  <figcaption>Big Buck Bunny Cropped</figcaption>
</figure>


In this example we will crop real-time video frames by an area with size 2/3 of the input video _(say `foo.mp4`)_ by applying `crop` filter in FFdecoder API, all while encoding them using OpenCV Library's [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) method in real-time. 

!!! info "OpenCV's `VideoWriter()` class requires a valid Output filename _(e.g. output_foo.avi)_, [FourCC](https://www.fourcc.org/fourcc.php) code, framerate, and resolution as input."

!!! note "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate and resolution."

!!! tip "More complex examples using `crop` filter can be found [here ➶](https://ffmpeg.org/ffmpeg-filters.html#toc-Examples-57) and can be applied similarly."

```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# define the Video Filter definition
# cropped the central input area with size 2/3 of the input video
ffparams = {
    "-vf": "crop=2/3*in_w:2/3*in_h"
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "foo.mp4", frame_format="bgr24", verbose=True, **ffparams
).formulate()

# retrieve JSON Metadata and convert it to dict
metadata_dict = json.loads(decoder.metadata)

# prepare OpenCV parameters
FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
FRAMERATE = metadata_dict["source_video_framerate"]
FRAMESIZE = tuple(metadata_dict["source_video_resolution"])

# Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

# grab the BGR24 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing BGR24 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.release()
```

&nbsp;

## Transcoding Rotated video (with `rotate` filter)

!!! quote "FFmpeg features "Rotate" Filter that is used to rotate videos by an arbitrary angle (expressed in radians)."

<figure markdown>
  ![Big Buck Bunny Rotated](../../../assets/gifs/bigbuckbunny_rotate.gif)
  <figcaption>Big Buck Bunny Rotated (with <code>rotate</code> filter)</figcaption>
</figure>


In this example we will rotate real-time video frames at an arbitrary angle by applying `rotate` filter in FFdecoder API and also using green color to fill the output area not covered by the rotated image, all while encoding them using OpenCV Library's [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) method in real-time. 

!!! info "OpenCV's `VideoWriter()` class requires a valid Output filename _(e.g. output_foo.avi)_, [FourCC](https://www.fourcc.org/fourcc.php) code, framerate, and resolution as input."

!!! note "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate and resolution."

```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# define the Video Filter definition
# rotate by 0.35 rad and fill green
ffparams = {
    "-vf": "rotate=angle=-20*PI/180:fillcolor=green" 
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "foo.mp4", frame_format="bgr24", verbose=True, **ffparams
).formulate()

# retrieve JSON Metadata and convert it to dict
metadata_dict = json.loads(decoder.metadata)

# prepare OpenCV parameters
FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
FRAMERATE = metadata_dict["source_video_framerate"]
FRAMESIZE = tuple(metadata_dict["source_video_resolution"])

# Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

# grab the BGR24 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing BGR24 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.release()
```

&nbsp;

## Transcoding Rotated video (with `transpose` filter) 

!!! quote "FFmpeg also features "Transpose" Filter that is used to rotate videos by 90 degrees clockwise and counter-clockwise direction as well as flip them vertically and horizontally."

<figure markdown>
  ![Big Buck Bunny Rotated](../../../assets/gifs/bigbuckbunny_transpose.gif)
  <figcaption>Big Buck Bunny Rotated (with <code>transpose</code> filter)</figcaption>
</figure>

In this example we will rotate real-time video frames by 90 degrees counterclockwise and preserve portrait geometry by applying `transfom` filter in FFdecoder API, all while encoding them using OpenCV Library's [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) method in real-time. 

!!! info "OpenCV's `VideoWriter()` class requires a valid Output filename _(e.g. output_foo.avi)_, [FourCC](https://www.fourcc.org/fourcc.php) code, framerate, and resolution as input."

!!! note "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate and resolution."

```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# define the Video Filter definition
# rotate by 90 degrees counter-clockwise and preserve portrait layout
ffparams = {
    "-vf": "transpose=dir=2:passthrough=portrait"
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "foo.mp4", frame_format="bgr24", verbose=True, **ffparams
).formulate()

# retrieve JSON Metadata and convert it to dict
metadata_dict = json.loads(decoder.metadata)

# prepare OpenCV parameters
FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
FRAMERATE = metadata_dict["source_video_framerate"]
FRAMESIZE = tuple(metadata_dict["source_video_resolution"])

# Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

# grab the BGR24 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing BGR24 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.release()
```

&nbsp;

## Transcoding Horizontally flipped and Scaled video

<figure markdown>
  ![Big Buck Bunny Horizontally flipped and Scaled](../../../assets/gifs/bigbuckbunny_hflip_scaled.gif)
  <figcaption>Big Buck Bunny Horizontally flipped and Scaled</figcaption>
</figure>

In this example we will horizontally flip and scale real-time video frames to half its original size by applying `hflip` and `scale` filter one-by-one in FFdecoder API, all while encoding them using OpenCV Library's [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) method in real-time. 

!!! info "OpenCV's `VideoWriter()` class requires a valid Output filename _(e.g. output_foo.avi)_, [FourCC](https://www.fourcc.org/fourcc.php) code, framerate, and resolution as input."

!!! note "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps source Video's metadata information _(as JSON string)_ to retrieve source framerate and resolution."

!!! tip "More complex examples using `scale` filter can be found [here ➶](https://ffmpeg.org/ffmpeg-filters.html#toc-Examples-107) and can be applied similarly."

```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# define the Video Filter definition
# horizontally flip and scale to half its original size
ffparams = {
    "-vf": "hflip,scale=w=iw/2:h=ih/2"
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "foo.mp4", frame_format="bgr24", verbose=True, **ffparams
).formulate()

# retrieve JSON Metadata and convert it to dict
metadata_dict = json.loads(decoder.metadata)

# prepare OpenCV parameters
FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
FRAMERATE = metadata_dict["source_video_framerate"]
FRAMESIZE = tuple(metadata_dict["source_video_resolution"])

# Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
writer = cv2.VideoWriter("output_foo.avi", FOURCC, FRAMERATE, FRAMESIZE)

# grab the BGR24 frame from the decoder
for frame in decoder.generateFrame():

    # check if frame is None
    if frame is None:
        break

    # {do something with the frame here}

    # writing BGR24 frame to writer
    writer.write(frame)

# terminate the decoder
decoder.terminate()

# safely close writer
writer.release()
```

&nbsp;