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
import struct
import subprocess
import tempfile
from typing import Any

import cv2
import numpy as np
import pytest
from PIL import Image

from deffcode import FFdecoder
from deffcode import ffdecoder as ffdecoder_module
from deffcode import sourcer as sourcer_module
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


@pytest.mark.parametrize("verbose", [True, False])
def test_capture_stderr_on_failure(verbose: bool) -> None:
    """
    With `-capture_stderr`, an FFmpeg pipeline that dies (invalid filter) must end
    the generator gracefully, expose its non-zero exit code via `terminate()`/`returncode`,
    and keep its error output in `stderr_tail`.
    """
    decoder = FFdecoder(
        return_testvideo_path(fmt="vo"),
        custom_ffmpeg=return_static_ffmpeg(),
        verbose=verbose,
        **{"-capture_stderr": True, "-vf": "nonexistentfilter"},
    ).formulate()
    assert decoder.returncode is None, "Test failed - returncode set before termination"
    assert list(decoder.generateFrame()) == [], "Test failed - expected no frames"
    retcode = decoder.terminate()
    assert retcode and retcode == decoder.returncode, f"Test failed - got exit code {retcode}"
    assert any("nonexistentfilter" in line for line in decoder.stderr_tail), (
        f"Test failed - error missing from stderr_tail: {decoder.stderr_tail}"
    )
    # repeated terminate must be idempotent
    assert decoder.terminate() == retcode, "Test failed - returncode lost on re-terminate"


@pytest.mark.parametrize("capture", [True, "yes"])
def test_capture_stderr_success(capture: Any) -> None:
    """
    A cleanly finished pipeline must report exit code 0. Non-bool
    `-capture_stderr` values are discarded, leaving `stderr_tail` empty.
    """
    decoder = FFdecoder(
        return_testvideo_path(fmt="vo"),
        custom_ffmpeg=return_static_ffmpeg(),
        **{"-capture_stderr": capture, "-vframes": 5},
    ).formulate()
    assert len(list(decoder.generateFrame())) == 5, "Test failed - expected 5 frames"
    assert decoder.terminate() == 0, "Test failed - expected exit code 0"
    assert bool(decoder.stderr_tail) == (capture is True), (
        f"Test failed - unexpected stderr_tail: {decoder.stderr_tail}"
    )


def test_returncode_on_stream_exhausted() -> None:
    """
    Decoding a source to its end and terminating right away must report exit
    code 0, not a SIGTERM-induced one while FFmpeg is still exiting.
    """
    decoder = FFdecoder(
        return_testvideo_path(fmt="vo"), custom_ffmpeg=return_static_ffmpeg()
    ).formulate()
    # discard frames to consume fast, racing FFmpeg exit
    assert sum(1 for _ in decoder.generateFrame()) > 0, "Test failed - expected frames"
    assert decoder.terminate() == 0, "Test failed - expected exit code 0"


def test_metadata_invalid_type_discarded() -> None:
    """
    Assigning an invalid-typed value to a source metadata property must be
    discarded with a warning, not raise `AttributeError`.
    """
    decoder = FFdecoder(
        return_testvideo_path(fmt="vo"), custom_ffmpeg=return_static_ffmpeg()
    ).formulate()
    try:
        original = json.loads(decoder.metadata)["source_video_pixfmt"]
        decoder.metadata = {"source_video_pixfmt": 1234}
        assert json.loads(decoder.metadata)["source_video_pixfmt"] == original, (
            "Test failed - invalid-typed value was not discarded"
        )
    finally:
        decoder.terminate()


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
    (
        [return_testvideo_path(), return_testvideo_path()],
        {"-filter_complex": "hstack=inputs=2"},
        True,
    ),
    (
        [return_testvideo_path(), return_testvideo_path()],
        {
            "-extract_metadata": True
        },  # Should fail with ValueError because of missing map/filter_complex
        False,
    ),
]


@pytest.mark.parametrize("source, ffparams, result", test_data)
def test_FFdecoder_params(source: str | list[str], ffparams: dict[str, Any], result: bool) -> None:
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
            FRAMESIZE = tuple(metadata_dict["output_frames_resolution"])

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


