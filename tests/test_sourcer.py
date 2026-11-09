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

import logging
import os
import subprocess
from typing import Any

import pytest

from deffcode import Sourcer
from deffcode import sourcer as sourcer_module
from deffcode.utils import logger_handler

from .essentials import (
    actual_frame_count_n_frame_size,
    return_generated_frames_path,
    return_static_ffmpeg,
    return_testvideo_path,
)

# define test logger
logger = logging.getLogger("Test_Sourcer")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize(
    "source, sourcer_params, custom_ffmpeg",
    [
        (
            return_generated_frames_path(return_static_ffmpeg()),
            {
                "-ffprefixes": "invalid",  # invalid ffprefixes
                "-filter_complex": "loop=loop=3:size=15:start=25",
            },
            return_static_ffmpeg(),
        ),
        (
            "rtmp://live.twitch.tv/",
            {
                "-ffmpeg_download_path": ["invalid"],  # invalid FFmpeg download path
                "-ffprefixes": ["-stream_loop", "3"],
            },
            return_static_ffmpeg(),
        ),
        (
            "unknown://invalid.com/",  # invalid source-1
            {"-force_validate_source": True},  # force_validate_source
            return_static_ffmpeg(),
        ),
        (
            return_testvideo_path(fmt="ao"),
            {"-force_validate_source": ["invalid"]},  # invalid force_validate_source
            return_static_ffmpeg(),
        ),
        (
            return_testvideo_path(),
            {},
            "invalid_ffmpeg",  # invalid FFmpeg
        ),
        (
            [return_testvideo_path(), return_testvideo_path()],
            {
                "-ffprefixes": [["-re"], ["-stream_loop", "-1"]],
            },
            return_static_ffmpeg(),
        ),
        (
            [return_testvideo_path(), return_testvideo_path()],
            {
                "-ffprefixes": "invalid"  # list of lists mismatch
            },
            return_static_ffmpeg(),
        ),
    ],
)
def test_source(
    source: str | list[str], sourcer_params: dict[str, Any], custom_ffmpeg: str
) -> None:
    """
    Paths Source - Test various source paths/urls supported by Sourcer.
    """
    try:
        sourcer = Sourcer(
            source, custom_ffmpeg=custom_ffmpeg, verbose=True, **sourcer_params
        ).probe_stream()
        logger.debug("Found Metadata: `{}`".format(sourcer.retrieve_metadata()))
    except Exception as e:
        if isinstance(e, ValueError) or custom_ffmpeg == "invalid_ffmpeg":
            pytest.xfail("Test Passed!")
        else:
            pytest.fail(str(e))


@pytest.mark.parametrize(
    "source, default_stream_indexes, params",
    [
        (return_testvideo_path(), [0, 0], ["source_has_video", "source_has_audio"]),
        ("mandelbrot=size=1280x720:rate=30", [0, 0], ["source_has_video"]),
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
        (
            [return_testvideo_path(), "mandelbrot=size=1280x720:rate=30"],
            (0, 0),
            ["source_has_video", "sources"],  # tests sources list
        ),
    ],
)
def test_probe_stream_n_retrieve_metadata(
    source: str | list[str],
    default_stream_indexes: tuple[int, ...] | list[int],
    params: list[str],
) -> None:
    """
    Test `probe_stream` and `retrieve_metadata` function.
    """
    try:
        source_demuxer = None
        if isinstance(source, list):
            source_demuxer = [
                "lavfi" if s == "mandelbrot=size=1280x720:rate=30" else None for s in source
            ]
        elif source == "mandelbrot=size=1280x720:rate=30":
            source_demuxer = "lavfi"

        if source == "invalid":
            sourcer = Sourcer(source, custom_ffmpeg=return_static_ffmpeg(), verbose=True)
        else:
            sourcer = Sourcer(
                source,
                custom_ffmpeg=return_static_ffmpeg(),
                source_demuxer=source_demuxer,
                verbose=True,
            ).probe_stream(default_stream_indexes=default_stream_indexes)
        metadata = sourcer.retrieve_metadata()
        logger.debug("Found Metadata: `{}`".format(metadata))

        # Test sources exists and is valid
        if "sources" in params:
            assert "sources" in metadata and len(metadata["sources"]) == len(source), (
                "Multi-input Test Failed!"
            )

        assert all(
            metadata.get(x, metadata["sources"] if x == "sources" else False) for x in params
        ), "Test Failed!"

        is_skipped = False
        if isinstance(source, list) or (
            source.startswith("http")
            or source.endswith("png")
            or source == "mandelbrot=size=1280x720:rate=30"
        ):
            is_skipped = True

        if is_skipped:
            logger.debug("Skipped check!")
        else:
            assert metadata["approx_video_nframes"] >= actual_frame_count_n_frame_size(source)[0], (
                "Test Failed for frames count!"
            )
    except Exception as e:
        if isinstance(e, ValueError) or (
            source in ["invalid", "unknown://invalid.com/"] and isinstance(e, AssertionError)
        ):
            pytest.xfail("Test Still Passed!")
        else:
            pytest.fail(str(e))


