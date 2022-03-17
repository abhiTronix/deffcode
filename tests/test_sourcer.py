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

import pytest
import logging
from .essentials import (
    return_static_ffmpeg,
    return_testvideo_path,
    return_generated_frames_path,
    actual_frame_count_n_frame_size,
)
from deffcode.utils import logger_handler
from deffcode import Sourcer

# define test logger
logger = logging.getLogger("Test_Sourcer")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize(
    "source, sourcer_params",
    [
        (return_testvideo_path(), {}),
        (
            "rtmp://live.twitch.tv/",
            {"-ffmpeg_download_path": ["invalid"]},
        ),
        ("unknown://invalid.com/", {}),
        ("unknown://invalid.com/", {"-force_validate_source": True}),
        (return_testvideo_path(fmt="ao"), {"-force_validate_source": ["invalid"]}),
        (
            return_generated_frames_path(return_static_ffmpeg()),
            {"-force_validate_source": "invalid"},
        ),
    ],
)
def test_source(source, sourcer_params):
    """
    Paths Source - Test various source paths/urls supported by Sourcer.
    """
    try:
        sourcer = Sourcer(
            source, custom_ffmpeg=return_static_ffmpeg(), verbose=True, **sourcer_params
        ).probe_stream()
        logger.debug("Found Metadata: `{}`".format(sourcer.retrieve_metadata()))
    except Exception as e:
        if isinstance(e, (ValueError, IOError)):
            pytest.xfail("Test Passed!")
        else:
            pytest.fail(str(e))


@pytest.mark.parametrize(
    "source, default_stream_indexes, params",
    [
        (return_testvideo_path(), [0, 0], ["source_has_video", "source_has_audio"]),
        (return_testvideo_path(fmt="ao"), [3, 2], ["source_has_audio"]),
        (
            "http://devimages.apple.com/iphone/samples/bipbop/bipbopall.m3u8",
            (1, 0),
            ["source_has_video", "source_has_audio"],
        ),
        ("unknown://invalid.com/", (1, "invalid", 0), []),
        ("invalid", (), []),
        (
            return_generated_frames_path(return_static_ffmpeg()),
            (0, 0),
            ["source_has_image_sequence"],
        ),
    ],
)
def test_probe_stream_n_retrieve_metadata(source, default_stream_indexes, params):
    """
    Test `probe_stream` and `retrieve_metadata` function.
    """
    try:
        if source == "invalid":
            sourcer = Sourcer(
                source, custom_ffmpeg=return_static_ffmpeg(), verbose=True
            )
        else:
            sourcer = Sourcer(
                source, custom_ffmpeg=return_static_ffmpeg(), verbose=True
            ).probe_stream(default_stream_indexes=default_stream_indexes)
        metadata = sourcer.retrieve_metadata()
        logger.debug("Found Metadata: `{}`".format(metadata))
        assert all(metadata[x] == True for x in params), "Test Failed!"
        if source.startswith("http") or source.endswith("png"):
            logger.debug("Skipped check!")
        else:
            assert (
                metadata["approx_video_nframes"]
                >= actual_frame_count_n_frame_size(source)[0]
            ), "Test Failed for frames count!"
    except Exception as e:
        if isinstance(e, (ValueError, IOError)) or (
            source in ["invalid", "unknown://invalid.com/"]
            and isinstance(e, AssertionError)
        ):
            pytest.xfail("Test Still Passed!")
        else:
            pytest.fail(str(e))