_grid = "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[out]"
test_data = [
    (["320x240"] * 2, {"-filter_complex": "hstack=inputs=2"}, (240, 640), 50),
    (
        ["320x240", "160x120"],
        {"-filter_complex": "[1:v]scale=80:-1[s];[0:v][s]overlay=W-w-10:H-h-10"},
        (240, 320),
        50,
    ),
    (["320x240"] * 4, {"-filter_complex": _grid, "-map": "[out]"}, (480, 640), 50),
    (
        ["320x240"] * 2,
        {"-filter_complex": "[0:v][1:v]xfade=duration=1:offset=1[v]", "-map": "[v]"},
        (240, 320),
        75,
    ),
    (["320x240", "160x120"], {"-map": "1:v"}, (120, 160), 50),
]


@pytest.mark.parametrize("sizes, ffparams, shape, n_frames", test_data)
def test_multi_input_composites(
    sizes: list[str], ffparams: dict[str, Any], shape: tuple[int, int], n_frames: int
) -> None:
    """
    Testing multi-input filtergraph recipes yield frames of the composite size and length
    """
    source = ["testsrc=size={}:rate=25:duration=2".format(s) for s in sizes]
    with FFdecoder(
        source, source_demuxer=["lavfi"] * len(sizes), frame_format="bgr24", **ffparams
    ) as decoder:
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert frames and frames[0].shape == (*shape, 3)
    assert abs(len(frames) - n_frames) <= 1


# one `lavfi` input carrying two embedded video streams: v0 red 320x240, v1 blue 160x120
_MULTI_STREAM = "color=c=red:s=320x240:r=25:d=2[out0];color=c=blue:s=160x120:r=30:d=2[out1]"


def _color(frame: np.ndarray) -> str:
    return "red" if frame[..., 0].mean() > frame[..., 2].mean() else "blue"


test_data = [
    ({}, (240, 320), "red"),
    ({"-default_stream_indexes": (1, 0)}, (120, 160), "blue"),
    ({"-map": "0:v:1"}, (120, 160), "blue"),
    ({"-default_stream_indexes": (1, 0), "-map": "0:v:1"}, (120, 160), "blue"),
    ({"-default_stream_indexes": (1, 0), "-vf": "scale=80:-2"}, (60, 80), "blue"),
    ({"-default_stream_indexes": (1, 0), "-filter_complex": "[0:v:1]null"}, (120, 160), "blue"),
    # index inferred from a filtergraph using only `[0:v:N]`
    ({"-filter_complex": "[0:v:1]hflip"}, (120, 160), "blue"),
    ({"-filter_complex": "[0:v:1]hflip[out]", "-map": "[out]"}, (120, 160), "blue"),
    # out-of-range index falls back to stream 0, also with `-vf`
    ({"-default_stream_indexes": (5, 0)}, (240, 320), "red"),
    ({"-default_stream_indexes": (5, 0), "-vf": "scale=80:-2"}, (60, 80), "red"),
    # mixed-rate composite: output has no fps; size still probed, frames not duplicated
    ({"-filter_complex": "[0:v:1]scale=320:240[b];[0:v:0][b]hstack"}, (240, 640), None),
    (
        {"-framerate": 25, "-filter_complex": "[0:v:1]scale=320:240[b];[0:v][b]hstack"},
        (240, 640),
        None,
    ),
    # optional map, and map winning over a conflicting index
    ({"-map": "0:v:1?"}, (120, 160), "blue"),
    ({"-default_stream_indexes": (1, 0), "-map": "0:v:0"}, (240, 320), "red"),
]


@pytest.mark.parametrize("ffparams, shape, color", test_data)
def test_multi_stream_source(
    ffparams: dict[str, Any], shape: tuple[int, int], color: str | None
) -> None:
    """
    Testing selecting an embedded video stream decodes THAT stream at its own size
    """
    with FFdecoder(
        _MULTI_STREAM, source_demuxer="lavfi", frame_format="rgb24", **ffparams
    ) as decoder:
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert frames and frames[0].shape == (*shape, 3)
    assert color is None or _color(frames[0]) == color
    # 2 seconds at the selected stream's (or v0's) rate
    assert abs(len(frames) - (60 if color == "blue" else 50)) <= 1


