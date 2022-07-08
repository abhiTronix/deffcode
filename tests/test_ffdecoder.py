"""
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
"""
# import the necessary packages

import os
import cv2
import json
import pytest
import tempfile
import platform
import numpy as np
import logging
from .essentials import (
    return_static_ffmpeg,
    return_testvideo_path,
    return_generated_frames_path,
    actual_frame_count_n_frame_size,
    remove_file_safe,
)
from PIL import Image
from deffcode import FFdecoder
from vidgear.gears import WriteGear
from deffcode.utils import logger_handler

# define test logger
logger = logging.getLogger("Test_FFdecoder")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


def array_data(self, size, frame_num=10):
    """
    Generate 10 numpy frames with random pixels
    """
    np.random.seed(0)
    random_data = np.random.random(size=(frame_num, size[0], size[1], 3)) * 255
    return random_data.astype(np.uint8)


@pytest.mark.parametrize(
    "source, output",
    [
        (return_testvideo_path(fmt="av"), True),
        (
            "https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/starship.mkv",
            True,
        ),
        ("unknown://invalid.com/", False),
        (return_testvideo_path(fmt="ao"), False),
        (
            return_generated_frames_path(return_static_ffmpeg()),
            True,
        ),
    ],
)
def test_source_playback(source, output):
    """
    Paths Source Playback - Test playback of various source paths/urls supported by FFdecoder API
    """
    decoder = None
    frame_num = 0
    try:
        # formulate the decoder with suitable source(for e.g. foo.mp4)
        if source == return_testvideo_path(fmt="av"):
            # get instance
            instance = FFdecoder(
                source,
                frame_format="bgr24",
                custom_ffmpeg=return_static_ffmpeg(),
                verbose=True,
            )
            # force unknown number of frames(like camera) {special case}
            instance.metadata = {"approx_video_nframes": 0}
            # formulate decoder
            decoder = instance.formulate()
        else:
            # formulate decoder
            decoder = FFdecoder(
                source,
                frame_format="bgr24",
                custom_ffmpeg=return_static_ffmpeg(),
                verbose=True,
            ).formulate()

        # gather data
        actual_frame_num, actual_frame_shape = actual_frame_count_n_frame_size(source)

        # grab RGB24(default) 3D frames from decoder
        for frame in decoder.generateFrame():
            # check shape
            if frame.shape != actual_frame_shape:
                raise RuntimeError("Test failed")
            # increment number of frames
            frame_num += 1

        assert frame_num >= actual_frame_num, "Test failed"
    except Exception as e:
        if not output:
            logger.exception(str(e))
            pytest.xfail("Test Passed!")
        else:
            pytest.fail(str(e))
    finally:
        # terminate the decoder
        not (decoder is None) and decoder.terminate()


@pytest.mark.parametrize(
    "pixfmts", ["bgr24", "gray", "rgba", "invalid", "yuvj422p", "yuv444p", "bgr48be"]
)
def test_frame_format(pixfmts):
    """
    Testing `frame_format` with different pixel formats.
    """
    decoder = None
    frame_num = 0
    source = return_testvideo_path(fmt="vo")
    actual_frame_num, actual_frame_shape = actual_frame_count_n_frame_size(source)
    extraparams = {"-pix_fmt": "bgr24"}
    try:
        # formulate the decoder with suitable source(for e.g. foo.mp4)
        decoder = FFdecoder(
            source,
            frame_format=pixfmts,
            custom_ffmpeg=return_static_ffmpeg(),
            **extraparams,
        ).formulate()

        # grab RGB24(default) 3D frames from decoder
        for frame in decoder.generateFrame():
            # lets print its shape
            print(frame.shape)
            break

    except Exception as e:
        pytest.fail(str(e))
    finally:
        # terminate the decoder
        not (decoder is None) and decoder.terminate()


