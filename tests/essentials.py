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

import os, cv2
import tempfile
import logging
import platform
from vidgear.gears import WriteGear
from deffcode.utils import logger_handler

# define test logger
logger = logging.getLogger("Essentials")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)

# define machine os
is_windows = True if os.name == "nt" else False


def return_static_ffmpeg():
    """
    returns system specific FFmpeg static path
    """
    path = ""
    if platform.system() == "Windows":
        path += os.path.join(
            tempfile.gettempdir(), "Downloads/FFmpeg_static/ffmpeg/bin/ffmpeg.exe"
        )
    elif platform.system() == "Darwin":
        path += os.path.join(
            tempfile.gettempdir(), "Downloads/FFmpeg_static/ffmpeg/bin/ffmpeg"
        )
    else:
        path += os.path.join(
            tempfile.gettempdir(), "Downloads/FFmpeg_static/ffmpeg/ffmpeg"
        )
    return os.path.abspath(path)


def remove_file_safe(path):
    """
    Remove file safely
    """
    try:
        if path and os.path.isfile(os.path.abspath(path)):
            os.remove(path)
    except Exception as e:
        logger.exception(e)


def return_testvideo_path(fmt="av"):
    """
    returns Test video path
    """
    supported_fmts = {
        "av": "BigBuckBunny_4sec.mp4",
        "vo": "BigBuckBunny_4sec_VO.mp4",
        "ao": "BigBuckBunny_4sec_AO.mp4",
    }
    req_fmt = fmt if (fmt in supported_fmts) else "av"
    path = "{}/Downloads/Test_videos/{}".format(
        tempfile.gettempdir(), supported_fmts[req_fmt]
    )
    return os.path.abspath(path)


def return_generated_frames_path(path):
    """
    returns Test video path
    """
    # create paths
    video_path = return_testvideo_path(fmt="vo")
    frame_dir = "{}/temp_images".format(tempfile.gettempdir())
    frames_path = os.path.join(frame_dir, "out%d.png")
    # check if empty
    if not os.listdir(frame_dir):
        # Define writer with default parameters
        writer = WriteGear(
            output_filename=os.path.join(
                *[tempfile.gettempdir(), "temp_write", "Output.mp4"]
            ),
            custom_ffmpeg=path,
        )
        # execute FFmpeg command
        writer.execute_ffmpeg_cmd(["-i", video_path, frames_path])
        # safely close writer
        writer.close()
    # return path
    return frames_path


def actual_frame_count_n_frame_size(path):
    """
    simply counts the total frames in a given video
    """
    stream = cv2.VideoCapture(path)
    num_cv = 0
    shape = None
    while True:
        (grabbed, frame) = stream.read()
        if not grabbed:
            logger.debug("Total frames: {}".format(num_cv))
            break
        else:
            if shape is None:
                shape = frame.shape
                logger.debug("Frames Shape: {}".format(shape))
        num_cv += 1
    stream.release()
    return (num_cv, shape)