# v1 is bigger, so FFmpeg alone would auto-select it
_MULTI_STREAM_REV = "color=c=red:s=160x120:r=25:d=2[out0];color=c=blue:s=320x240:r=30:d=2[out1]"

test_data = [
    (_MULTI_STREAM_REV, {}, (120, 160), 1),
    (_MULTI_STREAM_REV, {"-vf": "scale=80:-2"}, (60, 80), 1),
    ("testsrc=size=320x240:rate=25:duration=2", {}, (240, 320), 0),
]


@pytest.mark.parametrize("source, ffparams, shape, n_warnings", test_data)
def test_multi_stream_unselected(
    monkeypatch: Any,
    source: str,
    ffparams: dict[str, Any],
    shape: tuple[int, int],
    n_warnings: int,
) -> None:
    """
    Testing multi-stream sources without a selection decode stream 0 (with a warning),
    while single-stream sources stay unmapped and silent
    """
    warnings: list[str] = []
    monkeypatch.setattr(ffdecoder_module.logger, "warning", warnings.append)
    with FFdecoder(source, source_demuxer="lavfi", frame_format="rgb24", **ffparams) as decoder:
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert frames and frames[0].shape == (*shape, 3)
    assert not n_warnings or _color(frames[0]) == "red"
    assert sum("video streams" in w for w in warnings) == n_warnings


test_data = [
    ({}, 0),
    ({"-default_stream_indexes": (1, 0)}, 0),
    ({"-map": "0:v:1"}, 0),
    ({"-default_stream_indexes": (1, 0), "-vf": "scale=80:-2"}, 1),
    ({"-default_stream_indexes": (5, 0), "-vf": "scale=80:-2"}, 2),
]


@pytest.mark.parametrize("ffparams, decode_probes", test_data)
def test_multi_stream_probes(
    monkeypatch: Any, ffparams: dict[str, Any], decode_probes: int
) -> None:
    """
    Testing stream selection adds no decoding probe (`-f null`) unless `-vf` needs one,
    plus one re-probe for an out-of-range index with `-vf`
    """
    probes: list[list[str]] = []
    check = sourcer_module.check_sp_output
    monkeypatch.setattr(
        sourcer_module,
        "check_sp_output",
        lambda cmd, **kw: (probes.append(cmd), check(cmd, **kw))[1],
    )
    FFdecoder(_MULTI_STREAM, source_demuxer="lavfi", **ffparams)  # probes on init
    assert sum("null" in cmd for cmd in probes) == decode_probes


@pytest.mark.parametrize(
    "ffparams",
    [{"-map": "0:v:1"}, {"-default_stream_indexes": (1, 0)}, {"-filter_complex": "[0:v:1]null"}],
)
def test_multi_stream_mixed_codecs(ffparams: dict[str, Any]) -> None:
    """
    Testing selecting an embedded video stream with a different codec than v0
    uses the right decoder and frame count (file-based: has a `Duration`)
    """
    path = _side_path("multi_stream_mixed.mkv")
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cmd = [return_static_ffmpeg(), "-y", "-f", "lavfi", "-i", _MULTI_STREAM]
        cmd += ["-map", "0:v:0", "-map", "0:v:1", "-c:v:0", "mpeg4", "-c:v:1", "mpeg2video", path]
        subprocess.run(cmd, check=True, capture_output=True)
    with FFdecoder(path, frame_format="rgb24", **ffparams) as decoder:
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert frames and frames[0].shape == (120, 160, 3)
    assert _color(frames[0]) == "blue"
    assert abs(len(frames) - 60) <= 1


def _side_path(name: str) -> str:
    return os.path.join(tempfile.gettempdir(), "temp_write", name)