@pytest.mark.parametrize(
    "custom_params", [{"source_has_video": "Custom_Value"}, ["invalid"], {"foo": 1234}]
)
def test_metadata(custom_params):
    """
    Testing `metadata` print and updation
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    try:
        # formulate the decoder with suitable source(for e.g. foo.mp4)
        decoder = FFdecoder(
            source,
            custom_ffmpeg=return_static_ffmpeg(),
            verbose=True,
        ).formulate()
        # re-test
        decoder.formulate()

        # print metadata as `json.dump`
        logger.debug(decoder.metadata)

        # change metadata
        decoder.metadata = custom_params

        # print metadata as `json.dump`
        logger.debug(decoder.metadata)

        assert all(
            json.loads(decoder.metadata)[x] == custom_params[x] for x in custom_params
        ), "Test failed"
    except Exception as e:
        if custom_params == ["invalid"]:
            pytest.xfail(str(e))
        else:
            pytest.fail(str(e))
    finally:
        # terminate the decoder
        not (decoder is None) and decoder.terminate()


@pytest.mark.parametrize(
    "extraparams, pixfmts",
    [
        ({"-ss": "00:00:01.45", "-frames:v": 1}, "rgba"),
        ({"-ss": "00:02.45", "-vframes": 1}, "gray"),
    ],
)
def test_seek_n_save(extraparams, pixfmts):
    """
    Testing `frame_format` with different colorspaces.
    """
    decoder = None
    filename = ""
    try:
        # formulate the decoder with suitable source(for e.g. foo.mp4)
        decoder = FFdecoder(
            return_testvideo_path(fmt="vo"),
            frame_format=pixfmts,
            custom_ffmpeg=return_static_ffmpeg(),
            verbose=True,
            **extraparams,
        ).formulate()

        # grab the RGB24(default) frame from the decoder
        frame = next(decoder.generateFrame(), None)

        # check if frame is None
        if not (frame is None) and pixfmts == "rgba":
            # Convert and save our output
            filename = os.path.abspath("filename_rgba.jpeg")
            im = Image.fromarray(frame)
            im = im.convert("RGB")
            im.save(filename)
        elif not (frame is None) and pixfmts == "gray":
            # Convert and save our output
            filename = os.path.abspath("filename_gray.png")
            cv2.imwrite(filename, frame)
        else:
            raise AssertionError("Test Failed!")
        if filename:
            assert os.path.isfile(filename), "Test Failed!"
    except Exception as e:
        pytest.fail(str(e))
    finally:
        # terminate the decoder
        not (decoder is None) and decoder.terminate()
        filename and remove_file_safe(filename)


test_data_class = [
    (return_testvideo_path(), {"-c:v": "hevc"}, False),
    (
        return_generated_frames_path(return_static_ffmpeg()),
        {"-s": "data", "-vcodec": None},
        True,
    ),
    (
        return_testvideo_path(),
        {"-vcodec": "h264", "-vf": "rotate=angle=-20*PI/180:fillcolor=brown"},
        True,
    ),
    (
        return_testvideo_path(),
        {
            "-clones": [
                "-i",
                "https://abhitronix.github.io/deffcode/latest/assets/images/ffmpeg.png",
            ],
            "-filter_complex": "[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=W-w-5:H-h-5:format=auto,format=bgr24",
        },
        True,
    ),
]


@pytest.mark.parametrize("source, extraparams, result", test_data_class)
def test_FFdecoder_params(source, extraparams, result):
    """
    Testing FFdecoder API with different parameters and save output
    """
    decoder = None
    writer = None
    f_name = os.path.join(*[tempfile.gettempdir(), "temp_write", "output_foo.avi"])
    try:
        # initialize and formulate the decode with suitable source
        decoder = FFdecoder(source, frame_format="bgr24", **extraparams).formulate()

        # retrieve JSON Metadata and convert it to dict
        metadata_dict = json.loads(decoder.metadata)

        # prepare OpenCV parameters
        FOURCC = cv2.VideoWriter_fourcc("M", "J", "P", "G")
        FRAMERATE = metadata_dict["source_video_framerate"]
        FRAMESIZE = tuple(metadata_dict["source_video_resolution"])

        # Define writer with parameters and suitable output filename for e.g. `output_foo.avi`
        writer = cv2.VideoWriter(f_name, FOURCC, FRAMERATE, FRAMESIZE)

        # grab the BGR24 frame from the decoder
        for frame in decoder.generateFrame():

            # check if frame is None
            if frame is None:
                break

            # writing BGR24 frame to writer
            writer.write(frame)
    except Exception as e:
        if result:
            pytest.fail(str(e))
        else:
            pytest.xfail(str(e))
    finally:
        # terminate the decoder
        not (decoder is None) and decoder.terminate()
        not (writer is None) and writer.release() and remove_file_safe(f_name)


@pytest.mark.skipif(
    (platform.system() != "Linux"), reason="Tests on other platforms not supported yet!"
)
def test_cameradevice():
    """
    Tests FFdecoder's webcam playback capabilities
    """
    try:
        # Define writer with default parameters and suitable output filename for e.g. `Output.mp4`
        logger.debug("Creating v4l2loopback source")
        output_params = {"-f": "v4l2"}
        writer = WriteGear(output_filename="/dev/video0", logging=True, **output_params)

        # initialize and formulate the decode with suitable source
        logger.debug("Creating FFdecoder sink")
        decoder = FFdecoder(
            cam.device, source_demuxer="v4l2", frame_format="bgr24", verbose=True
        ).formulate()

        # create fake frame
        frames_data = array_data(size=(1280, 720))

        # send and capture frames
        for frame_sent in frames_data:
            # send and capture frames
            writer.write(frame_sent)

            # grab the bgr24 frame from the decoder
            frame_recv = next(decoder.generateFrame(), None)

            # check if frame is None
            if frame_recv is None:
                raise AssertionError("Test Failed!")
    except Exception as e:
        pytest.fail(str(e))
