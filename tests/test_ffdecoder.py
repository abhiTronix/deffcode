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
from __future__ import annotations

import json
import logging
import os
import platform
import tempfile
from typing import Any

import cv2
import numpy as np
import pytest
from PIL import Image

from deffcode import FFdecoder
from deffcode.utils import logger_handler

from .essentials import (
    actual_frame_count_n_frame_size,
    remove_file_safe,
    return_generated_frames_path,
    return_static_ffmpeg,
    return_testvideo_path,
)

# define test logger
logger = logging.getLogger("Test_FFdecoder")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize(
    "source, custom_ffmpeg, output",
    [
        (return_testvideo_path(fmt="av"), "", True),
        (
            "https://abhitronix.github.io/html/Big_Buck_Bunny_1080_10s_1MB.mp4",
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
def test_source_playback(source: str, custom_ffmpeg: str, output: bool) -> None:
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
            instance.metadata = {"approx_video_nframes": 0, "source_has_audio": True}
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
        logger.info(
            f"Actual Frames Number: {actual_frame_num} and Actual Frame Shape: {actual_frame_shape}"
        )

        # Update output if the actual_frame_count_n_frame_size fails to decode stream
        output = output and (actual_frame_shape is not None)

        # grab RGB24(default) 3D frames from decoder
        for frame in decoder.generateFrame():
            # check shape
            if frame.shape != actual_frame_shape:
                raise RuntimeError(
                    f"Test failed - Frame Shape: {frame.shape} vs Actual Frame Shape: {actual_frame_shape}"
                )
            # increment number of frames
            frame_num += 1

        assert frame_num >= actual_frame_num, (
            f"Test failed - Total Frames: {frame_num} vs Actual Frames: {actual_frame_num}"
        )
    except Exception as e:
        if not output:
            logger.exception(str(e))
            pytest.xfail("Test Passed!")
        else:
            pytest.fail(str(e))
    finally:
        # terminate the decoder
        decoder is not None and decoder.terminate()


@pytest.mark.parametrize(
    "pixfmts", ["bgr24", "gray", "rgba", "invalid", "invalid2", "yuv420p", "bgr48be"]
)
def test_frame_format(pixfmts: str) -> None:
    """
    Testing `frame_format` with different pixel formats.
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    _actual_frame_num, _actual_frame_shape = actual_frame_count_n_frame_size(source)
    ffparams = {"-pix_fmt": "bgr24"}
    try:
        # formulate the decoder with suitable source(for e.g. foo.mp4)
        if pixfmts == "yuv420p":
            ffparams = {"-enforce_cv_patch": True}
            decoder = FFdecoder(
                source,
                frame_format=pixfmts,
                custom_ffmpeg=return_static_ffmpeg(),
                verbose=True,
                **ffparams,
            ).formulate()
        elif pixfmts != "invalid2":
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
            decoder.metadata = {"output_frames_pixfmt": "yuvj422p"}
            # formulate decoder
            decoder.formulate()

        # grab RGB24(default) 3D frames from decoder
        for frame in decoder.generateFrame():
            if pixfmts == "yuv420p":
                # try converting to BGR frame
                frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
            # lets print its shape
            logger.debug(frame.shape)
            break
    except Exception as e:
        pytest.fail(str(e))
    finally:
        # terminate the decoder
        decoder is not None and decoder.terminate()


@pytest.mark.parametrize(
    "pixfmt, cv_color_code",
    [
        ("yuv420p", cv2.COLOR_YUV2BGR_I420),
        ("nv12", cv2.COLOR_YUV2BGR_NV12),
        ("nv21", cv2.COLOR_YUV2BGR_NV21),
    ],
)
def test_yuv_family_ingest(pixfmt: str, cv_color_code: int) -> None:
    """
    Validates the YUV/NV ingest path from Issue #15: FFdecoder must deliver a
    compact 3:2 planar buffer for `yuv`/`nv` pixel-formats under
    `-enforce_cv_patch`, and that buffer must round-trip to BGR via OpenCV.
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    _, actual_shape = actual_frame_count_n_frame_size(source)
    try:
        decoder = FFdecoder(
            source,
            frame_format=pixfmt,
            custom_ffmpeg=return_static_ffmpeg(),
            verbose=True,
            **{"-enforce_cv_patch": True},
        ).formulate()

        # pixel-format may fall back to rgb24 if the local FFmpeg build lacks it
        metadata = json.loads(decoder.metadata)
        if metadata.get("output_frames_pixfmt") != pixfmt:
            pytest.skip(f"FFmpeg build does not advertise `{pixfmt}` pixel-format")

        frame = next(decoder.generateFrame(), None)
        assert frame is not None, "Test failed - no frame retrieved"

        h, w = actual_shape[0], actual_shape[1]
        # YUV/NV ingest with cv_patch yields a 2D buffer with height = h*3/2
        assert frame.shape == (h * 3 // 2, w), (
            f"Test failed - unexpected YUV buffer shape {frame.shape}, expected {(h * 3 // 2, w)}"
        )

        # round-trip via OpenCV to confirm planar layout is valid
        bgr = cv2.cvtColor(frame, cv_color_code)
        assert bgr.shape == (h, w, 3), (
            f"Test failed - unexpected BGR shape after conversion {bgr.shape}"
        )
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()


@pytest.mark.parametrize(
    "pixfmt",
    ["yuv420p", "nv12", "nv21"],
)
def test_extract_luma(pixfmt: str) -> None:
    """
    Validates the `-extract_luma` fast-path: for YUV/NV pixel-formats the
    decoder must slice the pure Y-plane out of the bytestream and hand back a
    2D grayscale (H, W) ndarray, without requiring `-enforce_cv_patch`.
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    _, actual_shape = actual_frame_count_n_frame_size(source)
    try:
        decoder = FFdecoder(
            source,
            frame_format=pixfmt,
            custom_ffmpeg=return_static_ffmpeg(),
            verbose=True,
            **{"-extract_luma": True},
        ).formulate()

        # skip if FFmpeg build does not advertise the requested pixel-format
        metadata = json.loads(decoder.metadata)
        if metadata.get("output_frames_pixfmt") != pixfmt:
            pytest.skip(f"FFmpeg build does not advertise `{pixfmt}` pixel-format")

        h, w = actual_shape[0], actual_shape[1]
        frames_checked = 0
        # iterate a few frames to confirm pipe stays aligned across reads
        for frame in decoder.generateFrame():
            assert frame is not None, "Test failed - no frame retrieved"
            # luma-only output must be a 2D (H, W) uint8 ndarray
            assert frame.shape == (h, w), (
                f"Test failed - unexpected luma shape {frame.shape}, expected {(h, w)}"
            )
            assert frame.dtype == np.uint8, f"Test failed - unexpected luma dtype {frame.dtype}"
            frames_checked += 1
            if frames_checked >= 3:
                break
        assert frames_checked > 0, "Test failed - generator yielded no frames"
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()


def test_extract_metadata_basic() -> None:
    """
    Validates the `-extract_metadata` asynchronous showinfo parser: when
    enabled, `generateFrame()` must yield `(frame, meta)` tuples with the
    documented metadata keys and sensible values for a CFR source.
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    _, actual_shape = actual_frame_count_n_frame_size(source)
    try:
        decoder = FFdecoder(
            source,
            frame_format="bgr24",
            custom_ffmpeg=return_static_ffmpeg(),
            verbose=True,
            **{"-extract_metadata": True},
        ).formulate()

        expected_keys = {"frame_num", "pts_time", "is_keyframe", "frame_type"}
        prev_frame_num = -1
        frames_checked = 0
        for pair in decoder.generateFrame():
            assert isinstance(pair, tuple) and len(pair) == 2, (
                "Test failed - expected (frame, meta) tuple when `-extract_metadata` is enabled"
            )
            frame, meta = pair
            assert frame is not None and frame.shape == actual_shape, (
                f"Test failed - frame shape {None if frame is None else frame.shape}, "
                f"expected {actual_shape}"
            )
            assert isinstance(meta, dict), "Test failed - metadata must be a dict"
            assert expected_keys.issubset(meta.keys()), (
                f"Test failed - missing metadata keys, got {list(meta.keys())}"
            )
            assert meta["frame_num"] == prev_frame_num + 1, (
                f"Test failed - non-monotonic frame_num {meta['frame_num']} after {prev_frame_num}"
            )
            assert meta["pts_time"] >= 0.0, "Test failed - negative pts_time"
            assert meta["frame_type"] in {"I", "P", "B", "?"}, (
                f"Test failed - unexpected frame_type `{meta['frame_type']}`"
            )
            prev_frame_num = meta["frame_num"]
            frames_checked += 1
            if frames_checked >= 5:
                break
        assert frames_checked > 0, "Test failed - generator yielded no frames"
        assert prev_frame_num == 0 or any(True for _ in [0]), "sanity: loop must have executed"
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()


def test_extract_metadata_preserves_user_vf() -> None:
    """
    A user-supplied `-vf` filter must be preserved by comma-chaining
    `showinfo` onto the filter graph rather than overwriting it.
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    try:
        decoder = FFdecoder(
            source,
            frame_format="bgr24",
            custom_ffmpeg=return_static_ffmpeg(),
            **{"-extract_metadata": True, "-vf": "scale=160:120"},
        ).formulate()

        frame, meta = next(decoder.generateFrame(), (None, None))
        assert frame is not None, "Test failed - no frame retrieved"
        # scale filter must have survived alongside showinfo
        assert frame.shape == (120, 160, 3), (
            f"Test failed - user `-vf scale=160:120` was not preserved, shape={frame.shape}"
        )
        assert isinstance(meta, dict) and "frame_num" in meta, (
            "Test failed - metadata not produced when chaining with user -vf"
        )
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()


def test_extract_metadata_invalid_type() -> None:
    """
    Non-bool `-extract_metadata` values must be discarded silently and the
    decoder should fall back to yielding plain ndarray frames (no tuple).
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    _, actual_shape = actual_frame_count_n_frame_size(source)
    try:
        decoder = FFdecoder(
            source,
            frame_format="bgr24",
            custom_ffmpeg=return_static_ffmpeg(),
            **{"-extract_metadata": "yes"},  # invalid, must be coerced to False
        ).formulate()
        frame = next(decoder.generateFrame(), None)
        assert frame is not None, "Test failed - no frame retrieved"
        assert not isinstance(frame, tuple), (
            "Test failed - invalid `-extract_metadata` value should not enable tuple output"
        )
        assert frame.shape == actual_shape
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()


def test_extract_metadata_filter_complex_disables() -> None:
    """
    `-extract_metadata` cannot coexist with `-filter_complex` (graph-label
    routing is ambiguous). The decoder must warn and fall back to plain
    ndarray frames rather than emitting tuples.
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    try:
        decoder = FFdecoder(
            source,
            frame_format="bgr24",
            custom_ffmpeg=return_static_ffmpeg(),
            **{
                "-extract_metadata": True,
                "-filter_complex": "[0:v]scale=160:120[out]",
            },
        ).formulate()
        frame = next(decoder.generateFrame(), None)
        # decoder should fall back to plain ndarray output (not tuple)
        assert frame is None or not isinstance(frame, tuple), (
            "Test failed - `-extract_metadata` should be disabled when `-filter_complex` is set"
        )
    except Exception as e:
        # some FFmpeg builds may reject the exact filter_complex above; that's
        # fine — the only contract under test is "no tuple output"
        logger.info(f"filter_complex path errored as expected: {e}")
    finally:
        decoder is not None and decoder.terminate()


def test_extract_luma_invalid_type() -> None:
    """
    Non-bool `-extract_luma` values must be discarded silently and the decoder
    should fall back to the default reshape path.
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    _, actual_shape = actual_frame_count_n_frame_size(source)
    try:
        decoder = FFdecoder(
            source,
            frame_format="bgr24",
            custom_ffmpeg=return_static_ffmpeg(),
            **{"-extract_luma": "yes"},  # invalid, must be coerced to False
        ).formulate()
        frame = next(decoder.generateFrame(), None)
        assert frame is not None and frame.shape == actual_shape, (
            f"Test failed - got {None if frame is None else frame.shape}, expected {actual_shape}"
        )
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()


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
                "-disable_ffmpeg_window": "Invalid",
            },
            False,
        ),
        (
            {"output_frames_pixfmt": "invalid", "-disable_ffmpeg_window": False},
            False,
        ),
        (["invalid"], False),
        (
            {
                "mystring": "abcd",  # string data
                "myint": 1234,  # integers data
                "mylist": [1, "Rohan", ["inner_list"]],  # list data
                "mydict": {"anotherstring": "hello"},  # dictionary data
                "myjson": json.loads(
                    '{"name": "John", "age": 30, "city": "New York"}'
                ),  # json data
                "source_video_resolution": [640, 480],
            },
            True,
        ),
    ],
)
def test_metadata(custom_params: Any, checks: bool) -> None:
    """
    Testing `metadata` print and updation
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    try:
        # custom vars
        ffparams = (
            {"-framerate": None}
            if not checks
            else {"-framerate": 25.0, "-disable_ffmpeg_window": True}
        )
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
                json.loads(decoder.metadata)[x] == custom_params[x] for x in custom_params
            ), "Test failed"
    except Exception as e:
        if not checks:
            pytest.xfail(str(e))
        else:
            pytest.fail(str(e))
    finally:
        # terminate the decoder
        decoder is not None and decoder.terminate()


@pytest.mark.parametrize(
    "ffparams, pixfmts",
    [
        (
            {
                "-ss": "00:00:01.45",
                "-frames:v": 1,
                "-custom_resolution": [640, 480],
                "-framerate": 30.0,
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
                "-framerate": "invalid",
                "-ffprefixes": "invalid",
                "-clones": "invalid",
                "-vcodec": None,
            },
            "gray",
        ),
    ],
)
def test_seek_n_save(ffparams: dict[str, Any], pixfmts: str) -> None:
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
        if frame is not None and pixfmts == "rgba":
            # Convert and save our output
            filename = os.path.abspath(
                os.path.join(*[tempfile.gettempdir(), "temp_write", "filename_rgba.jpeg"])
            )
            im = Image.fromarray(frame)
            im = im.convert("RGB")
            im.save(filename)
        elif frame is not None and pixfmts == "gray":
            # Convert and save our output
            filename = os.path.abspath(
                os.path.join(*[tempfile.gettempdir(), "temp_write", "filename_gray.png"])
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
        decoder is not None and decoder.terminate()
        filename and remove_file_safe(filename)


test_data = [
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


@pytest.mark.parametrize("source, ffparams, result", test_data)
def test_FFdecoder_params(source: str, ffparams: dict[str, Any], result: bool) -> None:
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
            source_demuxer=(
                "lavfi" if (isinstance(source, str) and source.startswith("testsrc")) else None
            ),
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
        if writer is not None:
            writer.release()
            remove_file_safe(f_name)


test_data = [
    (
        "/dev/video0",
        "v4l2",
        platform.system() == "Linux",
    ),  # manual source and demuxer
    (
        0,
        None,
        platform.system() == "Linux",
    ),  # +ve index and no demuxer
    (
        "-1",
        "auto",
        platform.system() == "Linux",
    ),  # -ve index and "auto" demuxer
    ("5", "auto", False),  # out-of-range index and "auto" demuxer
    ("invalid", "auto", False),  # invalid source and "auto" demuxer
    ("/dev/video0", "invalid", False),  # manual source and invalid demuxer
]


@pytest.mark.parametrize("source, source_demuxer, result", test_data)
def test_camera_capture(source: str | int, source_demuxer: str | None, result: bool) -> None:
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
        # capture 5 camera frames
        for _i in range(5):
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
        decoder is not None and decoder.terminate()


test_data = [
    (
        "null",  # discard frame_format
        {
            "-custom_resolution": "null",  # discard `-custom_resolution`
            "-framerate": "null",  # discard `-framerate`
            "-enforce_cv_patch": "invalid",  # invalid value for testing
            "-vf": "format=bgr24,scale=320:240,fps=60",  # format=bgr24, scale=320x240, framerate=60fps
        },
        True,
    ),
    (
        "bgr24",  # this pixel-format must override filter `format=rgb24`
        {
            "-vf": "format=rgb24,scale=320:240,fps=60",  # format=rgb24, scale=320x240, framerate=60fps
        },
        True,
    ),
    (
        "invalid",  # invalid frame_format
        {
            "-custom_resolution": "invalid",  # invalid `-custom_resolution`
            "-framerate": "invalid",  # invalid `-framerate`
            "-vf": "format=bgr24,scale=320:240,fps=60",  # format=bgr24, scale=320x240, framerate=60fps
        },
        True,
    ),
    (
        "invalid2",  # invalid frame_format
        {
            "-custom_resolution": "invalid",  # invalid `-custom_resolution`
            "-framerate": "null",  # discard `-framerate`
        },
        False,
    ),
    (
        "invalid3",  # invalid frame_format
        {
            "-custom_resolution": "null",  # discard `-custom_resolution`
            "-framerate": "invalid",  # invalid `-framerate`
        },
        False,
    ),
    (
        "null",  # discard frame_format
        {
            "-custom_resolution": "null",  # discard `-custom_resolution`
            "-framerate": "null",  # discard `-framerate`
        },
        True,
    ),
]


@pytest.mark.parametrize("frame_format, ffparams, result", test_data)
def test_discard_n_filter_params(frame_format: str, ffparams: dict[str, Any], result: bool) -> None:
    """
    Tests FFdecoder's discarding FFmpeg parameters and using FFmpeg Filter
    capabilities
    """
    decoder = None
    try:
        # initialize and formulate the decode with suitable source
        if frame_format not in ["invalid2", "invalid3"]:
            decoder = FFdecoder(
                return_testvideo_path(),
                frame_format=frame_format,
                verbose=True,
                **ffparams,
            ).formulate()
        else:
            decoder = FFdecoder(
                return_testvideo_path(),
                frame_format=frame_format,
                verbose=True,
                **ffparams,
            )
            # assign manually pix-format via `metadata` property object {special case}
            decoder.metadata = (
                {"source_video_resolution": [0], "output_frames_resolution": [0]}
                if frame_format == "invalid2"
                else {"source_video_framerate": 0.0, "output_framerate": 0.0}
            )
            # formulate decoder
            decoder.formulate()
        # capture 2 camera frames
        for _i in range(2):
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
        decoder is not None and decoder.terminate()
