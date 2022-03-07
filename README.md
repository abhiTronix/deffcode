<!--
===============================================
deffcode library source-code is deployed under the Apache 2.0 License:

Copyright (c) 2019 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

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

<h1 align="center">
  <i>de</i><b>FF</b><i>code</i>
</h1>
<p align="center">Performant ⚡️ Pythonic FFmpeg Decoder with easy to adapt flexible API 🐍.</p>
<h2 align="center">
</h2>


&nbsp;

**deffcode** is a Performant and Robust FFmpeg Pythonic Wrapper that aimed at decoding any stream that you throw at it. Requiring minimal efforts, deffcode provides an easy-to-adapt flexible API to read a wide range of streams, and can ingest video using any decoder(even hardware ones) into any pixel format ffmpeg supports. It also provides pin-point accurate seeking for extracting only a specific part of your input as required. 

It is cross-platform, runs on Python 3.7+, and is easy to install.

&nbsp;


## Examples

### Basic Example

```python
# import the necessary packages
from deffcode import FFdecoder

# initialize and formulate the decoder
decoder = FFdecoder("foo.mp4").formulate()

# grab the RGB24(default) frame from 
# the decoder(generator)
for frame in decoder.generateFrame():
	print(frame.shape)

# terminate the decoder
decoder.terminate()
```

The output:

```sh
(720, 1280, 3)
(720, 1280, 3)
     ...
     ...
     ...
(720, 1280, 3)
```

### Basic OpenCV Example

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

### Basic PIL Example

```python
# import the necessary packages
from deffcode import FFdecoder
from PIL import Image

# define the FFmpeg parameter to seek 
# to 00:00:01 in time and get one single frame
extraparams = {"-ss": "00:00:01", "-frames:v":1}

# initialize and formulate the decode
decoder = FFdecoder("foo.mp4", **extraparams).formulate()

# grab the RGB24(default) frame from the decoder
frame = next(decoder.generateFrame(), None)

# check if frame is None
if not(frame is None)
    # Convert and Show output window
    im = Image.fromarray(frame)
    im.show()

# terminate the decoder
decoder.terminate()
```

### Basic Matplotlib Example

```python
# import the necessary packages
from deffcode import FFdecoder
import matplotlib.pyplot as plt

# define the FFmpeg parameter to seek 
# to 00:00:02.01 in time and get one single frame
extraparams = {"-ss": "00:00:02.01", "-frames:v":1}

# initialize and formulate the decode for Grayscale output
decoder = FFdecoder("foo.mp4", frame_format="gray", **extraparams).formulate()

# grab single Grayscale frame from the decoder
frame = next(decoder.generateFrame(), None)

# Show output window
plt.imshow(frame, cmap='gray', vmin=0, vmax=255)
plt.show()

# terminate the decoder
decoder.terminate()
```

&nbsp;

## Dependencies

Minimal requirements:
- Python 3.7+
- FFmpeg (See [this](https://abhitronix.github.io/vidgear/latest/gears/writegear/compression/advanced/ffmpeg_install/#ffmpeg-installation-instructions) for its installation)
- NumPy >=1.20.0
- requests
- colorlog
- tqdm

:bulb: These requirements are installed automatically(except FFmpeg).


&nbsp;

## Installation


```sh
# Install latest stable release
pip install -U deffcode
```

**And if you prefer to install deffcode directly from the repository:**

```sh
# Install latest stable release
pip install git+git://github.com/abhiTronix/deffcode@master#egg=deffcode
```

**Or you can also download its wheel (`.whl`) package from our repository's [releases](https://github.com/abhiTronix/deffcode/releases) section, and thereby can be installed as follows:**

```sh
# Install latest stable release
pip install deffcode-0.1.0-py3-none-any.whl
```

&nbsp;

----

<p align="center"><i><b>deffcode</b> is <a href="https://github.com/abhiTronix/deffcode/blob/master/LICENSE.md">Apache 2.0 Licensed</a> code.<br/>Designed & crafted with care.</i></br>⭐️</p>