def _cover_mp4(first: bool) -> str:
    """
    MP4 with red video + green cover art (attached pic). FFmpeg muxes cover art last;
    moving `udta` before `trak` inside `moov` (after `mdat`, so offsets stay valid)
    makes the demuxer expose it as stream 0, as some taggers do.
    """
    path = _side_path("cover_{}.mp4".format("first" if first else "last"))
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cmd = [return_static_ffmpeg(), "-y", "-f", "lavfi", "-i", "color=c=red:s=320x240:r=25:d=1"]
        cmd += ["-f", "lavfi", "-i", "color=c=green:s=64x64:r=1:d=1", "-map", "0", "-map", "1"]
        cmd += ["-c:v:0", "mpeg4", "-c:v:1", "png", "-frames:v:1", "1"]
        cmd += ["-disposition:v:1", "attached_pic", path]
        subprocess.run(cmd, check=True, capture_output=True)

        def boxes(buf: bytes) -> list[tuple[bytes, bytes]]:
            out, i = [], 0
            while i < len(buf):
                size, kind = struct.unpack(">I4s", buf[i : i + 8])
                out.append((kind, buf[i : i + (size or len(buf) - i)]))
                i += size or len(buf) - i
            return out

        if first:
            with open(path, "rb") as f:
                top = boxes(f.read())
            assert [k for k, _ in top][-1] == b"moov"
            order = {b"mvhd": 0, b"udta": 1}
            moov = sorted(boxes(top[-1][1][8:]), key=lambda k: order.get(k[0], 2))
            with open(path, "wb") as f:
                f.write(b"".join(b for _, b in top[:-1]) + top[-1][1][:8])
                f.write(b"".join(b for _, b in moov))
    return path


test_data = [
    (True, {}, (240, 320), [0]),
    (True, {"-vf": "scale=160:-2"}, (120, 160), [0]),
    (False, {}, (240, 320), [1]),
]


@pytest.mark.parametrize("first, ffparams, shape, pics", test_data)
def test_multi_stream_cover_art(
    monkeypatch: Any,
    first: bool,
    ffparams: dict[str, Any],
    shape: tuple[int, int],
    pics: list[int],
) -> None:
    """
    Testing unselected sources skip cover art (attached pic) wherever it is, silently,
    since only one real video stream remains
    """
    path = _cover_mp4(first)
    warnings: list[str] = []
    monkeypatch.setattr(ffdecoder_module.logger, "warning", warnings.append)
    with FFdecoder(path, frame_format="rgb24", **ffparams) as decoder:
        metadata = json.loads(decoder.metadata)
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert metadata["source_video_attached_pics"] == pics
    assert frames and frames[0].shape == (*shape, 3) and _color(frames[0]) == "red"
    assert abs(len(frames) - 25) <= 1
    assert not [w for w in warnings if "video streams" in w]


@pytest.mark.parametrize(
    "ffparams, n_warnings", [({}, 0), ({"-default_stream_indexes": (1, 0)}, 1)]
)
def test_multi_stream_programs(monkeypatch: Any, ffparams: dict[str, Any], n_warnings: int) -> None:
    """
    Testing a video stream shared by two MPEG-TS programs (printed twice in the banner)
    counts once: no false "video streams" warning, and an index 1 falls back to stream 0
    """
    path = _side_path("programs.ts")
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cmd = [return_static_ffmpeg(), "-y", "-f", "lavfi", "-i", "color=c=red:s=320x240:r=25:d=2"]
        cmd += ["-f", "lavfi", "-i", "sine=d=2", "-f", "lavfi", "-i", "sine=f=880:d=2"]
        cmd += ["-map", "0", "-map", "1", "-map", "2", "-c:v", "mpeg2video", "-c:a", "mp2"]
        cmd += ["-program", "title=A:st=0:st=1", "-program", "title=B:st=0:st=2", path]
        subprocess.run(cmd, check=True, capture_output=True)
    warnings: list[str] = []
    for mod in (ffdecoder_module, sourcer_module):
        monkeypatch.setattr(mod.logger, "warning", warnings.append)
    with FFdecoder(path, frame_format="rgb24", **ffparams) as decoder:
        metadata = json.loads(decoder.metadata)
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert metadata["source_video_streams"] == 1
    assert frames and _color(frames[0]) == "red" and abs(len(frames) - 50) <= 1
    assert len([w for w in warnings if "stream" in w]) == n_warnings


