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
import pytest
import shutil
import logging
import requests
import tempfile
from .essentials import (
    is_windows,
    return_static_ffmpeg,
    return_testvideo_path,
    return_generated_frames_path,
)
from deffcode.utils import logger_handler
from deffcode.ffhelper import (
    get_valid_ffmpeg_path,
    download_ffmpeg_binaries,
    validate_ffmpeg,
    validate_imgseqdir,
    is_valid_image_seq,
    is_valid_url,
    check_sp_output,
    extract_device_n_demuxer,
)

# define test logger
logger = logging.getLogger("Test_ffhelper")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


test_data = [
    (
        os.path.join(tempfile.gettempdir(), "temp_ffmpeg"),
        "win32" if is_windows else "",
    ),
    (
        os.path.join(tempfile.gettempdir(), "temp_ffmpeg"),
        "win64" if is_windows else "",
    ),
    ("wrong_test_path", "wrong_bit"),
]


@pytest.mark.parametrize("paths, os_bit", test_data)
def test_ffmpeg_binaries_download(paths, os_bit):
    """
    Testing Static FFmpeg auto-download on Windows OS
    """
    file_path = ""
    try:
        file_path = download_ffmpeg_binaries(
            path=paths, os_windows=is_windows, os_bit=os_bit
        )
        if file_path:
            logger.debug("FFmpeg Binary path: {}".format(file_path))
            assert os.path.isfile(file_path), "FFmpeg download failed!"
            shutil.rmtree(os.path.abspath(os.path.join(file_path, "../..")))
    except Exception as e:
        if paths == "wrong_test_path" or os_bit == "wrong_bit":
            pass
        else:
            pytest.fail(str(e))


@pytest.mark.parametrize("paths", ["wrong_test_path", return_static_ffmpeg()])
def test_validate_ffmpeg(paths):
    """
    Testing downloaded FFmpeg Static binaries validation on Windows OS
    """
    try:
        output = validate_ffmpeg(paths, verbose=True)
        if paths != "wrong_test_path":
            assert bool(output), "Validation Test failed at path: {}".format(paths)
    except Exception as e:
        if paths == "wrong_test_path":
            pass
        else:
            pytest.fail(str(e))


test_data = [
    ("", "", True),
    ("wrong_test_path", "", False),
    ("", "wrong_test_path", False),
    ("", os.path.join(tempfile.gettempdir(), "temp_ffmpeg"), True),
    (return_static_ffmpeg(), "", True),
    (os.path.dirname(return_static_ffmpeg()), "", True),
]


@pytest.mark.parametrize("paths, ffmpeg_download_paths, results", test_data)
def test_get_valid_ffmpeg_path(paths, ffmpeg_download_paths, results):
    """
    Testing FFmpeg excutables validation and correction:
    """
    try:
        output = get_valid_ffmpeg_path(
            custom_ffmpeg=paths,
            is_windows=is_windows,
            ffmpeg_download_path=ffmpeg_download_paths,
            verbose=True,
        )
        if not (
            paths == "wrong_test_path" or ffmpeg_download_paths == "wrong_test_path"
        ):
            assert (
                bool(output) == results
            ), "FFmpeg excutables validation and correction Test failed at path: {} and FFmpeg ffmpeg_download_paths: {}".format(
                paths, ffmpeg_download_paths
            )
    except Exception as e:
        if paths == "wrong_test_path" or ffmpeg_download_paths == "wrong_test_path":
            pass
        elif isinstance(e, requests.exceptions.Timeout):
            logger.exceptions(str(e))
        else:
            pytest.fail(str(e))


@pytest.mark.xfail(raises=Exception)
def test_check_sp_output():
    """
    Testing check_sp_output method
    """
    check_sp_output(["ffmpeg", "-Vv"])


@pytest.mark.parametrize(
    "URL, result",
    [
        ("rtmp://live.twitch.tv/", True),
        (None, False),
        ("unknown://invalid.com/", False),
    ],
)
def test_is_valid_url(URL, result):
    """
    Testing is_valid_url method
    """
    try:
        result_url = is_valid_url(return_static_ffmpeg(), url=URL, verbose=True)
        assert result_url == result, "URL validity test Failed!"
    except Exception as e:
        pytest.fail(str(e))


@pytest.mark.parametrize(
    "source, result",
    [
        (return_generated_frames_path(return_static_ffmpeg()), True),
        (None, False),
        (return_testvideo_path(), False),
        (
            "{}/Downloads/Test_videos/{}".format(tempfile.gettempdir(), "invalid.png"),
            False,
        ),
    ],
)
def test_is_valid_image_seq(source, result):
    """
    Testing test_is_valid_image_seq method
    """
    try:
        result_url = is_valid_image_seq(
            return_static_ffmpeg(), source=source, verbose=True
        )
        assert result_url == result, "Image sequence validity test Failed!"
    except Exception as e:
        result and pytest.fail(str(e))


@pytest.mark.parametrize(
    "path, result",
    [
        (return_generated_frames_path(return_static_ffmpeg()), True),
        ("unknown://invalid.com/", False),
    ],
)
def test_validate_imgseqdir(path, result):
    """
    Testing validate_imgseqdir method
    """
    try:
        output = validate_imgseqdir(path, extension="png", verbose=True)
        assert output == result, "Image sequence directory validity test Failed!"
    except Exception as e:
        result and pytest.fail(str(e))


@pytest.mark.xfail(raises=ValueError)
def test_extract_device_n_demuxer():
    """
    Testing extract_device_n_demuxer method
    """
    extract_device_n_demuxer(return_static_ffmpeg(), machine_OS="invalid", verbose=True)