def test_multi_input_primary_metadata() -> None:
    """
    Primary `source_*` metadata must describe input 0 only, even with a
    nonzero default video stream index and a combined filtergraph probe.
    """
    metadata = (
        Sourcer(
            [
                "testsrc=size=320x240:rate=25:duration=2",
                "testsrc=size=160x120:rate=10:duration=2",
            ],
            source_demuxer="lavfi",
            **{"-filter_complex": "[0:v][1:v]overlay"},
        )
        .probe_stream(default_stream_indexes=(1, 0))
        .retrieve_metadata()
    )
    assert metadata["source_video_resolution"] == [320, 240]
    assert metadata["source_video_framerate"] == 25.0
    assert [s["source_video_resolution"] for s in metadata["sources"]] == [
        [320, 240],
        [160, 120],
    ]


def test_multi_stream_indexes(monkeypatch: Any) -> None:
    """
    Stream indexes are per type (`0:v:N`); out-of-range ones warn and fall back to stream 0.
    Stream count is reported, and nothing warns for index 0.
    """
    src = "color=c=red:s=320x240:r=25:d=2[out0];color=c=blue:s=160x120:r=30:d=2[out1]"
    warnings: list[str] = []
    monkeypatch.setattr(sourcer_module.logger, "warning", warnings.append)
    for indexes, resolution, framerate, n_warnings in [
        ((1, 0), [160, 120], 30.0, 0),
        ((5, 0), [320, 240], 25.0, 1),
        ((0, 0), [320, 240], 25.0, 1),
    ]:
        metadata = (
            Sourcer(src, source_demuxer="lavfi")
            .probe_stream(default_stream_indexes=indexes)
            .retrieve_metadata()
        )
        assert metadata["source_video_resolution"] == resolution
        assert metadata["source_video_framerate"] == framerate
        assert len(warnings) == n_warnings
        assert metadata["source_video_streams"] == 2


@pytest.mark.parametrize("label", ["displaymatrix", "Display Matrix"])  # FFmpeg < 8.1, >= 8.1
def test_orientation_parsing(label: str) -> None:
    """
    Rotation must parse with either side-data label and stay paired with its
    own video stream (audio streams and unrotated streams in between).
    """
    banner = f"""Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'multi.mp4':
  Stream #0:0[0x1](und): Video: h264 (Main), yuv420p, 1280x720, 25 fps, 25 tbr, 12800 tbn
  Stream #0:1[0x2](und): Audio: aac (LC), 44100 Hz, stereo, fltp, 128 kb/s
  Stream #0:2[0x3](und): Video: h264 (Main), yuv420p, 640x360, 30 fps, 30 tbr, 15360 tbn
    Side data:
      {label}: rotation of -90.00 degrees"""
    sourcer = Sourcer(return_testvideo_path(), custom_ffmpeg=return_static_ffmpeg())
    sourcer._Sourcer__ffsp_output = banner
    extract = sourcer._Sourcer__extract_resolution_framerate
    assert extract(default_stream=0)["orientation"] == 0.0
    assert extract(default_stream=1) == {
        "framerate": 30.0,
        "resolution": [640, 360],
        "orientation": -90.0,
    }