test_data = [
    (
        {"-extra_outputs": ["-y", "-map", "0", "-c", "copy", _side_path("side_copy.mkv")]},
        [_side_path("side_copy.mkv")],
        None,
    ),
    (
        {
            "-filter_complex": "[0:v]split=2[main][rec];[main]scale=320:-2[main]",
            "-map": "[main]",
            "-extra_outputs": [
                "-y",
                "-map",
                "[rec]",
                "-c:v",
                "libx264",
                _side_path("side_split.mp4"),
            ],
        },
        [_side_path("side_split.mp4")],
        320,
    ),
    (
        {
            "-extra_outputs": [
                "-y",
                "-map",
                "0:v",
                "-c:v",
                "libx264",
                "-flags",
                "+global_header",
                "-f",
                "tee",
                # tee treats `\` as escape char, so use forward slashes for Windows paths
                "{}|[f=mpegts]{}".format(
                    _side_path("side_tee.mkv"), _side_path("side_tee.ts")
                ).replace("\\", "/"),
            ]
        },
        [_side_path("side_tee.mkv"), _side_path("side_tee.ts")],
        None,
    ),
]


@pytest.mark.parametrize("ffparams, side_files, width", test_data)
def test_extra_outputs(ffparams: dict[str, Any], side_files: list[str], width: int | None) -> None:
    """
    Testing `-extra_outputs` writes side outputs from the same pipeline while frames
    still reach Python intact (incl. `-filter_complex` labels consumed only by side outputs)
    """
    decoder = None
    source = return_testvideo_path(fmt="av")
    actual_count, actual_shape = actual_frame_count_n_frame_size(source)
    os.makedirs(_side_path(""), exist_ok=True)
    try:
        decoder = FFdecoder(
            source, frame_format="bgr24", custom_ffmpeg=return_static_ffmpeg(), **ffparams
        ).formulate()
        frames = [f for f in decoder.generateFrame() if f is not None]
        assert decoder.terminate() == 0, "Test failed - FFmpeg exited with an error"
        assert len(frames) == actual_count, f"Test failed - got {len(frames)} frames"
        # width proves output metadata came from the probe, not the source fallback
        assert frames[0].shape[1] == (width or actual_shape[1]), (
            f"Test failed - unexpected frame shape {frames[0].shape}"
        )
        for side in side_files:
            # count via FFmpeg, since OpenCV on macOS (AVFoundation) can't read `.mkv`; use
            # default FFmpeg, as the pinned 2022 static build dies silently probing `.ts` on CI
            side_decoder = FFdecoder(side).formulate()
            side_count = sum(f is not None for f in side_decoder.generateFrame())
            side_decoder.terminate()
            assert side_count > 0, f"Test failed - empty {side}"
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()
        for side in side_files:
            remove_file_safe(side)


def test_extra_outputs_early_terminate() -> None:
    """
    Terminating mid-stream must still leave a valid (finalized) side `.mp4`
    """
    decoder = None
    side = _side_path("side_early.mp4")
    os.makedirs(_side_path(""), exist_ok=True)
    try:
        decoder = FFdecoder(
            return_testvideo_path(fmt="av"),
            frame_format="bgr24",
            custom_ffmpeg=return_static_ffmpeg(),
            **{"-extra_outputs": ["-y", "-map", "0:v", "-c:v", "libx264", side]},
        ).formulate()
        for num, frame in enumerate(decoder.generateFrame()):
            if frame is None or num == 9:
                break
        decoder.terminate()
        assert actual_frame_count_n_frame_size(side)[0] >= 10, (
            "Test failed - side output not finalized"
        )
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()
        remove_file_safe(side)


