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

# Basic Recipes :pie:


!!! warning "Important Information"

    * DeFFcode APIs **MUST** requires FFmpeg executable present in path. Follow these dedicated [Installation Instructions ➶](../../installation/ffmpeg_install/) for its installation.

    * ==All DeFFcode APIs will raise `RuntimeError` if they fails to detect valid FFmpeg executable on your system!==

    * Always use [`terminate()`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.terminate) function at the end with FFdecoder API to avoid undesired behavior.

&thinsp;

## Saving Keyframes as Image

> In Python, there are many libraries available in Python that allow us to store [`ndarray`](https://numpy.org/doc/stable/reference/arrays.ndarray.html#the-n-dimensional-array-ndarray) frames as images. And in combination with DeFFcode's **effortless and precise FFmpeg Frame Seeking** with `-ss` parameter, we can save any frame from a specific part of our input source. 

Here's a example for seeking to `00:00:01.45`_(or 1045msec)_ in time, and get one single frame, thereby saving it as JPEG image with few prominent python libraries.

??? note "Time unit syntax in `-ss` FFmpeg parameter"
    You can use two different time unit formats with `-ss` FFmpeg parameter: 

    - **Sexagesimal(in seconds):** Uses *(HOURS:MM:SS.MILLISECONDS)*, such as in `01:23:45.678`
    - **Fractional:** such as in `02:30.05`, this is interpreted as 2 minutes, 30 seconds, and a half a second, which would be the same as using 150.5 in seconds.

=== "Using Pillow"

    In Pillow, the `fromarray()` function is used to create an image memory from an RGB array. We can then save this image memory to our desired location by providing the required path and the filename as follows:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    from PIL import Image

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec)
    # in time and get one single frame
    extraparams = {"-ss": "00:00:01.45", "-frames:v": 1}

    # initialize and formulate the decode with suitable source
    decoder = FFdecoder("foo.mp4", **extraparams).formulate()

    # grab the RGB24(default) frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not (frame is None):
        # Convert and save our output
        im = Image.fromarray(frame)
        im.save("filename.jpeg")
    else:
        print("Something is wrong")

    # terminate the decoder
    decoder.terminate()
    ```

=== "Using OpenCV"

    In OpenCV, the `imwrite()` function can export only BGR frames as an image file, thereby make sure to use `frame_format="bgr24"` as shown below:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec) 
    # in time and get one single frame
    extraparams = {"-ss": "00:00:01.45", "-frames:v":1}

    # initialize and formulate the decoder for BGR24 outputwith suitable source
    decoder = FFdecoder("foo.mp4", frame_format="bgr24", **extraparams).formulate()

    # grab the BGR24 frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not(frame is None):
        # Save our output
        cv2.imwrite('filename.jpeg', frame)
    else:
        print("Something is wrong")

    # terminate the decoder
    decoder.terminate()
    ```

=== "Using Matplotlib"

    In Matplotlib, the `imsave()` function can save an RGB frames as an image file:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import matplotlib.pyplot as plt

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec) 
    # in time and get one single frame
    extraparams = {"-ss": "00:00:01.45", "-frames:v":1}

    # initialize and formulate the decode with suitable source
    decoder = FFdecoder("foo.mp4", **extraparams).formulate()

    # grab the RGB24(default) frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not(frame is None):
        # Save our output
        plt.imsave('filename.jpeg', frame)
    else:
        print("Something is wrong")

    # terminate the decoder
    decoder.terminate()
    ```

=== "Using imageio"

    In imageio, the `imwrite()` function is used to create an image memory from an RGB array:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import imageio

    # define the FFmpeg parameter to seek to 00:00:01.45(or 1s and 45msec) 
    # in time and get one single frame
    extraparams = {"-ss": "00:00:01.45", "-frames:v":1}

    # initialize and formulate the decode with suitable source
    decoder = FFdecoder("foo.mp4", **extraparams).formulate()

    # grab the RGB24(default) frame from the decoder
    frame = next(decoder.generateFrame(), None)

    # check if frame is None
    if not(frame is None):
        # Save our output
        imageio.imwrite('filename.jpeg', frame)
    else:
        print("Something is wrong")

    # terminate the decoder
    decoder.terminate()
    ```

&nbsp;


## Display frames using OpenCV Library

You can easily use DeFFcode APIs directly with any Video Processing library such OpenCV. 

In following example we're using OpenCV's `imshow()` to display real-time BGR frame from DeFFcode's FFdecoder API.

!!! note "FFdecoder API's `generateFrame()` function can be used both as a Generator and Iterator. But Generator is the recommended way."

??? tip "Use `waitKey(1)` after `imshow()` function"
    While displaying frames with `imshow()` function, it is appropriate to set the time delay in `waitKey()` to 1msec to pause each frame in the video so that the thread is freed up to do the processing we want to do. In rare cases, when the playback needs to be at a certain framerate, we may want the delay to be higher than 1msec.

=== "As a Generator(Recommended)"

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # initialize and formulate the decoder for BGR24 output
    decoder = FFdecoder("foo.mp4", frame_format="bgr24").formulate()

    # grab the RGB24(default) frame from the decoder
    for frame in decoder.generateFrame():

        # check if frame is None
        if frame is None:
            break
        
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

