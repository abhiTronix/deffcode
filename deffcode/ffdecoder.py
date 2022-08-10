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
import numpy as np
import subprocess as sp
from collections import OrderedDict

# import utils packages
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
    """
    > FFdecoder API compiles and executes the FFmpeg pipeline inside a subprocess pipe for generating real-time, low-overhead, lightning fast video frames
    with robust error-handling in python 🎞️⚡

    FFdecoder API implements a **standalone highly-extensible wrapper around [FFmpeg](https://ffmpeg.org/)** multimedia framework that provides complete
    control over the underline pipeline including **access to almost any FFmpeg specification thinkable** such as framerate, resolution, hardware decoder(s),
    complex filter(s), and pixel format(s) that are readily supported by all well known Computer Vision libraries.

    FFdecoder API **compiles its FFmpeg pipeline** by processing input Video Source metadata and User-defined options, and **runs it inside a
    [`subprocess`](https://docs.python.org/3/library/subprocess.html) pipe** concurrently with the main thread, while extracting output dataframes(1D arrays)
    into a Numpy buffer. These dataframes are consecutively grabbed from the buffer and decoded into ==[24-bit RGB](https://en.wikipedia.org/wiki/List_of_monochrome_and_RGB_color_formats#24-bit_RGB) _(default)_
    [`ndarray`](https://numpy.org/doc/stable/reference/arrays.ndarray.html#the-n-dimensional-array-ndarray) 3D frames== that are readily available
    through its [`generateFrame()`](#deffcode.ffdecoder.FFdecoder.generateFrame) method.

    FFdecoder API **employs [Sourcer API](../../reference/sourcer) at its backend** for gathering, processing, and validating metadata of all
    multimedia streams available in the given source for formulating/compiling its default FFmpeg pipeline. This metadata information is also
    available as a JSON string with its [`metadata`](#deffcode.ffdecoder.FFdecoder.metadata) property object and can be updated as desired.

    FFdecoder API **supports a wide-ranging media stream** as input source such as USB/Virtual/IP Camera Feed, Multimedia video file,
    Screen Capture, Image Sequence, Network protocols _(such as HTTP(s), RTP/RSTP, etc.)_, so on and so forth.

    Furthermore, FFdecoder API maintains the **standard [OpenCV-Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) _(Python API for OpenCV)_ coding syntax**, thereby making it even easier to
    integrate this API in any Computer Vision application.

    !!! example "For usage examples, kindly refer our **[Basic Recipes :cake:](../../recipes/basic)** and **[Advanced Recipes :croissant:](../../recipes/advanced)**"

    !!! info "FFdecoder API parameters are explained [here ➶](params/)"
    """

    def __init__(
        self,
        source,
        source_demuxer=None,
        frame_format=None,
        custom_ffmpeg="",
        verbose=False,
        **ffparams
    ):
        """
        This constructor method initializes the object state and attributes of the FFdecoder Class.

        Parameters:
            source (str): defines the input(`-i`) source filename/URL/device-name/device-path.
            source_demuxer (str): specifies the demuxer(`-f`) for the input source.
            frame_format (str): sets pixel format(`-pix_fmt`) of the decoded frames.
            custom_ffmpeg (str): assigns the location of custom path/directory for custom FFmpeg executable.
            verbose (bool): enables/disables verbose.
            ffparams (dict): provides the flexibility to control supported internal and FFmpeg parameters.
        """

        # enable verbose if specified
        self.__verbose_logs = (
            verbose if (verbose and isinstance(verbose, bool)) else False
        )

        # define whether initializing
        self.__initializing = True

        # define frame pixel-format for decoded frames
        self.__frame_format = (
            frame_format.strip() if isinstance(frame_format, str) else None
        )

        # handles user-defined parameters
        self.__extra_params = {}

        # handle process to be frames written
        self.__process = None

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
            if not (v is None) and not isinstance(v, (dict, list, int, float, tuple))
            else v
            for k, v in ffparams.items()
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

        # define dict to store user-defined parameters
        self.__user_metadata = {}
        # extract and assign source metadata as dict
        self.__source_metadata = (
            Sourcer(
                source=source,
                source_demuxer=source_demuxer,
                verbose=verbose,
                custom_ffmpeg=custom_ffmpeg if isinstance(custom_ffmpeg, str) else "",
                **sourcer_params
            )
            .probe_stream(default_stream_indexes=default_stream_indexes)
            .retrieve_metadata()
        )
        # add dummy value for `output_frames_pixfmt` source metadata
        self.__source_metadata["output_frames_pixfmt"] = "unknown"

        # handle valid FFmpeg assets location
        self.__ffmpeg = self.__source_metadata["ffmpeg_binary_path"]

        # handle pass-through audio mode works in conjunction with WriteGear [TODO]
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
            and self.__passthrough_mode  # [TODO]
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
                "Unable to find any usable video stream in the given source!"
            )
        # store as metadata
        self.__source_metadata["ffdecoder_operational_mode"] = self.__supported_opmodes[
            self.__opmode
        ]
        # and log it
        self.__verbose_logs and logger.critical(
            "Activating {} Mode of Operation.".format(
                self.__supported_opmodes[self.__opmode]
            )
        )

        # handle user-defined framerate
        __framerate = self.__extra_params.pop("-framerate", 0.0)
        if not (__framerate is None) and isinstance(__framerate, (float, int)):
            self.__inputframerate = float(__framerate) if __framerate > 0.0 else 0.0
        else:
            # warn if wrong type
            logger.warning(
                "Discarding invalid `-framerate` value of wrong type `{}`!".format(
                    type(__framerate).__name__
                )
            )
            # reset to default
            self.__inputframerate = 0.0

        # FFmpeg parameter `-s` is unsupported
        if not (self.__extra_params.pop("-s", None) is None):
            logger.warning(
                "Discarding user-defined `-s` FFmpeg parameter as it can only be assigned with `-custom_resolution` attribute! Read docs for more details."
            )
        # handle user defined decoded frame resolution(must be a tuple or list)
        self.__custom_resolution = self.__extra_params.pop("-custom_resolution", None)
        if not (self.__custom_resolution is None) and (
            not isinstance(self.__custom_resolution, (list, tuple))
            or len(self.__custom_resolution) != 2
        ):
            # log it
            logger.warning(
                "Discarding invalid `-custom_resolution` value: `{}`!".format(
                    self.__custom_resolution
                )
            )
            # reset improper values
            self.__custom_resolution = None

        # handle user defined ffmpeg pre-headers(parameters such as `-re`) parameters (must be a list)
        self.__ffmpeg_prefixes = self.__extra_params.pop("-ffprefixes", [])
        if not isinstance(self.__ffmpeg_prefixes, list):
            # log it
            logger.warning(
                "Discarding invalid `-ffprefixes` value of wrong type: `{}`!".format(
                    type(self.__ffmpeg_prefixes).__name__
                )
            )
            # reset improper values
            self.__ffmpeg_prefixes = []

    def formulate(self):

        """
        This method formulates all necessary FFmpeg pipeline arguments and executes it inside the FFmpeg `subprocess` pipe.

        **Returns:** A reference to the FFdecoder class object.
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

            # dynamically calculate default raw-frames pixel format(if not assigned by user).
            self.__ff_pixfmt_metadata = get_supported_pixfmts(self.__ffmpeg)
            supported_pixfmts = [fmts[0] for fmts in self.__ff_pixfmt_metadata]
            default_pixfmt = (
                "rgb24"
                if "rgb24" in supported_pixfmts
                else self.__source_metadata["source_video_pixfmt"]
            )
            # assigning `-pix_fmt` parameter cannot be assigned directly
            if "-pix_fmt" in self.__extra_params:
                logger.warning(
                    "Discarding user-defined `-pix_fmt` value as it can only be assigned with `frame_format` parameter! Read docs for more details."
                )
                self.__extra_params.pop("-pix_fmt", None)
            # assign output raw-frames pixel format
            if (
                "output_frames_pixfmt" in self.__source_metadata
                and self.__source_metadata["output_frames_pixfmt"] in supported_pixfmts
            ):
                # check if manually defined via `metadata` property object
                # assign if valid and supported
                output_params["-pix_fmt"] = self.__source_metadata[
                    "output_frames_pixfmt"
                ].strip()
            elif (
                not (self.__frame_format is None)
                and self.__frame_format in supported_pixfmts
            ):
                # check if assigned via `frame_format` parameter
                # assign if valid and supported
                output_params["-pix_fmt"] = self.__frame_format.strip()
            else:
                # reset to default if not supported
                not (self.__frame_format is None) and logger.critical(
                    "Provided FFmpeg does not support `{}` pixel format(pix_fmt). Switching to default `{}`!".format(
                        self.__frame_format, "rgb24"
                    )
                )
                output_params["-pix_fmt"] = default_pixfmt

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
                # change dtype
                self.__raw_frame_dtype = np.dtype("u1")
            # assign to global parameter
            self.__raw_frame_pixfmt = output_params["-pix_fmt"]
            # also store as metadata
            self.__source_metadata["output_frames_pixfmt"] = output_params["-pix_fmt"]

            # handle raw-frame size
            if not (self.__custom_resolution is None):
                # assign if assigned by user
                self.__raw_frame_resolution = self.__custom_resolution
            elif (
                self.__source_metadata["source_video_resolution"]
                and len(self.__source_metadata["source_video_resolution"]) == 2
            ):
                # calculate raw-frame resolution/dimensions based on source (if not assigned by user).
                self.__raw_frame_resolution = self.__source_metadata[
                    "source_video_resolution"
                ]
            else:
                # otherwise raise error
                raise RuntimeError(
                    "Invalid `source_video_resolution` metadata value detected!"
                )
            # add to pipeline
            dimensions = "{}x{}".format(
                self.__raw_frame_resolution[0], self.__raw_frame_resolution[1]
            )
            output_params["-s"] = str(dimensions)

            # dynamically calculate raw-frame framerate based on source (if not assigned by user).
            if self.__inputframerate > 0.0:
                # assign if assigned by user
                output_params["-framerate"] = str(self.__inputframerate)
            elif self.__source_metadata["source_video_framerate"] > 0.0:
                # calculate raw-frame framerate based on source
                output_params["-framerate"] = str(
                    self.__source_metadata["source_video_framerate"]
                )
            else:
                # otherwise raise error
                raise RuntimeError(
                    "Invalid `source_video_framerate` metadata value detected!"
                )

            # add rest to output parameters
            output_params.update(self.__extra_params)

            # dynamically calculate raw-frame numbers based on source (if not assigned by user).
            # TODO Added support for `-re -stream_loop` and `-loop`
            if "-frames:v" in input_params:
                self.__raw_frame_num = input_params["-frames:v"]
            elif self.__source_metadata["approx_video_nframes"]:
                self.__raw_frame_num = self.__source_metadata["approx_video_nframes"]
            else:
                self.__raw_frame_num = None
                # log that number of frames are unknown
                self.__verbose_logs and logger.info(
                    "Live/Network Stream detected! Number of frames in given source are not known."
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
        This Internal method to fetch next dataframes(1D arrays) from `subprocess` pipe's standard output(`stdout`) into a Numpy buffer.
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
        This Internal method grabs and decodes next 3D `ndarray` video-frame from the buffer.
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
        elif self.__raw_frame_pixfmt == "yuv444p":
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
        This method returns a [Generator function](https://wiki.python.org/moin/Generators)
        _(also an Iterator using `next()`)_ of video frames, grabbed continuously from the buffer.
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
        Handles entry with the `with` statement. See [PEP343 -- The 'with' statement'](https://peps.python.org/pep-0343/).

        **Returns:** Output of `formulate()` method.
        """
        return self.formulate()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handles exit with the `with` statement. See [PEP343 -- The 'with' statement'](https://peps.python.org/pep-0343/).
        """
        self.terminate()

    @property
    def metadata(self):
        """
        A property object that dumps metadata information as JSON string.

        **Returns:** Metadata as JSON string.
        """
        # import dependency
        import json

        # return complete (source+user-defined) metadata as JSON string
        return json.dumps({**self.__source_metadata, **self.__user_metadata}, indent=2)

    @metadata.setter
    def metadata(self, value):
        """
        A property object that updates metadata information with user-defined dictionary.

        Parameters:
            value (dict): User-defined dictionary.
        """
        # check if value dict type
        if value and isinstance(value, dict):
            # log it
            self.__verbose_logs and logger.info("Updating Metadata...")
            # extract any source metadata keys
            default_keys = set(value).intersection(self.__source_metadata)
            # iterate over source metadata keys and sanitize it
            for key in default_keys or []:
                if key == "source":
                    # `source` metadata value cannot be altered
                    logger.warning(
                        "`source` metadata value cannot be altered. Discarding!"
                    )
                elif isinstance(value[key], type(self.__source_metadata[key])):
                    # check if correct datatype as original
                    # update source metadata if valid
                    self.__source_metadata.update(value)
                    continue
                else:
                    # otherwise discard and log it
                    logger.warning(
                        "Manually assigned `{}` metadata value is invalid type. Discarding!"
                    ).format(key)
                # delete invalid key
                del value[key]
            # There is no concept of a tuple in the JSON format.
            # Python's `json` module converts Python tuples to JSON lists
            # because that's the closest thing in JSON to a tuple.
            any(isinstance(value[x], tuple) for x in value) and logger.warning(
                "All TUPLE metadata values will be converted to LIST datatype. Read docs for more details."
            )
            # update user-defined metadata
            self.__user_metadata.update(value)
        else:
            # otherwise raise error
            raise ValueError("Invalid datatype metadata assigned. Aborting!")

    def __launch_FFdecoderline(self, input_params, output_params):

        """
        This Internal method executes FFmpeg pipeline arguments inside a `subprocess` pipe in a new process.

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
            + (["-hide_banner"] if not self.__verbose_logs else [])
            + self.__ffmpeg_prefixes
            + input_parameters
            + (
                ["-f", self.__source_metadata["source_demuxer"]]
                if ("source_demuxer" in self.__source_metadata.keys())
                else []
            )
            + ["-i", self.__source_metadata["source"]]
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
        Safely terminates all processes.
        """
        # signal we are closing
        self.__verbose_logs and logger.debug("Terminating FFdecoder Pipeline...")
        self.__terminate_stream = True
        # check if no process was initiated at first place
        if self.__process is None or not (self.__process.poll() is None):
            logger.warning("Pipeline already terminated!")
            return
        # Attempt to close pipeline.
        # close `stdin` output
        self.__process.stdin and self.__process.stdin.close()
        # close `stdout` output
        self.__process.stdout and self.__process.stdout.close()
        # wait if still process is still processing some information
        if self.__process.poll() is None:
            self.__process.terminate()
        self.__process.wait()
        self.__process = None
        self.__verbose_logs and logger.debug(
            "FFdecoder Pipeline terminated successfully"
        )
