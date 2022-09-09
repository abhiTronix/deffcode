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
import re
import os
import copy
import json
import logging
import platform
import numpy as np

# import utils packages
from .utils import logger_handler, validate_device_index, dict2Args
from .ffhelper import (
    check_sp_output,
    get_supported_demuxers,
    is_valid_url,
    is_valid_image_seq,
    get_valid_ffmpeg_path,
    extract_device_n_demuxer,
)

# define logger
logger = logging.getLogger("Sourcer")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


class Sourcer:
    """
    > Sourcer API acts as **Source Probing Utility** that unlike other FFmpeg Wrappers which mostly uses [`ffprobe`](https://ffmpeg.org/ffprobe.html) module,
    attempts to open the given Input Source directly with [**FFmpeg**](https://ffmpeg.org/) inside a [`subprocess`](https://docs.python.org/3/library/subprocess.html) pipe,
    and parses/probes the standard output(stdout) employing various pattern matching methods in order to recognize all the properties(metadata) of each
    media stream contained in it.

    Sourcer API primarily acts as a **backend for [FFdecoder API](../../reference/ffdecoder)** for gathering, processing, and validating
    all multimedia streams metadata available in the given Input Source. Sourcer shares this information with FFdecoder API which helps in
    formulating its default FFmpeg pipeline parameters for real-time video-frames generation.

    Sourcer API is design as a standalone **Metadata Extraction API** for easily parsing information from multimedia streams available in the
    given Input Source and returns it in either Human-readable _(JSON string)_ or Machine-readable _(Dictionary object)_ type with its
    [`retrieve_metadata()`](#deffcode.sourcer.Sourcer.retrieve_metadata) method.

    !!! info "All metadata attributes available with Sourcer API(On :fontawesome-brands-windows: Windows) are discussed [here ➶](../../recipes/basic/#display-source-video-metadata)."

    Furthermore, Sourcer's [`sourcer_params`](params/#sourcer_params) dictionary parameter can be used to define almost any FFmpeg parameter as well as alter internal API settings.

    !!! example "For usage examples, kindly refer our **[Basic Recipes :cake:](../../recipes/basic)** and **[Advanced Recipes :croissant:](../../recipes/advanced)**"

    !!! info "Sourcer API parameters are explained [here ➶](params/)"
    """

    def __init__(
        self,
        source,
        source_demuxer=None,
        custom_ffmpeg="",
        verbose=False,
        **sourcer_params,
    ):
        """
        This constructor method initializes the object state and attributes of the Sourcer Class.

        Parameters:
            source (str): defines the input(`-i`) source filename/URL/device-name/device-path.
            source_demuxer (str): specifies the demuxer(`-f`) for the input source.
            custom_ffmpeg (str): assigns the location of custom path/directory for custom FFmpeg executable.
            verbose (bool): enables/disables verbose.
            sourcer_params (dict): provides the flexibility to control supported internal and FFmpeg parameters.
        """
        # checks if machine in-use is running windows os or not
        self.__machine_OS = platform.system()

        # define internal parameters
        self.__verbose_logs = (  # enable verbose if specified
            verbose if (verbose and isinstance(verbose, bool)) else False
        )

        # handle metadata received
        self.__ffsp_output = None

        # sanitize sourcer_params
        self.__sourcer_params = {
            str(k).strip(): str(v).strip()
            if not isinstance(v, (dict, list, int, float, tuple))
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

        # handle user defined ffmpeg pre-headers(parameters such as `-re`) parameters (must be a list)
        self.__ffmpeg_prefixes = self.__sourcer_params.pop("-ffprefixes", [])
        if not isinstance(self.__ffmpeg_prefixes, list):
            # log it
            logger.warning(
                "Discarding invalid `-ffprefixes` value of wrong type `{}`!".format(
                    type(self.__ffmpeg_prefixes).__name__
                )
            )
            # reset improper values
            self.__ffmpeg_prefixes = []

        # handle where to save the downloaded FFmpeg Static assets on Windows(if specified)
        __ffmpeg_download_path = self.__sourcer_params.pop("-ffmpeg_download_path", "")
        if not isinstance(__ffmpeg_download_path, str):
            # reset improper values
            __ffmpeg_download_path = ""

        # validate the FFmpeg assets and return location (also downloads static assets on windows)
        self.__ffmpeg = get_valid_ffmpeg_path(
            str(custom_ffmpeg),
            True if self.__machine_OS == "Windows" else False,
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

        # sanitize externally accessible parameters and assign them
        # handles source demuxer
        if source is None:
            # first check if source value is empty
            # raise error if true
            raise ValueError("Input `source` parameter is empty!")
        elif isinstance(source_demuxer, str):
            # assign if valid demuxer value
            self.__source_demuxer = source_demuxer.strip().lower()
            # assign if valid demuxer value
            assert self.__source_demuxer != "auto" or validate_device_index(
                source
            ), "Invalid `source_demuxer='auto'` value detected with source: `{}`. Aborting!".format(
                source
            )
        else:
            # otherwise find valid default source demuxer value
            # enforce "auto" if valid index device
            self.__source_demuxer = "auto" if validate_device_index(source) else None
            # log if not valid index device and invalid type
            self.__verbose_logs and not self.__source_demuxer in [
                "auto",
                None,
            ] and logger.warning(
                "Discarding invalid `source_demuxer` parameter value of wrong type: `{}`".format(
                    type(source_demuxer).__name__
                )
            )
            # log if not valid index device and invalid type
            self.__verbose_logs and self.__source_demuxer == "auto" and logger.critical(
                "Given source `{}` is a valid device index. Enforcing 'auto' demuxer.".format(
                    source
                )
            )

        # handles source stream
        self.__source = source

        # creates shallow copy for further usage #TODO
        self.__source_org = copy.copy(self.__source)
        self.__source_demuxer_org = copy.copy(self.__source_demuxer)

        # handles all extracted devices names/paths list
        # when source_demuxer = "auto"
        self.__extracted_devices_list = []

        # various source stream params
        self.__default_video_resolution = ""  # handles stream resolution
        self.__default_video_framerate = ""  # handles stream framerate
        self.__default_video_bitrate = ""  # handles stream's video bitrate
        self.__default_video_pixfmt = ""  # handles stream's video pixfmt
        self.__default_video_decoder = ""  # handles stream's video decoder
        self.__default_source_duration = ""  # handles stream's video duration
        self.__approx_video_nframes = ""  # handles approx stream frame number
        self.__default_audio_bitrate = ""  # handles stream's audio bitrate
        self.__default_audio_samplerate = ""  # handles stream's audio samplerate

        # handle various stream flags
        self.__contains_video = False  # contains video
        self.__contains_audio = False  # contains audio
        self.__contains_images = False  # contains image-sequence

        # handles output parameters through filters
        self.__metadata_output = None  # handles output stream metadata
        self.__output_frames_resolution = ""  # handles output stream resolution
        self.__output_framerate = ""  # handles output stream framerate
        self.__output_frames_pixfmt = ""  # handles output frame pixel format

        # check whether metadata probed or not?
        self.__metadata_probed = False

    def probe_stream(self, default_stream_indexes=(0, 0)):
        """
        This method Parses/Probes FFmpeg `subprocess` pipe's Standard Output for given input source and Populates the information in private class variables.

        Parameters:
            default_stream_indexes (list, tuple): selects specific video and audio stream index in case of multiple ones. Value can be of format: `(int,int)`. For example `(0,1)` is ("0th video stream", "1st audio stream").

        **Returns:** Reference to the instance object.
        """
        assert (
            isinstance(default_stream_indexes, (list, tuple))
            and len(default_stream_indexes) == 2
            and all(isinstance(x, int) for x in default_stream_indexes)
        ), "Invalid default_stream_indexes value!"
        # validate source and extract metadata
        self.__ffsp_output = self.__validate_source(
            self.__source,
            source_demuxer=self.__source_demuxer,
            forced_validate=(
                self.__forcevalidatesource if self.__source_demuxer is None else True
            ),
        )
        # parse resolution and framerate
        video_rfparams = self.__extract_resolution_framerate(
            default_stream=default_stream_indexes[0]
        )
        if video_rfparams:
            self.__default_video_resolution = video_rfparams["resolution"]
            self.__default_video_framerate = video_rfparams["framerate"]

        # parse output parameters through filters (if available)
        if not (self.__metadata_output is None):
            # parse output resolution and framerate
            out_video_rfparams = self.__extract_resolution_framerate(
                default_stream=default_stream_indexes[0], extract_output=True
            )
            if out_video_rfparams:
                self.__output_frames_resolution = out_video_rfparams["resolution"]
                self.__output_framerate = out_video_rfparams["framerate"]
            # parse output pixel-format
            self.__output_frames_pixfmt = self.__extract_video_pixfmt(
                default_stream=default_stream_indexes[0], extract_output=True
            )

        # parse pixel-format
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
            # parse audio bitrate and samplerate
            audio_params = self.__extract_audio_bitrate_nd_samplerate(
                default_stream=default_stream_indexes[1]
            )
            if audio_params:
                self.__default_audio_bitrate = audio_params["bitrate"]
                self.__default_audio_samplerate = audio_params["samplerate"]
            # parse video duration
            self.__default_source_duration = self.__extract_duration()
            # calculate all flags
            if (
                self.__default_video_bitrate
                or (self.__default_video_framerate and self.__default_video_resolution)
            ) and (self.__default_audio_bitrate or self.__default_audio_samplerate):
                self.__contains_video = True
                self.__contains_audio = True
            elif self.__default_video_bitrate or (
                self.__default_video_framerate and self.__default_video_resolution
            ):
                self.__contains_video = True
            elif self.__default_audio_bitrate or self.__default_audio_samplerate:
                self.__contains_audio = True
            else:
                raise ValueError(
                    "Invalid source with no decodable audio or video stream provided. Aborting!"
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

    def retrieve_metadata(self, pretty_json=False, force_retrieve_missing=False):
        """
        This method returns Parsed/Probed Metadata of the given source.

        Parameters:
            pretty_json (bool): whether to return metadata as JSON string(if `True`) or Dictionary(if `False`) type?
            force_retrieve_output (bool): whether to also return metadata missing in current Pipeline. This method returns `(metadata, metadata_missing)` tuple if `force_retrieve_output=True` instead of `metadata`.

        **Returns:** `metadata` or `(metadata, metadata_missing)`, formatted as JSON string or python dictionary.
        """
        # check if metadata has been probed or not
        assert (
            self.__metadata_probed
        ), "Source Metadata not been probed yet! Check if you called `probe_stream()` method."
        # log it
        self.__verbose_logs and logger.debug("Extracting Metadata...")
        # create metadata dictionary from information populated in private class variables
        metadata = {
            "ffmpeg_binary_path": self.__ffmpeg,
            "source": self.__source,
        }
        metadata_missing = {}
        # Only either `source_demuxer` or `source_extension` attribute can be
        # present in metadata.
        if self.__source_demuxer is None:
            metadata.update({"source_extension": os.path.splitext(self.__source)[-1]})
            # update missing
            force_retrieve_missing and metadata_missing.update({"source_demuxer": ""})
        else:
            metadata.update({"source_demuxer": self.__source_demuxer})
            # update missing
            force_retrieve_missing and metadata_missing.update({"source_extension": ""})
        # add source video metadata properties
        metadata.update(
            {
                "source_video_resolution": self.__default_video_resolution,
                "source_video_pixfmt": self.__default_video_pixfmt,
                "source_video_framerate": self.__default_video_framerate,
                "source_video_decoder": self.__default_video_decoder,
                "source_duration_sec": self.__default_source_duration,
                "approx_video_nframes": (
                    int(self.__approx_video_nframes)
                    if self.__approx_video_nframes
                    else None
                ),
                "source_video_bitrate": self.__default_video_bitrate,
                "source_audio_bitrate": self.__default_audio_bitrate,
                "source_audio_samplerate": self.__default_audio_samplerate,
                "source_has_video": self.__contains_video,
                "source_has_audio": self.__contains_audio,
                "source_has_image_sequence": self.__contains_images,
            }
        )
        # add output metadata properties (if available)
        if not (self.__metadata_output is None):
            metadata.update(
                {
                    "output_frames_resolution": self.__output_frames_resolution,
                    "output_frames_pixfmt": self.__output_frames_pixfmt,
                    "output_framerate": self.__output_framerate,
                }
            )
        else:
            # since output stream metadata properties are only available when additional
            # FFmpeg parameters(such as filters) are defined manually, thereby missing
            # output stream properties are handled by assigning them counterpart source
            # stream metadata property values
            force_retrieve_missing and metadata_missing.update(
                {
                    "output_frames_resolution": self.__default_video_resolution,
                    "output_frames_pixfmt": self.__default_video_pixfmt,
                    "output_framerate": self.__default_video_framerate,
                }
            )
        # log it
        self.__verbose_logs and logger.debug(
            "Metadata Extraction completed successfully!"
        )
        # parse as JSON string(`json.dumps`), if defined
        metadata = json.dumps(metadata, indent=2) if pretty_json else metadata
        metadata_missing = (
            json.dumps(metadata_missing, indent=2) if pretty_json else metadata_missing
        )
        # return `metadata` or `(metadata, metadata_missing)`
        return metadata if not force_retrieve_missing else (metadata, metadata_missing)

    @property
    def enumerate_devices(self):
        """
        A property object that enumerate all probed Camera Devices connected to your system names
        along with their respective "device indexes" or "camera indexes" as python dictionary.

        **Returns:** Probed Camera Devices as python dictionary.
        """
        # check if metadata has been probed or not
        assert (
            self.__metadata_probed
        ), "Source Metadata not been probed yet! Check if you called `probe_stream()` method."

        # log if specified
        self.__verbose_logs and logger.debug("Enumerating all probed Camera Devices.")

        # return probed Camera Devices as python dictionary.
        return {
            dev_idx: dev for dev_idx, dev in enumerate(self.__extracted_devices_list)
        }

    def __validate_source(self, source, source_demuxer=None, forced_validate=False):
        """
        This Internal method validates source and extracts its metadata.

        Parameters:
            source_demuxer(str): specifies the demuxer(`-f`) for the input source.
            forced_validate (bool): whether to skip validation tests or not?

        **Returns:** `True` if passed tests else `False`.
        """
        # validate source demuxer(if defined)
        if not (source_demuxer is None):
            # check if "auto" demuxer is specified
            if source_demuxer == "auto":
                # integerise source to get index
                index = int(source)
                # extract devices list and actual demuxer value
                (
                    self.__extracted_devices_list,
                    source_demuxer,
                ) = extract_device_n_demuxer(
                    self.__ffmpeg,
                    machine_OS=self.__machine_OS,
                    verbose=self.__verbose_logs,
                )
                # valid indexes range
                valid_indexes = [
                    x
                    for x in range(
                        -len(self.__extracted_devices_list),
                        len(self.__extracted_devices_list),
                    )
                ]
                # check index is within valid range
                if self.__extracted_devices_list and index in valid_indexes:
                    # overwrite actual source device name/path/index
                    if self.__machine_OS == "Windows":
                        # Windows OS requires "video=" suffix
                        self.__source = source = "video={}".format(
                            self.__extracted_devices_list[index]
                        )
                    elif self.__machine_OS == "Darwin":
                        # Darwin OS requires only device indexes
                        self.__source = source = (
                            str(index)
                            if index >= 0
                            else str(len(self.__extracted_devices_list) + index)
                        )
                    else:
                        # Linux OS require /dev/video format
                        self.__source = source = next(
                            iter(self.__extracted_devices_list[index].keys())
                        )
                    # overwrite source_demuxer global variable
                    self.__source_demuxer = source_demuxer
                    self.__verbose_logs and logger.debug(
                        "Successfully configured device `{}` at index `{}` with demuxer `{}`.".format(
                            self.__extracted_devices_list[index]
                            if self.__machine_OS != "Linux"
                            else next(
                                iter(self.__extracted_devices_list[index].values())
                            )[0],
                            index
                            if index >= 0
                            else len(self.__extracted_devices_list) + index,
                            self.__source_demuxer,
                        )
                    )
                else:
                    # raise error otherwise
                    raise ValueError(
                        "Given source `{}` is not a valid device index. Possible values index values can be: {}".format(
                            source,
                            ",".join(f"{x}" for x in valid_indexes),
                        )
                    )
            # otherwise validate against supported demuxers
            elif not (source_demuxer in get_supported_demuxers(self.__ffmpeg)):
                # raise if fails
                raise ValueError(
                    "Installed FFmpeg failed to recognize `{}` demuxer. Check `source_demuxer` parameter value again!".format(
                        source_demuxer
                    )
                )
            else:
                pass

        # assert if valid source
        assert source and isinstance(
            source, str
        ), "Input `source` parameter is of invalid type!"

        # Differentiate input
        if forced_validate:
            source_demuxer is None and logger.critical(
                "Forcefully passing validation test for given source!"
            )
            self.__source = source
        elif os.path.isfile(source):
            self.__source = os.path.abspath(source)
        elif is_valid_image_seq(
            self.__ffmpeg, source=source, verbose=self.__verbose_logs
        ):
            self.__source = source
            self.__contains_images = True
        elif is_valid_url(self.__ffmpeg, url=source, verbose=self.__verbose_logs):
            self.__source = source
        else:
            logger.error("`source` value is unusable or unsupported!")
            # discard the value otherwise
            raise ValueError("Input source is invalid. Aborting!")
        # format command
        if self.__sourcer_params:
            # handle additional params separately
            meta_cmd = (
                [self.__ffmpeg]
                + (["-hide_banner"] if not self.__verbose_logs else [])
                + ["-t", "0.0001"]
                + self.__ffmpeg_prefixes
                + (["-f", source_demuxer] if source_demuxer else [])
                + ["-i", source]
                + dict2Args(self.__sourcer_params)
                + ["-f", "null", "-"]
            )
        else:
            meta_cmd = (
                [self.__ffmpeg]
                + (["-hide_banner"] if not self.__verbose_logs else [])
                + self.__ffmpeg_prefixes
                + (["-f", source_demuxer] if source_demuxer else [])
                + ["-i", source]
            )
        # extract metadata, decode, and filter
        metadata = (
            check_sp_output(
                meta_cmd,
                force_retrieve_stderr=True,
            )
            .decode("utf-8")
            .strip()
        )
        # separate input and output metadata (if available)
        if "Output #" in metadata:
            (metadata, self.__metadata_output) = metadata.split("Output #")
        # return metadata based on params
        return metadata

    def __extract_video_bitrate(self, default_stream=0):
        """
        This Internal method parses default video-stream bitrate from metadata.

        Parameters:
            default_stream (int): selects specific video-stream in case of multiple ones.

        **Returns:** Default Video bitrate as string value.
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
                r",\s[0-9]+\s\w\w[\/]s", selected_stream.strip()
            )
            if len(filtered_bitrate):
                default_video_bitrate = filtered_bitrate[0].split(" ")[1:3]
                final_bitrate = "{}{}".format(
                    int(default_video_bitrate[0].strip()),
                    "k" if (default_video_bitrate[1].strip().startswith("k")) else "M",
                )
                return final_bitrate
        return ""

    def __extract_video_decoder(self, default_stream=0):
        """
        This Internal method parses default video-stream decoder from metadata.

        Parameters:
            default_stream (int): selects specific video-stream in case of multiple ones.

        **Returns:** Default Video decoder as string value.
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
            if filtered_pixfmt:
                return filtered_pixfmt[0].split(" ")[-1]
        return ""

    def __extract_video_pixfmt(self, default_stream=0, extract_output=False):
        """
        This Internal method parses default video-stream pixel-format from metadata.

        Parameters:
            default_stream (int): selects specific video-stream in case of multiple ones.

        **Returns:** Default Video pixel-format as string value.
        """
        identifiers = ["Video:", "Stream #"]
        meta_text = (
            [
                line.strip()
                for line in self.__ffsp_output.split("\n")
                if all(x in line for x in identifiers)
            ]
            if not extract_output
            else [
                line.strip()
                for line in self.__metadata_output.split("\n")
                if all(x in line for x in identifiers)
            ]
        )
        if meta_text:
            selected_stream = meta_text[
                default_stream
                if default_stream > 0 and default_stream < len(meta_text)
                else 0
            ]
            filtered_pixfmt = re.findall(
                r",\s[a-z][a-z0-9_-]*", selected_stream.strip()
            )
            if filtered_pixfmt:
                return filtered_pixfmt[0].split(" ")[-1]
        return ""

    def __extract_audio_bitrate_nd_samplerate(self, default_stream=0):
        """
        This Internal method parses default audio-stream bitrate and sample-rate from metadata.

        Parameters:
            default_stream (int): selects specific audio-stream in case of multiple ones.

        **Returns:** Default Audio-stream bitrate and sample-rate as string value.
        """
        identifiers = ["Audio:", "Stream #"]
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
            filtered_audio_bitrate = re.findall(
                r"fltp,\s[0-9]+\s\w\w[\/]s", selected_stream.strip()
            )
            filtered_audio_samplerate = re.findall(
                r",\s[0-9]+\sHz", selected_stream.strip()
            )
            # get audio bitrate metadata
            if filtered_audio_bitrate:
                filtered = filtered_audio_bitrate[0].split(" ")[1:3]
                result["bitrate"] = "{}{}".format(
                    int(filtered[0].strip()),
                    "k" if (filtered[1].strip().startswith("k")) else "M",
                )
            else:
                result["bitrate"] = ""
            # get audio samplerate metadata
            result["samplerate"] = (
                filtered_audio_samplerate[0].split(", ")[1]
                if filtered_audio_samplerate
                else ""
            )
        return result if result and (len(result) == 2) else {}

    def __extract_resolution_framerate(self, default_stream=0, extract_output=False):
        """
        This Internal method parses default video-stream resolution and framerate from metadata.

        Parameters:
            default_stream (int): selects specific audio-stream in case of multiple ones.
            extract_output (bool): Whether to extract from output(if true) or input(if false) stream?

        **Returns:** Default Video resolution and framerate as dictionary value.
        """
        identifiers = ["Video:", "Stream #"]
        # use output metadata if available
        meta_text = (
            [
                line.strip()
                for line in self.__ffsp_output.split("\n")
                if all(x in line for x in identifiers)
            ]
            if not extract_output
            else [
                line.strip()
                for line in self.__metadata_output.split("\n")
                if all(x in line for x in identifiers)
            ]
        )
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
            filtered_tbr = re.findall(r"\d+(?:\.\d+)?\stbr", selected_stream.strip())

            # extract framerate metadata
            if filtered_framerate:
                # calculate actual framerate
                result["framerate"] = float(
                    re.findall(r"[\d\.\d]+", filtered_framerate[0])[0]
                )
            elif filtered_tbr:
                # guess from TBR(if fps unavailable)
                result["framerate"] = float(
                    re.findall(r"[\d\.\d]+", filtered_tbr[0])[0]
                )

            # extract resolution metadata
            if filtered_resolution:
                result["resolution"] = [int(x) for x in filtered_resolution[0]]

        return result if result and (len(result) == 2) else {}

    def __extract_duration(self, inseconds=True):
        """
        This Internal method parses stream duration from metadata.

        Parameters:
            inseconds (bool): whether to parse time in second(s) or `HH::mm::ss`?

        **Returns:** Default Stream duration as string value.
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
                        float(x) * 60**i
                        for i, x in enumerate(reversed(t_duration[0].split(":")))
                    )
                    if inseconds
                    else t_duration
                )
        return 0