=== "As a Iterator"

    We can also use `generateFrame()` function as Iterator which is more close to OpenCV-Python (Python API for OpenCV) coding syntax:

    ```python
    # import the necessary packages
    from deffcode import FFdecoder
    import cv2

    # initialize and formulate the decoder for BGR24 output
    decoder = FFdecoder("foo.mp4", frame_format="bgr24").formulate()

    # loop over frames
    while True:
        # grab the BGR24 frame from the decoder
        frame = next(decoder.generateFrame(), None)

        # check if frame is None
        if frame is None:
            break
        
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


## Generate Source Video Metadata

FFdecoder using its [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object _(as Pretty JSON(`json.dump`))_, and Sourcer  using its [`retrieve_metadata()`](../../reference/sourcer/#deffcode.sourcer.Sourcer.retrieve_metadata) method _(as Python dictionary)_, both DeFFcode APIs can be used for **Source Metadata Extraction** that extracts metadata out of given media file.  

In this example we will generate all metadata parameters available within `foo.mp4` media file using both APIs.

=== "Using FFdecoder API"

    ```python
    # import the necessary packages
    from deffcode import FFdecoder

    # initialize and formulate the decoder using suitable source
    decoder = FFdecoder("foo.mp4").formulate()

    # print metadata as `json.dump`
    print(decoder.metadata)

    # terminate the decoder
    decoder.terminate()
    ```
    ???+ quote "After running above python code, the resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"
        ```json
        {
          "ffmpeg_binary_path": "C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe",
          "source": "foo.mp4",
          "source_extension": ".mp4",
          "source_video_resolution": [
            1280,
            720
          ],
          "source_video_framerate": 25.0,
          "source_video_pixfmt": "yuv420p",
          "source_video_decoder": "h264",
          "source_duration_sec": 5.31,
          "approx_video_nframes": 133,
          "source_video_bitrate": "1205k",
          "source_audio_bitrate": "384k",
          "source_audio_samplerate": "48000 Hz",
          "source_has_video": true,
          "source_has_audio": true,
          "source_has_image_sequence": false,
          "ffdecoder_operational_mode": "Video-Only"
        }
        ```

=== "Using Sourcer API"

    ```python
    # import the necessary packages
    from deffcode import Sourcer

    # initialize and formulate the decoder using suitable source
    sourcer = Sourcer("foo.mp4").probe_stream()

    # print metadata as `dict`
    print(sourcer.retrieve_metadata())
    ```
    
    ???+ quote "After running above python code, the resultant Terminal Output will look something as following on :fontawesome-brands-windows:Windows machine:"
        ```py
        {'ffmpeg_binary_path': 'C:\\Users\\foo\\AppData\\Local\\Temp\\ffmpeg-static-win64-gpl/bin/ffmpeg.exe', 'source': 'foo.mp4', 'source_extension': '.mp4', 'source_video_resolution': [1280, 720], 'source_video_framerate': 25.0, 'source_video_pixfmt': 'yuv420p', 'source_video_decoder': 'h264', 'source_duration_sec': 5.31, 'approx_video_nframes': 133, 'source_video_bitrate': '1205k', 'source_audio_bitrate': '384k', 'source_audio_samplerate': '48000 Hz', 'source_has_video': True, 'source_has_audio': True, 'source_has_image_sequence': False}
    
        ```

&nbsp;



## Generating Video from frames using OpenCV Library

FFdecoder can work effortlessly with any OpenCV API class or method such as `VideoWriter()` to save the video.

In this example we will generate video from FFdecoder outputted frames using OpenCV Library's [`VideoWriter()`](https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html#ad59c61d8881ba2b2da22cff5487465b5) class which require a valid output filename _(e.g. output.avi)_, a [FourCC](https://www.fourcc.org/fourcc.php) code, output framerate, and lastly input frame-size.

!!! tip "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps Source Metadata as JSON to retrieve source framerate and frame-size."

!!! alert "OpenCV expects only `BGR` format frames in its `write(frame)` function."


```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# initialize and formulate the decoder for BGR24 output
decoder = FFdecoder("input_foo.mp4", frame_format="bgr24").formulate()

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

## Generating Video with Filter Applied

FFdecoder API support almost any [FFmpeg's Video Filter](http://www.ffmpeg.org/ffmpeg-filters.html#Video-Filters) through `-vf` FFmpeg parameter that applies **a single chain of filters** to the to real-time generated frames.

In this example we will apply Video Filter definitions _(like `rotate` and `drawtext`)_ to real-time frames in FFdecoder API through `-vf` FFmpeg parameter, and generate output video using OpenCV Library's `VideoWriter()` class.

!!! warning "This example assumes you're running :fontawesome-brands-windows:Windows machine. If not, then change `fontfile` path in `drawtext` Video Filter definition accordingly." 

!!! info "You can use FFdecoder's [`metadata`](../../reference/ffdecoder/#deffcode.ffdecoder.FFdecoder.metadata) property object that dumps Source Metadata as JSON to retrieve source framerate and frame-size."

!!! alert "OpenCV expects `BGR` format frames in its `write(frame)` function."

```python
# import the necessary packages
from deffcode import FFdecoder
import json, cv2

# define the Video Filter definition like `rotate` and `drawtext` with `-vf` FFmpeg parameter
extraparams = {
    "-vf": ""
    + "rotate=angle=-20*PI/180:fillcolor=brown"  # rotate filter
    + ", "
    + "drawtext=text='Rotated Video':fontfile='c\:\/windows\/fonts\/arial.ttf':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=24:fontcolor=white"  # drawtext filter
}

# initialize and formulate the decoder for BGR24 output with given params
decoder = FFdecoder(
    "input_foo.mp4", frame_format="bgr24", **extraparams
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