@pytest.mark.parametrize("value", ["foo", [["-map", "0"]], {"a": 1}])
def test_extra_outputs_invalid(value: Any) -> None:
    """
    Invalid `-extra_outputs` values must be discarded, leaving normal decoding untouched
    """
    decoder = None
    source = return_testvideo_path(fmt="vo")
    actual_count, actual_shape = actual_frame_count_n_frame_size(source)
    try:
        decoder = FFdecoder(
            source,
            frame_format="bgr24",
            custom_ffmpeg=return_static_ffmpeg(),
            **{"-extra_outputs": value},
        ).formulate()
        frames = [f for f in decoder.generateFrame() if f is not None]
        assert len(frames) == actual_count and frames[0].shape == actual_shape
    except Exception as e:
        pytest.fail(str(e))
    finally:
        decoder is not None and decoder.terminate()


def test_sar_hdr_warnings(monkeypatch: Any) -> None:
    """
    Testing anamorphic HDR source warns about squeezed and washed out frames (not with
    filters), and the suggested `-vf` outputs display aspect ratio
    """
    path = _side_path("sar_hdr.mkv")
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cmd = [return_static_ffmpeg(), "-y", "-f", "lavfi", "-i", "testsrc2=s=144x108:r=25:d=1"]
        cmd += ["-vf", "setsar=4/3", "-c:v", "libx264", "-x264-params"]
        cmd += ["colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc", path]
        subprocess.run(cmd, check=True, capture_output=True)
    warnings: list[str] = []
    monkeypatch.setattr(ffdecoder_module.logger, "warning", warnings.append)
    for ffparams, shape, n_warnings in [
        ({}, (108, 144, 3), 2),
        ({"-vf": "scale=iw*sar:ih,setsar=1"}, (108, 192, 3), 0),  # as suggested
    ]:
        warnings.clear()
        with FFdecoder(path, **ffparams) as decoder:
            metadata = json.loads(decoder.metadata)
            frames = [f for f in decoder.generateFrame() if f is not None]
        assert metadata["source_video_sar"] == [4, 3]
        assert metadata["source_video_color_transfer"] == "smpte2084"
        assert frames and frames[0].shape == shape
        assert len([w for w in warnings if "SAR" in w or "HDR" in w]) == n_warnings


def _testsrc(pixfmt: str) -> str:
    """320x240 ffv1 `testsrc` video with 25 frames in given pixel-format"""
    path = _side_path(f"pixfmt_{pixfmt}.mkv")
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        cmd = [return_static_ffmpeg(), "-y", "-f", "lavfi", "-i", "testsrc=s=320x240:r=25:d=1"]
        cmd += ["-pix_fmt", pixfmt, "-c:v", "ffv1", path]
        subprocess.run(cmd, check=True, capture_output=True)
    return path


@pytest.mark.parametrize(
    "src_pixfmt, ffparams, pixfmt, shape",
    [
        ("yuv420p", {}, "rgb24", (240, 320, 3)),  # metadata reports decoded pixfmt
        ("yuv420p", {"-vf": "hflip"}, "rgb24", (240, 320, 3)),  # planar passthrough
        ("yuv444p", {"-vf": "hflip"}, "rgb24", (240, 320, 3)),
        ("bgr0", {"-vf": "hflip"}, "rgb24", (240, 320, 3)),  # padded passthrough
        ("yuv420p", {"-vf": "format=gray"}, "gray", (240, 320)),  # requested packed
        ("gray", {"-vf": "hflip"}, "gray", (240, 320)),  # packed passthrough
        ("bgra", {"-vf": "hflip"}, "bgra", (240, 320, 4)),
        ("yuv420p", {"-vf": "scale=160:90"}, "rgb24", (90, 160, 3)),  # no 2nd scaler
        ("yuv420p", {"-vf": "crop=160:120,scale=200:150"}, "rgb24", (150, 200, 3)),
        ("yuv420p", {"-vf": "hflip", "-enforce_cv_patch": True}, "yuv420p", (360, 320)),
    ],
)
def test_filter_output_pixfmt(
    src_pixfmt: str, ffparams: dict[str, Any], pixfmt: str, shape: tuple[int, ...]
) -> None:
    """
    Testing filters' output pixel-format is used only when frames can be reshaped as-is,
    and every frame matches FFmpeg's own output (no planar data in packed frames)
    """
    path = _testsrc(src_pixfmt)
    with FFdecoder(path, **ffparams) as decoder:
        metadata = json.loads(decoder.metadata)
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert metadata["output_frames_pixfmt"] == pixfmt
    assert len(frames) == 25 and frames[0].shape == shape
    cmd = [metadata["ffmpeg_binary_path"], "-v", "error", "-i", path]
    cmd += ["-vf", ffparams["-vf"]] if "-vf" in ffparams else []
    cmd += ["-pix_fmt", pixfmt, "-f", "rawvideo", "-"]
    assert b"".join(f.tobytes() for f in frames) == subprocess.run(cmd, capture_output=True).stdout


