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
import logging
import json
import numpy as np
import subprocess as sp
from collections import OrderedDict

# import helper packages
from .utils import dict2Args, logger_handler
from .sourcer import Sourcer
from .ffhelper import (
    get_supported_pixfmts,
    get_supported_vdecoders,
)

# define FFdecoder logger
logger = logging.getLogger("FFdecoder")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


class FFdecoder:
    """ """

    def __init__(
        self, source, frame_format=None, custom_ffmpeg="", verbose=False, **extraparams
    ):
        """
        This constructor method initializes the object state and attributes of the FFdecoder.

        Parameters:
            source (str): defines the default input source.
            frame_format (str): sets pixel format(-pix_fmt) of the decoded frames.
            custom_ffmpeg (str): assigns the location of custom path/directory for custom FFmpeg executable.
            verbose (bool): enables/disables verbose.
            extraparams (dict): provides the flexibility to control supported internal parameters and FFmpeg properties.
        """

        # enable verbose if specified
        self.__verbose_logs = (
            verbose if (verbose and isinstance(verbose, bool)) else False
        )

        # define whether initializing
        self.__initializing = True

        # define frame pixel-format for decoded frames
        self.__frame_format = frame_format

        # handles user-defined parameters
        self.__extra_params = {}

        # handle process to be frames written
        self.__process = None

        # handle valid FFmpeg assets location
        self.__ffmpeg = ""

        # handle exclusive metadata
        self.__ff_pixfmt_metadata = None  # metadata
        self.__raw_frame_num = None  # raw-frame number
        self.__raw_frame_pixfmt = None  # raw-frame pixformat
        self.__raw_frame_dtype = None  # raw-frame dtype
        self.__raw_frame_depth = None  # raw-frame depth
        self.__raw_frame_resolution = None  # raw-frame resolution/dimension

        # define supported mode of operation
        self.__supported_opmodes = {
            "av": "Audio-Video",  # audio is only for pass-through, not really for audio decoding yet.
            "vo": "Video-Only",
            "imgseq": "Image-Sequence",
            # "ao":"Audio-Only", # reserved for future
        }
        # operation mode variable
        self.__opmode = None

        # handle termination
        self.__terminate_stream = False

        # cleans and reformat user-defined parameters
        self.__extra_params = {
            str(k).strip(): str(v).strip()
            if not isinstance(v, (dict, list, int, float))
            else v
            for k, v in extraparams.items()
        }

        # handle custom Sourcer API params
        sourcer_params = self.__extra_params.pop("-custom_sourcer_params", {})
        # reset improper values
        sourcer_params = {} if not isinstance(sourcer_params, dict) else sourcer_params

        # pass parameter(if specified) to Sourcer API, specifying where to save the downloaded FFmpeg Static
        # assets on Windows(if specified)
        sourcer_params["-ffmpeg_download_path"] = self.__extra_params.pop(
            "-ffmpeg_download_path", ""
        )

        # handle video and audio stream indexes in case of multiple ones.
        default_stream_indexes = self.__extra_params.pop(
            "-default_stream_indexes", (0, 0)
        )
        # reset improper values
        default_stream_indexes = (
            (0, 0)
            if not isinstance(default_stream_indexes, (list, tuple))
            else default_stream_indexes
        )

        # extract and assign source metadata as dict
        self.__source_metadata = (
            Sourcer(
                source=source,
                verbose=verbose,
                ffmpeg_path=self.__ffmpeg,
                **sourcer_params
            )
            .probe_stream(default_stream_indexes=default_stream_indexes)
            .retrieve_metadata()
        )

        # get valid ffmpeg path
        self.__ffmpeg = self.__source_metadata["ffmpeg_binary_path"]

        # handle pass-through audio mode works in conjunction with WriteGear [WIP]
        self.__passthrough_mode = self.__extra_params.pop("-passthrough_audio", False)
        if not (isinstance(self.__passthrough_mode, bool)):
            self.__passthrough_mode = False
        # handle mode of operation
        if self.__source_metadata["source_has_image_sequence"]:
            # image-sequence mode
            self.__opmode = "imgseq"
        elif (
            self.__source_metadata[
                "source_has_video"
            ]  # audio is only for pass-through, not really for audio decoding yet.
            and self.__source_metadata["source_has_audio"]
            and self.__passthrough_mode  # [WIP]
        ):
            self.__opmode = "av"
        # elif __defop_mode == "ao" and self.__source_metadata.contains_audio: # [TODO]
        #    self.__opmode = "ao"
        elif self.__source_metadata["source_has_video"]:
            # video-only mode
            self.__opmode = "vo"
        else:
            # raise if unknown mode
            raise ValueError(
                "Unable to find suitable/usable video stream in the given source!"
            )
        # store as metadata
        self.__source_metadata["operational_mode"] = self.__supported_opmodes[
            self.__opmode
        ]
        # and log it
        self.__verbose_logs and logger.critical(
            "Activating {} Mode of Operation.".format(
                self.__supported_opmodes[self.__opmode]
            )
        )

        # handle user-defined framerate
        self.__inputframerate = self.__extra_params.pop("-framerate", 0.0)
        if (
            isinstance(self.__inputframerate, (float, int))
            and self.__inputframerate > 0.0
        ):
            # must be float
            self.__inputframerate = float(self.__inputframerate)
        else:
            # reset improper values
            self.__inputframerate = 0.0

        # FFmpeg parameter `-s` is unsupported
        if not (self.__extra_params.pop("-s", None) is None):
            logger.warning(
                "Discarding user-defined `-s` FFmpeg parameter as it can only be assigned with `-custom_resolution`!"
            )
        # handle user defined decoded frame resolution(must be a tuple or list)
        self.__custom_resolution = self.__extra_params.pop("-custom_resolution", None)
        if self.__custom_resolution is None or not (
            isinstance(self.__custom_resolution, (list, tuple))
            and len(self.__custom_resolution) == 2
        ):
            # reset improper values
            self.__custom_resolution = None

        # handle user defined ffmpeg pre-headers(parameters such as `-re`) parameters (must be a list)
        self.__ffmpeg_prefixes = self.__extra_params.pop("-ffprefixes", [])
        if not isinstance(self.__ffmpeg_prefixes, list):
            # reset improper values
            self.__ffmpeg_prefixes = []

        # handle user defined ffmpeg post-headers(parameters before `-i`) parameters (must be a list)
        self.__ffmpeg_postfixes = self.__extra_params.pop("-ffpostfixes", [])
        if not isinstance(self.__ffmpeg_postfixes, list):
            # reset improper values
            self.__ffmpeg_postfixes = []

    def formulate(self):

        """
        Formulates all necessary FFmpeg parameters command and Launches FFmpeg Pipeline using subprocess module.
        """
        # assign values to class variables on first run
        if self.__initializing:
            # prepare parameter dict
            input_params = OrderedDict()
            output_params = OrderedDict()

            # dynamically pre-assign a default video-decoder (if not assigned by user).
            supported_vdecodecs = get_supported_vdecoders(self.__ffmpeg)
            default_vdecodec = (
                self.__source_metadata["source_video_decoder"]
                if self.__source_metadata["source_video_decoder"] in supported_vdecodecs
                else "unknown"
            )
            if "-c:v" in self.__extra_params:
                self.__extra_params["-vcodec"] = self.__extra_params.pop(
                    "-c:v", default_vdecodec
                )
            # handle image sequence separately
            if self.__opmode == "imgseq":
                # -vcodec is discarded by default
                # (This is correct or maybe -vcodec required in some unknown case) [TODO]
                self.__extra_params.pop("-vcodec", None)
            elif (
                "-vcodec" in self.__extra_params
                and self.__extra_params["-vcodec"] is None
            ):
                # special case when -vcodec is not needed intentionally
                self.__extra_params.pop("-vcodec", None)
            else:
                # assign video decoder selected here.
                if not "-vcodec" in self.__extra_params:
                    input_params["-vcodec"] = default_vdecodec
                else:
                    input_params["-vcodec"] = self.__extra_params.pop(
                        "-vcodec", default_vdecodec
                    )
                if (
                    default_vdecodec != "unknown"
                    and not input_params["-vcodec"] in supported_vdecodecs
                ):
                    # reset to default if not supported
                    logger.warning(
                        "Provided FFmpeg does not support `{}` video decoder. Switching to default supported `{}` decoder!".format(
                            input_params["-vcodec"], default_vdecodec
                        )
                    )
                    input_params["-vcodec"] = default_vdecodec
                # raise error if not valid decoder found
                if not input_params["-vcodec"] in supported_vdecodecs:
                    raise RuntimeError(
                        "Provided FFmpeg does not support any known usable video-decoders."
                        " Either define your own manually or switch to another FFmpeg binaries(if available)."
                    )

            # handle user-defined number of frames.
            if "-vframes" in self.__extra_params:
                self.__extra_params["-frames:v"] = self.__extra_params.pop(
                    "-vframes", None
                )
            if "-frames:v" in self.__extra_params:
                value = self.__extra_params.pop("-frames:v", None)
                if not (value is None) and value > 0:
                    output_params["-frames:v"] = value

            # dynamically calculate raw-frame pixel format based on source (if not assigned by user).
            self.__ff_pixfmt_metadata = get_supported_pixfmts(self.__ffmpeg)
            supported_pixfmts = [fmts[0] for fmts in self.__ff_pixfmt_metadata]
            default_pixfmt = (
                "rgb24"
                if "rgb24" in supported_pixfmts
                else self.__source_metadata["source_video_pixfmt"]
            )
            if "-pix_fmt" in self.__extra_params:
                logger.warning(
                    "Discarding user-defined `-pix_fmt` value as it can only be assigned with `frame_format` parameter!"
                )
                self.__extra_params.pop("-pix_fmt", None)
            if (
                self.__frame_format is None
                or not self.__frame_format in supported_pixfmts
            ):
                # reset to default if not supported
                not (self.__frame_format is None) and logger.critical(
                    "Provided FFmpeg does not support `{}` pixel format(pix_fmt). Switching to default `{}`!".format(
                        self.__frame_format, "rgb24"
                    )
                )
                output_params["-pix_fmt"] = default_pixfmt
            else:
                output_params["-pix_fmt"] = self.__frame_format

            # dynamically calculate raw-frame dtype based on pix format selected
            frames_pixfmt = output_params["-pix_fmt"]
            (self.__raw_frame_depth, rawframesbpp) = [
                (int(x[1]), int(x[2]))
                for x in self.__ff_pixfmt_metadata
                if x[0] == frames_pixfmt
            ][0]
            raw_bit_per_component = rawframesbpp // self.__raw_frame_depth
            if raw_bit_per_component in [4, 8]:
                self.__raw_frame_dtype = np.dtype("u1")
            elif raw_bit_per_component == 16:
                if frames_pixfmt.endswith("le"):
                    self.__raw_frame_dtype = np.dtype("<u2")
                elif frames_pixfmt.endswith("be"):
                    self.__raw_frame_dtype = np.dtype(">u2")
                else:
                    pass
            else:
                # reset to default if not supported
                logger.critical(
                    "Given `frame_format` value: {} is not supported by FFdecoder. Switching to default `{}`!".format(
                        frames_pixfmt, "rgb24"
                    )
                )
                output_params["-pix_fmt"] = default_pixfmt
                self.__raw_frame_dtype = np.dtype("u1")
            self.__raw_frame_pixfmt = output_params["-pix_fmt"]

            # dynamically calculate raw-frame resolution/dimensions based on source (if not assigned by user).
            self.__raw_frame_resolution = (
                self.__custom_resolution
                if not (self.__custom_resolution is None)
                else self.__source_metadata["source_video_resolution"]
            )
            dimensions = "{}x{}".format(
                self.__raw_frame_resolution[0], self.__raw_frame_resolution[1]
            )  # apply if defined
            output_params["-s"] = str(dimensions)

            # dynamically calculate raw-frame frame-rate based on source (if not assigned by user).
            framerate = (
                self.__inputframerate
                if self.__inputframerate > 0.0
                else self.__source_metadata["source_video_framerate"]
            )
            output_params["-framerate"] = str(framerate)

            # add rest to output parameters
            output_params.update(self.__extra_params)

            # dynamically calculate raw-frame numbers based on source (if not assigned by user).
            if "-frames:v" in input_params:
                self.__raw_frame_num = input_params["-frames:v"]
            elif self.__source_metadata["approx_video_nframes"]:
                self.__raw_frame_num = self.__source_metadata["approx_video_nframes"]
            else:
                self.__raw_frame_num = None
                # log that number of frames are unknown
                self.__verbose_logs and logger.info(
                    "Live/Network Stream detected! Number of frames for given source is unknown."
                )

            # compose the Pipeline using formulated FFmpeg parameters
            self.__launch_FFdecoderline(input_params, output_params)

            # inform the initialization is completed
            self.__initializing = False
        else:
            # warn if pipeline is recreated
            logger.error("This pipeline is already created and running!")
        return self

    def __fetchNextfromPipeline(self):
        """
        Internal method to fetch next dataframe(in bytes) from FFmpeg Pipeline.
        """
        assert not (
            self.__process is None
        ), "Pipeline is not running! Check if you called `create()` method."

        # formulated raw frame size
        raw_frame_size = (
            self.__raw_frame_depth
            * self.__raw_frame_resolution[0]
            * self.__raw_frame_resolution[1]
        )
        # next dataframe as numpy ndarray
        nparray = None
        try:
            # read bytes frames from buffer
            nparray = np.frombuffer(
                self.__process.stdout.read(
                    raw_frame_size * self.__raw_frame_dtype.itemsize
                ),
                dtype=self.__raw_frame_dtype,
            )
        except Exception as e:
            raise RuntimeError("Frame fetching failed with error: {}".format(str(e)))
        return (
            nparray
            if not (nparray is None) and len(nparray) == raw_frame_size
            else None
        )

    def __fetchNextFrame(self):
        """
        Internal method to reconstruct next video-frame(`ndarray`) from fetched dataframe.
        """
        # Read next and reconstruct as numpy array
        frame = self.__fetchNextfromPipeline()
        # check if empty
        if frame is None:
            return frame
        elif self.__raw_frame_pixfmt.startswith("gray"):
            # reconstruct gray frames
            frame = frame.reshape(
                (
                    self.__raw_frame_resolution[1],
                    self.__raw_frame_resolution[0],
                    self.__raw_frame_depth,
                )
            )[:, :, 0]
        elif self.__raw_frame_pixfmt.startswith(
            "yuv"
        ) and self.__raw_frame_pixfmt.startswith("444p"):
            # reconstruct exclusive frames
            frame = frame.reshape(
                (
                    self.__raw_frame_depth,
                    self.__raw_frame_resolution[1],
                    self.__raw_frame_resolution[0],
                )
            ).transpose((1, 2, 0))
        else:
            # reconstruct default frames
            frame = frame.reshape(
                (
                    self.__raw_frame_resolution[1],
                    self.__raw_frame_resolution[0],
                    self.__raw_frame_depth,
                )
            )
        # return frame
        return frame

    def generateFrame(self):
        """
        A python Generator function which can also works as an Iterator(using `next()`) for extracting
        video-frames(`ndarray`) at rapid pace.
        """
        if self.__raw_frame_num is None or not self.__raw_frame_num:
            while not self.__terminate_stream:
                frame = self.__fetchNextFrame()
                if frame is None:
                    self.__terminate_stream = True
                    continue
                yield frame
        else:
            for _ in range(self.__raw_frame_num):
                frame = self.__fetchNextFrame()
                if frame is None:
                    self.__terminate_stream = True
                    break
                yield frame

    def __enter__(self):
        """
        Handles entry
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles exit
        """
        self.close()

    @property
    def metadata(self):
        """
        A property object that dumps Source metadata dict as JSON for pretty printing. As well as can be used to update source metadata with user-defined dictionary.

        **Returns:** A [`json.dumps`](https://docs.python.org/3/library/json.html#json.dumps) output.
        """
        return json.dumps(self.__source_metadata, indent=2)

    @metadata.setter
    def metadata(self, value):
        """
        A property object that updates source metadata with user-defined dictionary.

        Parameters:
            value (dict): User-defined dictionary.
        """
        self.__verbose_logs and logger.info("Updating Metadata...")
        if value and isinstance(value, dict):
            self.__source_metadata.update(value)
        else:
            raise ValueError("Invalid value specified.")

    def __launch_FFdecoderline(self, input_params, output_params):

        """
        An Internal method that launches FFmpeg Pipeline using subprocess module, that pipelines dataframes(in bytes) to `stdout`.

        Parameters:
            input_params (dict): Input FFmpeg parameters
            output_params (dict): Output FFmpeg parameters
        """
        # convert input parameters to list
        input_parameters = dict2Args(input_params)

        # convert output parameters to list
        output_parameters = dict2Args(output_params)

        # format command
        cmd = (
            [self.__ffmpeg]
            + self.__ffmpeg_prefixes
            + input_parameters
            + self.__ffmpeg_postfixes
            + ["-i"]
            + [self.__source_metadata["source"]]
            + output_parameters
            + ["-f", "rawvideo", "-"]
        )
        # assign value to class variable
        _cmd = " ".join(cmd)
        # compose the FFmpeg process
        if self.__verbose_logs:
            logger.debug("Executing FFmpeg command: `{}`".format(_cmd))
            # In debugging mode
            self.__process = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=None)
        else:
            # In silent mode
            self.__process = sp.Popen(
                cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.DEVNULL
            )

    def terminate(self):
        """
        Safely terminate all processes.
        """
        # signal we are closing
        self.__verbose_logs and logger.debug("Terminating FFdecoder Pipeline...")
        self.__terminate_stream = True
        # Attempt to close pipeline.
        if self.__process is None or not (self.__process.poll() is None):
            return  # no process was initiated at first place
        # close `stdin` output
        self.__process.stdin and self.__process.stdin.close()
        # close `stdout` output
        self.__process.stdout and self.__process.stdout.close()
        # wait if still process is still processing some information
        self.__process.wait()
        self.__process = None