def test_orientation_and_relative_path(tmp_path: Any, monkeypatch: Any) -> None:
    """
    Real rotated clip reports its rotation, and a relative DASH manifest path
    (which FFmpeg's dash demuxer can't open) probes fine.
    """
    ffmpeg = return_static_ffmpeg()
    monkeypatch.chdir(tmp_path)
    os.makedirs("dash")
    for cmd in (
        ["-display_rotation", "90", "-i", return_testvideo_path(fmt="vo"), "-c", "copy", "rot.mp4"],
        ["-i", return_testvideo_path(fmt="vo"), "-c", "copy", "-f", "dash", "dash/a.mpd"],
    ):
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *cmd], check=True)

    rot = Sourcer("rot.mp4", custom_ffmpeg=ffmpeg).probe_stream().retrieve_metadata()
    assert rot["source_video_orientation"] == 90.0

    dash = Sourcer("dash/a.mpd", custom_ffmpeg=ffmpeg).probe_stream().retrieve_metadata()
    assert dash["source_video_resolution"] == [1280, 720]


@pytest.mark.parametrize(
    "video, sar, dar, color",
    [
        (  # HDR10, anamorphic (FFmpeg >= 5.x adds per-stream `start`)
            "hevc (Main 10), yuv420p10le(tv, bt2020nc/bt2020/smpte2084, progressive), 1440x1080 [SAR 4:3 DAR 16:9], 25 fps, 25 tbr, 1k tbn, start 10.000000",
            [4, 3],
            [16, 9],
            ["tv", "bt2020nc", "bt2020", "smpte2084"],
        ),
        (  # single name when space = primaries = transfer
            "h264 (High), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 25 fps, 25 tbr, 1k tbn",
            [1, 1],
            [16, 9],
            ["tv", "bt709", "bt709", "bt709"],
        ),
        (  # unknowns, nested field order parens, container SAR overriding codec SAR
            "h264 (High), yuvj420p(pc, bt709/unknown/unknown, top coded first (swapped)), 720x576 [SAR 1:1 DAR 5:4], SAR 16:15 DAR 4:3, 25 fps, 25 tbr, 1k tbn",
            [16, 15],
            [4, 3],
            ["pc", "bt709", "", ""],
        ),
        (  # no details or SAR at all (FFmpeg 4.4 rawvideo)
            "rawvideo (I420 / 0x30323449), yuv444p, 720x576, 25 fps, 25 tbr, 25 tbn, 25 tbc",
            [1, 1],
            [5, 4],
            ["", "", "", ""],
        ),
    ],
)
def test_banner_metadata_parsing(
    monkeypatch: Any, video: str, sar: list[int], dar: list[int], color: list[str]
) -> None:
    """
    SAR/DAR, color, start time, non-`fltp` audio bitrate, and durations >= 24h parse from banner.
    """
    banner = f"""Input #0, matroska,webm, from 'x.mkv':
  Duration: 25:00:01.50, start: 10.000000, bitrate: 251 kb/s
  Stream #0:0: Video: {video} (default)
  Stream #0:1: Audio: pcm_s16le, 44100 Hz, stereo, s16, 1411 kb/s"""
    monkeypatch.setattr(Sourcer, "_Sourcer__validate_source", lambda *args, **kwargs: banner)
    metadata = Sourcer("x.mkv").probe_stream().retrieve_metadata()
    assert metadata["source_video_sar"] == sar
    assert metadata["source_video_dar"] == dar
    assert [
        metadata["source_video_color_" + k] for k in ("range", "space", "primaries", "transfer")
    ] == color
    assert metadata["source_start_sec"] == 10.0
    assert metadata["source_duration_sec"] == 90001.5
    assert metadata["source_audio_bitrate"] == "1411k"
