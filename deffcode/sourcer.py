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

# import required libraries
import re, logging, os
import numpy as np

# import helper packages
from .utils import logger_handler
from .ffhelper import (
    check_sp_output,
    is_valid_url,
    is_valid_image_seq,
    get_valid_ffmpeg_path,
)

# define logger
logger = logging.getLogger("Sourcer")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


class Sourcer:
    """ """

    def __init__(self, source, custom_ffmpeg="", verbose=False, **sourcer_params):
        """
        This constructor method initializes the object state and attributes of the Sourcer.

        Parameters:
            source (str): defines the default input source.
            verbose (bool): enables/disables verbose.
            custom_ffmpeg (str): assigns the location of custom path/directory for custom FFmpeg executable.
            sourcer_params (dict): provides the flexibility to control supported internal Sourcer parameters.
        """
        # checks if machine in-use is running windows os or not
        self.__os_windows = True if os.name == "nt" else False

        # define internal parameters
        self.__verbose_logs = (  # enable verbose if specified
            verbose if (verbose and isinstance(verbose, bool)) else False
        )
        self.__ffsp_output = None  # handles metadata received
        self.__sourcer_params = {
            str(k).strip(): str(v).strip()
            if not isinstance(v, (dict, list, int, float))
            else v
            for k, v in sourcer_params.items()
        }

        # handle whether to force validate source
        self.__forcevalidatesource = self.__sourcer_params.pop(
            "-force_validate_source", False
        )
        if not isinstance(self.__forcevalidatesource, bool):
            # reset improper values
            self.__forcevalidatesource = False

        # handle where to save the downloaded FFmpeg Static assets on Windows(if specified)
        __ffmpeg_download_path = self.__sourcer_params.pop("-ffmpeg_download_path", "")
        if not isinstance(__ffmpeg_download_path, str):
            # reset improper values
            __ffmpeg_download_path = ""

        # validate the FFmpeg assets and return location (also downloads static assets on windows)
        self.__ffmpeg = get_valid_ffmpeg_path(
            str(custom_ffmpeg),
            self.__os_windows,
            ffmpeg_download_path=__ffmpeg_download_path,
            verbose=self.__verbose_logs,
        )

        # check if valid FFmpeg path returned
        if self.__ffmpeg:
            self.__verbose_logs and logger.debug(
                "Found valid FFmpeg executable: `{}`.".format(self.__ffmpeg)
            )
        else:
            # else raise error
            raise RuntimeError(
                "[DeFFcode:ERROR] :: Failed to find FFmpeg assets on this system. Kindly compile/install FFmpeg or provide a valid custom FFmpeg binary path!"
            )

        # define externally accessible parameters
        self.__source = source  # handles source stream
        self.__source_extension = os.path.splitext(source)[
            -1
        ]  # handles source stream extension
        self.__default_video_resolution = ""  # handle stream resolution
        self.__default_video_framerate = ""  # handle stream framerate
        self.__default_video_bitrate = ""  # handle stream's video bitrate
        self.__default_video_pixfmt = ""  # handle stream's video pixfmt
        self.__default_video_decoder = ""  # handle stream's video decoder
        self.__default_source_duration = ""  # handle stream's video duration
        self.__approx_video_nframes = ""  # handle approx stream frame number
        self.__default_audio_bitrate = ""  # handle stream's audio bitrate

        # handle flags
        self.__contains_video = False  # contain video
        self.__contains_audio = False  # contain audio
        self.__contains_images = False  # contain image-sequence

        # check whether metadata probed or not
        self.__metadata_probed = False

    def probe_stream(self, default_stream_indexes=(0, 0)):
        """
        Parses Source's FFmpeg Output and populates metadata in private class variables

        Parameters:
            default_stream_indexes (list, tuple): selects specific video and audio stream index in case of multiple ones. Value can be of format: (int,int). For example (0,1) is ("0th video stream", "1st audio stream").

        **Returns:** Reference to the instance object.
        """
        assert (
            isinstance(default_stream_indexes, (list, tuple))
            and len(default_stream_indexes) == 2
            and all(isinstance(x, int) for x in default_stream_indexes)
        ), "Invalid default_stream_indexes value!"
        # validate source and extract metadata
        self.__ffsp_output = self.__validate_source(self.__source)
        # parse resolution and framerate
        video_rfparams = self.__extract_resolution_framerate(
            default_stream=default_stream_indexes[0]
        )
        if video_rfparams:
            self.__default_video_resolution = video_rfparams["resolution"]
            self.__default_video_framerate = video_rfparams["framerate"]
        # parse pixel format
        self.__default_video_pixfmt = self.__extract_video_pixfmt(
            default_stream=default_stream_indexes[0]
        )
        # parse video decoder
        self.__default_video_decoder = self.__extract_video_decoder(
            default_stream=default_stream_indexes[0]
        )
        # parse rest of metadata
        if not self.__contains_images:
            # parse video bitrate
            self.__default_video_bitrate = self.__extract_video_bitrate(
                default_stream=default_stream_indexes[0]
            )
            # parse audio bitrate
            self.__default_audio_bitrate = self.__extract_audio_bitrate(
                default_stream=default_stream_indexes[1]
            )
            # parse video duration
            self.__default_source_duration = self.__extract_duration()
            # calculate all flags
            if self.__default_video_bitrate and self.__default_audio_bitrate:
                self.__contains_video = True
                self.__contains_audio = True
            elif self.__default_video_bitrate:
                self.__contains_video = True
            elif self.__default_audio_bitrate:
                self.__contains_audio = True
            else:
                raise IOError(
                    "Invalid source provided. No usable Audio/Video stream detected. Aborting!!!"
                )
        # calculate approximate number of video frame
        if self.__default_video_framerate and self.__default_source_duration:
            self.__approx_video_nframes = np.rint(
                self.__default_video_framerate * self.__default_source_duration
            ).astype(int, casting="unsafe")

        # signal metadata has been probed
        self.__metadata_probed = True

        # return reference to the instance object.
        return self

    def retrieve_metadata(self):
        """
        Returns Source metadata formatted as python dictionary.

        **Returns:** A dictionary value containing metadata.
        """
        # check if metadata has been probed or not
        assert (
            self.__metadata_probed
        ), "Source Metadata not been probed yet! Check if you called `probe_stream()` method."

        self.__verbose_logs and logger.debug("Retrieving Metadata...")
        metadata = {
            "ffmpeg_binary_path": self.__ffmpeg,
            "source": self.__source,
            "source_extension": self.__source_extension,
            "source_video_resolution": self.__default_video_resolution,
            "source_video_framerate": self.__default_video_framerate,
            "source_video_pixfmt": self.__default_video_pixfmt,
            "source_video_decoder": self.__default_video_decoder,
            "source_duration_sec": self.__default_source_duration,
            "approx_video_nframes": int(self.__approx_video_nframes)
            if self.__approx_video_nframes
            else None,
            "source_video_bitrate": self.__default_video_bitrate,
            "source_audio_bitrate": self.__default_audio_bitrate,
            "source_has_video": self.__contains_video,
            "source_has_audio": self.__contains_audio,
            "source_has_image_sequence": self.__contains_images,
        }
        return metadata

    def __validate_source(self, source):
        """
        Internal method for validating source and extract its FFmpeg metadata.
        """
        if source is None or not source or not isinstance(source, str):
            raise ValueError("Input source is empty!")
        # Differentiate input
        if os.path.isfile(source):
            self.__video_source = os.path.abspath(source)
        elif is_valid_image_seq(
            self.__ffmpeg, source=source, verbose=self.__verbose_logs
        ):
            self.__video_source = source
            self.__contains_images = True
        elif is_valid_url(self.__ffmpeg, url=source, verbose=self.__verbose_logs):
            self.__video_source = source
        elif self.__forcevalidatesource:
            logger.critical("Forcefully passing validation test for given source!")
            self.__video_source = source
        else:
            logger.error("`source` value is unusable or unsupported!")
            # discard the value otherwise
            raise ValueError("Input source is invalid. Aborting!")
        # extract metadata
        metadata = check_sp_output(
            [self.__ffmpeg, "-hide_banner", "-i", source], force_retrieve_stderr=True
        )
        # filter and return
        return metadata.decode("utf-8").strip()

    def __extract_video_bitrate(self, default_stream=0):
        """
        Parses default video-stream bitrate from metadata.

        Parameters:
            default_stream (int): selects specific video-stream in case of multiple ones.

        **Returns:** A string value.
        """
        identifiers = ["Video:", "Stream #"]
        video_bitrate_text = [
            line.strip()
            for line in self.__ffsp_output.split("\n")
            if all(x in line for x in identifiers)
        ]
        if video_bitrate_text:
            selected_stream = video_bitrate_text[
                default_stream
                if default_stream > 0 and default_stream < len(video_bitrate_text)
                else 0
            ]
            filtered_bitrate = re.findall(
                r",\s[0-9]+\s\w\w[/]s", selected_stream.strip()
            )
            default_video_bitrate = filtered_bitrate[0].split(" ")[1:3]
            final_bitrate = "{}{}".format(
                int(default_video_bitrate[0].strip()),
                "k" if (default_video_bitrate[1].strip().startswith("k")) else "M",
            )
            return final_bitrate
        else:
            return ""

    def __extract_video_decoder(self, default_stream=0):
        """
        Parses default video-stream decoder from metadata.

        Parameters:
            default_stream (int): selects specific video-stream in case of multiple ones.

        **Returns:** A string value.
        """
        assert isinstance(default_stream, int), "Invalid input!"
        identifiers = ["Video:", "Stream #"]
        meta_text = [
            line.strip()
            for line in self.__ffsp_output.split("\n")
            if all(x in line for x in identifiers)
        ]
        if meta_text:
            selected_stream = meta_text[
                default_stream
                if default_stream > 0 and default_stream < len(meta_text)
                else 0
            ]
            filtered_pixfmt = re.findall(
                r"Video:\s[a-z0-9_-]*", selected_stream.strip()
            )
            return filtered_pixfmt[0].split(" ")[-1]
        else:
            return ""

    def __extract_video_pixfmt(self, default_stream=0):
        """
        Parses default video-stream pixel format from metadata.

        Parameters:
            default_stream (int): selects specific video-stream in case of multiple ones.

        **Returns:** A string value.
        """
        identifiers = ["Video:", "Stream #"]
        meta_text = [
            line.strip()
            for line in self.__ffsp_output.split("\n")
            if all(x in line for x in identifiers)
        ]
        if meta_text:
            selected_stream = meta_text[
                default_stream
                if default_stream > 0 and default_stream < len(meta_text)
                else 0
            ]
            filtered_pixfmt = re.findall(
                r",\s[a-z][a-z0-9_-]*", selected_stream.strip()
            )
            return filtered_pixfmt[0].split(" ")[-1]
        else:
            return ""

    def __extract_audio_bitrate(self, default_stream=0):
        """
        Parses default audio-stream bitrate from metadata.

        Parameters:
            default_stream (int): selects specific audio-stream in case of multiple ones.

        **Returns:** A string value.
        """
        default_audio_bitrate = re.findall(
            r"fltp,\s[0-9]+\s\w\w[/]s", self.__ffsp_output
        )
        sample_rate_identifiers = ["Audio", "Hz"] + (
            ["fltp"] if isinstance(self.__source, str) else []
        )
        audio_sample_rate = [
            line.strip()
            for line in self.__ffsp_output.split("\n")
            if all(x in line for x in sample_rate_identifiers)
        ]
        if default_audio_bitrate:
            selected_stream = (
                default_stream
                if default_stream > 0 and default_stream < len(default_audio_bitrate)
                else 0
            )
            filtered = default_audio_bitrate[selected_stream].split(" ")[1:3]
            final_bitrate = "{}{}".format(
                int(filtered[0].strip()),
                "k" if (filtered[1].strip().startswith("k")) else "M",
            )
            return final_bitrate
        elif audio_sample_rate:
            selected_stream = (
                default_stream
                if default_stream > 0 and default_stream < len(audio_sample_rate)
                else 0
            )
            sample_rate = re.findall(r"[0-9]+\sHz", audio_sample_rate[selected_stream])[
                0
            ]
            sample_rate_value = int(sample_rate.split(" ")[0])
            samplerate_2_bitrate = int(
                (sample_rate_value - 44100) * (320 - 96) / (48000 - 44100) + 96
            )
            return str(samplerate_2_bitrate) + "k"
        else:
            return ""

    def __extract_resolution_framerate(self, default_stream=0):
        """
        Parses default video-stream resolution and framerate from metadata.

        **Returns:** A dictionary value.
        """
        identifiers = ["Video:", "Stream #"]
        meta_text = [
            line.strip()
            for line in self.__ffsp_output.split("\n")
            if all(x in line for x in identifiers)
        ]
        result = {}
        if meta_text:
            selected_stream = meta_text[
                default_stream
                if default_stream > 0 and default_stream < len(meta_text)
                else 0
            ]
            # filter data
            filtered_resolution = re.findall(
                r"([1-9]\d+)x([1-9]\d+)", selected_stream.strip()
            )
            filtered_framerate = re.findall(
                r"\d+(?:\.\d+)?\sfps", selected_stream.strip()
            )
            # get framerate and resolution metadata
            if filtered_framerate:
                result["framerate"] = float(
                    re.findall(r"[\d\.\d]+", filtered_framerate[0])[0]
                )
            if filtered_resolution:
                result["resolution"] = [int(x) for x in filtered_resolution[0]]
        return result if result and (len(result) == 2) else {}

    def __extract_duration(self, inseconds=True):
        """
        Parses stream duration from metadata.

        **Returns:** A string value.
        """
        identifiers = ["Duration:"]
        stripped_data = [
            line.strip()
            for line in self.__ffsp_output.split("\n")
            if all(x in line for x in identifiers)
        ]
        if stripped_data:
            t_duration = re.findall(
                r"(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d+(?:\.\d+)?)",
                stripped_data[0],
            )
            if t_duration:
                return (
                    sum(
                        float(x) * 60 ** i
                        for i, x in enumerate(reversed(t_duration[0].split(":")))
                    )
                    if inseconds
                    else t_duration
                )
        return 0