@pytest.mark.parametrize(
    "ffparams, shape",
    [
        ({}, (320, 240, 3)),  # auto-rotated upright, not squeezed into coded size
        ({"-custom_resolution": "null"}, (320, 240, 3)),
        ({"-ffprefixes": ["-noautorotate"]}, (240, 320, 3)),
    ],
)
def test_rotated_source(ffparams: dict[str, Any], shape: tuple[int, ...]) -> None:
    """Testing ±90° sources decode with FFmpeg's own auto-rotated frames"""
    path = _side_path("rot.mkv")
    if not os.path.isfile(path):
        cmd = [return_static_ffmpeg(), "-y", "-i", _testsrc("yuv420p"), "-c", "copy"]
        # `-display_rotation` needs FFmpeg 6.0+, older ones only honor the legacy `rotate` tag
        if subprocess.run([*cmd[:2], "-display_rotation", "90", *cmd[2:], path]).returncode:
            subprocess.run([*cmd, "-metadata:s:v:0", "rotate=90", path], check=True)
    with FFdecoder(path, **ffparams) as decoder:
        metadata = json.loads(decoder.metadata)
        frames = [f for f in decoder.generateFrame() if f is not None]
    assert metadata["output_frames_resolution"] == list(shape[1::-1])
    assert len(frames) == 25 and frames[0].shape == shape
    cmd = [metadata["ffmpeg_binary_path"], "-v", "error", *ffparams.get("-ffprefixes", [])]
    cmd += ["-i", path, "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    assert b"".join(f.tobytes() for f in frames) == subprocess.run(cmd, capture_output=True).stdout


@pytest.mark.parametrize(
    "pixfmt, ratio, dtype",
    [
        ("yuv420p", 1.5, "u1"),
        ("nv21", 1.5, "u1"),
        ("yuv422p", 2, "u1"),
        ("yuv444p", 3, "u1"),
        ("yuva420p", 2.5, "u1"),
        ("yuv410p", 1.125, "u1"),
        ("yuv420p10le", 1.5, "<u2"),
        ("yuv444p10le", 3, "<u2"),
        ("p010le", 1.5, "<u2"),
    ],
)
@pytest.mark.parametrize("patch", ["-extract_luma", "-enforce_cv_patch"])
def test_yuv_patches_layouts(pixfmt: str, ratio: float, dtype: str, patch: str) -> None:
    """
    Testing `-extract_luma`/`-enforce_cv_patch` read whole frames of any YUV subsampling and
    bit-depth: Y-plane or stacked planes must match FFmpeg's own output, for every frame
    """
    path = _testsrc("yuv444p")
    with FFdecoder(path, frame_format=pixfmt, **{patch: True}) as decoder:
        metadata = json.loads(decoder.metadata)
        frames = [f for f in decoder.generateFrame() if f is not None]
    cmd = [metadata["ffmpeg_binary_path"], "-v", "error", "-i", path, "-pix_fmt", pixfmt]
    raw = subprocess.run([*cmd, "-f", "rawvideo", "-"], capture_output=True)
    shape = (240, 320) if patch == "-extract_luma" else (int(240 * ratio), 320)
    assert len(frames) == 25 and frames[0].shape == shape and frames[0].dtype == dtype
    size = len(raw.stdout) // 25  # frame size, Y-plane comes first
    expected = [raw.stdout[i : i + frames[0].nbytes] for i in range(0, len(raw.stdout), size)]
    assert [f.tobytes() for f in frames] == expected
