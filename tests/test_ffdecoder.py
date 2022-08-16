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
from deffcode.utils import logger_handler

# define test logger
logger = logging.getLogger("Test_FFdecoder")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize(
    "source, custom_ffmpeg, output",
    [
        (return_testvideo_path(fmt="av"), return_static_ffmpeg(), True),
        (
            "https://raw.githubusercontent.com/abhiTronix/Imbakup/master/Images/starship.mkv",
            "",
            True,
        ),
        ("unknown://invalid.com/", "", False),
        (return_testvideo_path(fmt="ao"), return_static_ffmpeg(), False),
        (
            return_generated_frames_path(return_static_ffmpeg()),
            return_static_ffmpeg(),
            True,
        ),
    ],
)
def test_source_playback(source, custom_ffmpeg, output):
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
                custom_ffmpeg=custom_ffmpeg,
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
                custom_ffmpeg=custom_ffmpeg,
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
    "pixfmts", ["bgr24", "gray", "rgba", "invalid", "invalid2", "yuv444p", "bgr48be"]
)
def test_frame_format(pixfmts):
    """
    Testing `frame_format` with different pixel formats.
    """
    decoder = None
    frame_num = 0
    source = return_testvideo_path(fmt="vo")
    actual_frame_num, actual_frame_shape = actual_frame_count_n_frame_size(source)
    ffparams = {"-pix_fmt": "bgr24"}
    try:
        # formulate the decoder with suitable source(for e.g. foo.mp4)
        if pixfmts != "invalid2":
            decoder = FFdecoder(
                source,
                frame_format=pixfmts,
                custom_ffmpeg=return_static_ffmpeg(),
                **ffparams,
            ).formulate()
        else:
            decoder = FFdecoder(
                source,
                custom_ffmpeg=return_static_ffmpeg(),
                **ffparams,
            )
            # assign manually pix-format via `metadata` property object {special case}
            decoder.metadata = dict(output_frames_pixfmt="yuvj422p")
            # formulate decoder
            decoder.formulate()

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
    "custom_params, checks",
    [
        (
            {
                "source": "Custom_Value",  # source cannot be altered
                "mytuple": (  # Python's `json` module converts Python tuples to JSON lists
                    1,
                    "John",
                    ("inner_tuple"),
                ),
                "output_frames_pixfmt": 1234,  # invalid pixformat
                "source_video_resolution": [640],  # invalid resolution
            },
            False,
        ),
        (
            {"output_frames_pixfmt": "invalid"},
            False,
        ),
        (["invalid"], False),
        (
            dict(
                mystring="abcd",  # string data
                myint=1234,  # integers data
                mylist=[1, "Rohan", ["inner_list"]],  # list data
                mydict={"anotherstring": "hello"},  # dictionary data
                myjson=json.loads(
                    '{"name": "John", "age": 30, "city": "New York"}'
                ),  # json data
                source_video_resolution=[640, 480],
            ),
            True,
        ),
    ],
)
def test_metadata(custom_params, checks):
    """
    Testing `metadata` print and updation
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    try:
        # custom vars
        ffparams = {"-framerate": None} if not checks else {}
        # formulate the decoder with suitable source(for e.g. foo.mp4)
        decoder = FFdecoder(
            source, custom_ffmpeg=return_static_ffmpeg(), verbose=True, **ffparams
        ).formulate()
        # re-test
        decoder.formulate()

        # print metadata as `json.dump`
        logger.debug(decoder.metadata)

        # change metadata
        decoder.metadata = custom_params

        # print metadata as `json.dump`
        logger.debug(decoder.metadata)

        if checks:
            assert all(
                json.loads(decoder.metadata)[x] == custom_params[x]
                for x in custom_params
            ), "Test failed"
    except Exception as e:
        if not checks:
            pytest.xfail(str(e))
        else:
            pytest.fail(str(e))
    finally:
        # terminate the decoder
        not (decoder is None) and decoder.terminate()


@pytest.mark.parametrize(
    "ffparams, pixfmts",
    [
        (
            {
                "-ss": "00:00:01.45",
                "-frames:v": 1,
                "-custom_resolution": [640, 480],
                "-passthrough_audio": "invalid",  # just for test
                "-vcodec": "unknown",
            },
            "rgba",
        ),
        (
            {
                "-ss": "00:02.45",
                "-vframes": 1,
                "-custom_resolution": "invalid",
                "-ffprefixes": "invalid",
                "-clones": "invalid",
                "-framerate": "invalid",
                "-vcodec": None,
            },
            "gray",
        ),
    ],
)
def test_seek_n_save(ffparams, pixfmts):
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
            **ffparams,
        ).formulate()

        # grab the RGB24(default) frame from the decoder
        frame = next(decoder.generateFrame(), None)

        # check if frame is None
        if not (frame is None) and pixfmts == "rgba":
            # Convert and save our output
            filename = os.path.abspath(
                os.path.join(
                    *[tempfile.gettempdir(), "temp_write", "filename_rgba.jpeg"]
                )
            )
            im = Image.fromarray(frame)
            im = im.convert("RGB")
            im.save(filename)
        elif not (frame is None) and pixfmts == "gray":
            # Convert and save our output
            filename = os.path.abspath(
                os.path.join(
                    *[tempfile.gettempdir(), "temp_write", "filename_gray.png"]
                )
            )
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
        "testsrc=size=1280x720:rate=30",  # virtual "testsrc" source
        {
            "-ffprefixes": ["-t", "5"],  # playback time of 5 seconds
            "-clones": [
                "-i",
                "https://abhitronix.github.io/deffcode/latest/assets/images/ffmpeg.png",
            ],
            "-filter_complex": "[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=W-w-5:H-h-5:format=auto,format=bgr24",
        },
        True,
    ),
]


@pytest.mark.parametrize("source, ffparams, result", test_data_class)
def test_FFdecoder_params(source, ffparams, result):
    """
    Testing FFdecoder API with different parameters and save output
    """
    decoder = None
    writer = None
    f_name = os.path.join(*[tempfile.gettempdir(), "temp_write", "output_foo.avi"])
    try:
        # initialize and formulate the decode with suitable source
        with FFdecoder(
            source,
            frame_format="bgr24",
            source_demuxer="lavfi"
            if (isinstance(source, str) and source.startswith("testsrc"))
            else None,
            **ffparams,
        ) as decoder:

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
        if not (writer is None):
            writer.release()
            remove_file_safe(f_name)


test_data_class = [
    (
        "/dev/video0",
        "v4l2",
        True if platform.system() == "Linux" else False,
    ),  # manual source and demuxer
    (
        0,
        None,
        True if platform.system() == "Linux" else False,
    ),  # +ve index and no demuxer
    (
        "-1",
        "auto",
        True if platform.system() == "Linux" else False,
    ),  # -ve index and "auto" demuxer
    ("5", "auto", False),  # out-of-range index and "auto" demuxer
    ("/dev/video0", "invalid", False),  # manual source and invalid demuxer
]


@pytest.mark.parametrize("source, source_demuxer, result", test_data_class)
def test_camera_capture(source, source_demuxer, result):
    """
    Tests FFdecoder's realtime Webcam and Virtual playback capabilities
    as well as Index based Camera Device Capturing
    """
    decoder = None
    try:
        # initialize and formulate the decode with suitable source
        decoder = FFdecoder(
            source,
            source_demuxer=source_demuxer,
            frame_format="bgr24",
            verbose=True,
        ).formulate()
        # capture 10 camera frames
        for i in range(10):
            # grab the bgr24 frame from the decoder
            frame_recv = next(decoder.generateFrame(), None)
            # check if frame is None
            if frame_recv is None:
                raise AssertionError("Test Failed!")
    except Exception as e:
        if result:
            # catch errors
            pytest.fail(str(e))
        else:
            pytest.xfail(str(e))
    finally:
        # terminate
        not (decoder is None) and decoder.terminate()
