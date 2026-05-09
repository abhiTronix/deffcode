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
import platform
import re
import subprocess as sp
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm

# import utils packages
from .utils import delete_file_safe, logger_handler

# define logger
logger = logging.getLogger("FFhelper")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)

# set default timeout for subprocesses
MAX_TIMEOUT_SUBPROCESS: float = float(os.getenv("MAX_TIMEOUT_SUBPROCESS", 10.0))
# set grace period (seconds) between SIGTERM and SIGKILL when terminating
# a timed-out subprocess. Allows FFmpeg to flush buffers and release hardware
# resources before being force-killed.
TERMINATE_TIMEOUT_SUBPROCESS: float = float(
    os.getenv("TERMINATE_TIMEOUT_SUBPROCESS", 2.0)
)
# set default timer for download requests
DEFAULT_TIMEOUT_REQUESTS: float = float(os.getenv("DEFAULT_TIMEOUT_REQUESTS", 3.0))


class TimeoutHTTPAdapter(HTTPAdapter):
    """
    A custom Transport Adapter with default timeouts
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.timeout: float = DEFAULT_TIMEOUT_REQUESTS
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(
        self, request: requests.PreparedRequest, **kwargs: Any
    ) -> requests.Response:
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def get_valid_ffmpeg_path(
    custom_ffmpeg: str = "",
    is_windows: bool = False,
    ffmpeg_download_path: str = "",
    verbose: bool = False,
) -> str | bool:
    """
    ## get_valid_ffmpeg_path

    Validate the given FFmpeg path/binaries, and returns a valid FFmpeg executable path.

    Parameters:
        custom_ffmpeg (string): path to custom FFmpeg executables
        is_windows (boolean): is running on Windows OS?
        ffmpeg_download_path (string): FFmpeg static binaries download location _(Windows only)_
        verbose (bool): enables verbose for its operations

    **Returns:** A valid FFmpeg executable path string.
    """
    final_path = ""
    if is_windows:
        # checks if current os is windows
        if custom_ffmpeg:
            # if custom FFmpeg path is given assign to local variable
            final_path += custom_ffmpeg
        else:
            # otherwise auto-download them
            try:
                if not (ffmpeg_download_path):
                    # otherwise save to Temp Directory
                    import tempfile

                    ffmpeg_download_path = tempfile.gettempdir()

                verbose and logger.debug(
                    "FFmpeg Windows Download Path: {}".format(ffmpeg_download_path)
                )

                # download Binaries
                os_bit = (
                    ("win64" if platform.machine().endswith("64") else "win32")
                    if is_windows
                    else ""
                )
                _path = download_ffmpeg_binaries(
                    path=ffmpeg_download_path, os_windows=is_windows, os_bit=os_bit
                )
                # assign to local variable
                final_path += _path

            except Exception as e:
                # log if any error occurred
                logger.exception(str(e))
                logger.error(
                    "Error in downloading FFmpeg binaries, Check your network and Try again!"
                )
                return False

        if os.path.isfile(final_path):
            # check if valid FFmpeg file exist
            pass
        elif os.path.isfile(os.path.join(final_path, "ffmpeg.exe")):
            # check if FFmpeg directory exists, if does, then check for valid file
            final_path = os.path.join(final_path, "ffmpeg.exe")
        else:
            # else return False
            verbose and logger.debug(
                "No valid FFmpeg executables found at Custom FFmpeg path!"
            )
            return False
    else:
        # otherwise perform test for Unix
        if custom_ffmpeg:
            # if custom FFmpeg path is given assign to local variable
            if os.path.isfile(custom_ffmpeg):
                # check if valid FFmpeg file exist
                final_path += custom_ffmpeg
            elif os.path.isfile(os.path.join(custom_ffmpeg, "ffmpeg")):
                # check if FFmpeg directory exists, if does, then check for valid file
                final_path = os.path.join(custom_ffmpeg, "ffmpeg")
            else:
                # else return False
                verbose and logger.debug(
                    "No valid FFmpeg executables found at Custom FFmpeg path!"
                )
                return False
        else:
            # otherwise assign ffmpeg binaries from system
            final_path += "ffmpeg"

    verbose and logger.debug("Final FFmpeg Path: {}".format(final_path))

    # Final Auto-Validation for FFmeg Binaries. returns final path if test is passed
    return final_path if validate_ffmpeg(final_path, verbose=verbose) else False


def download_ffmpeg_binaries(
    path: str, os_windows: bool = False, os_bit: str = ""
) -> str:
    """
    ## download_ffmpeg_binaries

    Generates FFmpeg Static Binaries for windows(if not available)

    Parameters:
        path (string): path for downloading custom FFmpeg executables
        os_windows (boolean): is running on Windows OS?
        os_bit (string): 32-bit or 64-bit OS?

    **Returns:** A valid FFmpeg executable path string.
    """
    final_path = ""
    if os_windows and os_bit:
        # initialize with available FFmpeg Static Binaries GitHub Server
        file_url = "https://github.com/abhiTronix/FFmpeg-Builds/releases/latest/download/ffmpeg-static-{}-gpl.zip".format(
            os_bit
        )

        file_name = os.path.join(
            os.path.abspath(path), "ffmpeg-static-{}-gpl.zip".format(os_bit)
        )
        file_path = os.path.join(
            os.path.abspath(path),
            "ffmpeg-static-{}-gpl/bin/ffmpeg.exe".format(os_bit),
        )
        base_path, _ = os.path.split(file_name)  # extract file base path
        # check if file already exists
        if os.path.isfile(file_path):
            final_path += file_path  # skip download if does
        else:
            # import libs
            import zipfile

            # check if given path has write access
            assert os.access(path, os.W_OK), (
                "[Helper:ERROR] :: Permission Denied, Cannot write binaries to directory = "
                + path
            )
            # remove leftovers if exists
            os.path.isfile(file_name) and delete_file_safe(file_name)
            # download and write file to the given path
            with open(file_name, "wb") as f:
                logger.debug(
                    "No Custom FFmpeg path provided. Auto-Installing FFmpeg static binaries from GitHub Mirror now. Please wait..."
                )
                # create session
                with requests.Session() as http:
                    # setup retry strategy
                    retries = Retry(
                        total=3,
                        backoff_factor=1,
                        status_forcelist=[429, 500, 502, 503, 504],
                    )
                    # Mount it for https usage
                    adapter = TimeoutHTTPAdapter(
                        timeout=MAX_TIMEOUT_SUBPROCESS, max_retries=retries
                    )
                    http.mount("https://", adapter)
                    response = http.get(file_url, stream=True)
                    response.raise_for_status()
                    total_length = (
                        response.headers.get("content-length")
                        if "content-length" in response.headers
                        else len(response.content)
                    )
                    assert (
                        total_length is not None
                    ), "[Helper:ERROR] :: Failed to retrieve files, check your Internet connectivity!"
                    bar = tqdm(total=int(total_length), unit="B", unit_scale=True)
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                        len(data) > 0 and bar.update(len(data))
                    bar.close()
            logger.debug("Extracting executables.")
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                _zip_fname, _ = os.path.split(zip_ref.infolist()[0].filename)
                zip_ref.extractall(base_path)
            # perform cleaning
            delete_file_safe(file_name)
            logger.debug("FFmpeg binaries for Windows configured successfully!")
            final_path += file_path
    # return final path
    return final_path


def validate_ffmpeg(path: str, verbose: bool = False) -> bool:
    """
    ## validate_ffmpeg

    Validate FFmpeg Binaries. Returns `True` if validity test passes successfully.

    Parameters:
        path (string): absolute path of FFmpeg binaries
        verbose (bool): enables verbose for its operations

    **Returns:** A boolean value, confirming whether tests passed, or not?.
    """
    try:
        # get the FFmpeg version
        version = check_sp_output([path, "-version"])
        firstline = version.split(b"\n")[0]
        version = firstline.split(b" ")[2].strip()
        if verbose:  # log if test are passed
            logger.debug("FFmpeg validity Test Passed!")
            logger.debug(
                "Found valid FFmpeg Version: `{}` installed on this system".format(
                    version
                )
            )
    except Exception as e:
        # log if test are failed
        if verbose:
            logger.exception(str(e))
            logger.warning("FFmpeg validity Test Failed!")
        return False
    return True


def get_supported_pixfmts(path: str) -> list[tuple[str, str, str]]:
    """
    ## get_supported_pixfmts

    Find and returns all FFmpeg's supported pixel formats.

    Parameters:
        path (string): absolute path of FFmpeg binaries

    **Returns:** List of supported pixel formats as (PIXEL FORMAT, NB_COMPONENTS, BITS_PER_PIXEL).
    """
    pxfmts = check_sp_output([path, "-hide_banner", "-pix_fmts"])
    splitted = pxfmts.split(b"\n")
    srtindex = [i for i, s in enumerate(splitted) if b"-----" in s]
    # extract video encoders
    supported_pxfmts = [
        x.decode("utf-8").strip()
        for x in splitted[srtindex[0] + 1 :]
        if x.decode("utf-8").strip()
    ]
    # compile regex
    finder = re.compile(r"([A-Z]*[\.]+[A-Z]*\s[a-z0-9_-]*)(\s+[0-4])(\s+[0-9]+)")
    # find all outputs
    outputs = finder.findall("\n".join(supported_pxfmts))
    # return output findings
    return [
        (list(o[0].split(" "))[-1], o[1].strip(), o[2].strip())
        for o in outputs
        if len(o) == 3
    ]


def get_supported_vdecoders(path: str) -> list[str]:
    """
    ## get_supported_vdecoders

    Find and returns all FFmpeg's supported video decoders.

    Parameters:
        path (string): absolute path of FFmpeg binaries

    **Returns:** List of supported decoders.
    """
    decoders = check_sp_output([path, "-hide_banner", "-decoders"])
    splitted = decoders.split(b"\n")
    # extract video encoders
    supported_vdecoders = [
        x.decode("utf-8").strip()
        for x in splitted[2 : len(splitted) - 1]
        if x.decode("utf-8").strip().startswith("V")
    ]
    # compile regex
    finder = re.compile(r"[A-Z]*[\.]+[A-Z]*\s[a-z0-9_-]*")
    # find all outputs
    outputs = finder.findall("\n".join(supported_vdecoders))
    # return output findings
    return [list(o.split(" "))[-1] for o in outputs]


def get_supported_demuxers(path: str) -> list[str]:
    """
    ## get_supported_demuxers

    Find and returns all FFmpeg's supported demuxers.

    Parameters:
        path (string): absolute path of FFmpeg binaries

    **Returns:** List of supported demuxers.
    """
    # extract and clean FFmpeg output
    demuxers = check_sp_output([path, "-hide_banner", "-demuxers"])
    splitted = [x.decode("utf-8").strip() for x in demuxers.split(b"\n")]
    split_index = next((idx for idx, s in enumerate(splitted) if "--" in s), None)
    if split_index is None:
        logger.warning(
            "Failed to locate demuxer separator `--` in FFmpeg `-demuxers` output. "
            "Returning empty list of supported demuxers."
        )
        return []
    supported_demuxers = splitted[split_index + 1 : len(splitted) - 1]
    # search all demuxers
    outputs = [re.search(r"\s[a-z0-9_,-]{2,}\s", d) for d in supported_demuxers]
    outputs = [o.group(0) for o in outputs if o]
    # return demuxers output
    return [o.strip() if "," not in o else o.split(",")[-1].strip() for o in outputs]


def extract_device_n_demuxer(
    path: str, machine_OS: str | None = None, verbose: bool = False
) -> tuple[list[Any], str]:
    """
    ## get_valid_devicepath

    Discovers and extracts all Video-Capture device(s) name/path/index present on system and
    supported by valid OS specific FFmpeg demuxer.

    Parameters:
        path (string): absolute path of FFmpeg binaries.
        machine_OS(string): OS running _(Must be a value of `platform.system()` module)_.
        verbose (bool): enables/disables verbose.

    **Returns:** Tuple of list of supported device(s) path/name/index and OS specific demuxer used.
    """
    # validate `machine_OS` parameter value
    assert machine_OS is not None and isinstance(
        machine_OS, str
    ), "`machine_OS` parameter value is empty or invalid type. Aborting!"

    # initialize params
    devices: list[Any] = []  # handles devices discovered
    req_demuxer: str | None = None  # handle required demuxer

    # define all valid FFmpeg demuxers w.r.t OS platforms
    valid_demuxers = {"Windows": "dshow", "Darwin": "avfoundation", "Linux": "v4l2"}

    # check OS is supported
    if machine_OS.strip() not in list(valid_demuxers.keys()):
        # raise error if OS isn't supported
        raise ValueError(
            """Unsupported OS detected! The `source_demuxer='auto'` value isn't supported on your OS,
                Kindly assign `source` and `source_demuxer` parameter values manually."""
        )
    else:
        # assign required demuxer
        req_demuxer = valid_demuxers[machine_OS.strip()]

    # log if specified
    verbose and logger.debug("Auto-Searching for valid devices...")

    # assert if demuxer is supported by provided ffmpeg.
    assert req_demuxer in get_supported_demuxers(
        path
    ), "Required `{}` demuxer isn't supported by provided FFmpeg binaries. Kindly compile FFmpeg with \
            suitable flags or manually assign `source` and `source_demuxer` parameter values. Aborting!".format(
        valid_demuxers[machine_OS]
    )
    # create default ffmpeg command (for Windows and MacOS)
    default_ffcommand = "-hide_banner -list_devices true -f {} -i dummy".format(
        req_demuxer
    )

    # find all OS specific FFmpeg devices path and demuxer
    if machine_OS == "Windows":
        # get metadata
        metadata = check_sp_output(
            [path, *default_ffcommand.split(" ")],
            force_retrieve_stderr=True,
            timeout=MAX_TIMEOUT_SUBPROCESS,
        )
        # clean and split metadata
        splitted = [x.decode("utf-8").strip() for x in metadata.split(b"\n")]
        # find video only
        head, _sep, _tail = "\n".join(splitted).partition("DirectShow audio")
        if head.strip():
            # compile regex
            finder = re.compile(r'"(.*?[^\\])"')
            # find all outputs
            outputs = finder.findall(head.strip())
            # return output findings
            devices = [o.strip() for o in outputs if not (o.startswith("@device"))]
    elif machine_OS == "Linux":
        # get devices if `video4linux` drivers are correctly configured.
        metadata = check_sp_output(
            ["v4l2-ctl", "--list-devices"],
            force_retrieve_stderr=True,
        )
        # decode metadata
        decoded = metadata.decode("utf-8").strip()
        # check if command executed properly
        if (
            not decoded
            or {"command", "not", "found"}.issubset(decoded.split(" "))
            or (
                {"Cannot", "open", "device"}.issubset(decoded.split(" "))
                and "):" not in decoded
            )
        ):
            logger.error(
                "Cannot execute `v4l2-ctl` command. "
                + (
                    "Kindly install `v4l-utils` package on your linux machine."
                    if {"command", "not", "found"}.issubset(decoded.split(" "))
                    else "Permission denied! Add your username to the `video` group to fix this error."
                )
            )
        else:
            # clean metadata
            clean_n_splitted = [
                x.strip()
                for x in decoded.split("\n\n")
                if "/dev/video" in x and "):" in x
            ]
            # compile regex
            finder = re.compile(r"^[a-zA-Z0-9_.\- ]*")
            # iterate over data
            for data in clean_n_splitted:
                # find all valid device names
                device_name = [dev.strip() for dev in finder.findall(data) if dev]
                dev_paths = [x.strip() for x in data.split("\n") if "/dev/video" in x]
                # patch for multiple /dev/video paths for single device
                if len(dev_paths) > 1:
                    # warn users about this
                    verbose and logger.warning(
                        "Multiple `/dev/video` paths detected for {} device. This might take a while!".format(
                            device_name
                        )
                    )
                    # iterate over each device's paths
                    for path in dev_paths:
                        # search in path properties
                        metadata_path = check_sp_output(
                            ["v4l2-ctl", "--device={}".format(path), "--all"],
                            timeout=MAX_TIMEOUT_SUBPROCESS,
                        )
                        # decode path metadata
                        decoded_path = metadata_path.decode("utf-8").strip()
                        if (
                            "Width/Height" in decoded_path
                            and "Pixel Format" in decoded_path
                        ):
                            # append once required Width/Height and Pixel Format detected
                            devices.append({path: device_name})
                        else:
                            # skip path otherwise
                            pass
                elif len(dev_paths) == 1:
                    # append path directly if only one
                    devices.append({dev_paths[0]: device_name})
                else:
                    pass
    else:  # Darwin OSes
        # get metadata
        metadata = check_sp_output(
            [path, *default_ffcommand.split(" ")],
            force_retrieve_stderr=True,
            timeout=MAX_TIMEOUT_SUBPROCESS,
        )
        # clean and split metadata
        splitted = [x.decode("utf-8").strip() for x in metadata.split(b"\n")]
        # find video only
        head, _sep, _tail = "\n".join(splitted).partition("AVFoundation audio")
        if head.strip():
            # compile regex
            finder = re.compile(r"\[[0-9]\](.*)")
            # find all outputs
            outputs = finder.findall(head)
            # return output findings
            devices = [o.strip() for o in outputs]

    # check if any devices were found
    if devices:
        # log everything if `verbose=True`
        if verbose:
            for idx, dev in enumerate(devices):
                logger.info(
                    "[{}]: {}".format(
                        idx,
                        (
                            dev
                            if machine_OS != "Linux"
                            else "{} at path `{}`".format(
                                next(iter(dev.values()))[0], next(iter(dev.keys()))
                            )
                        ),
                    )
                )
            logger.debug(
                "Auto-Search completed successfully! Found `{}` valid device(s).".format(
                    len(devices)
                )
            )
        # return list of device name/path/index and related demuxer
        return (devices, req_demuxer)
    else:
        # otherwise raise error
        raise RuntimeError(
            "API unable to discover any valid device(s) connected your machine. Aborting!"
        )


def validate_imgseqdir(
    source: str, extension: str = "jpg", verbose: bool = False
) -> bool:
    """
    ## validate_imgseqdir

    Validates Image Sequence by counting number of Image files.

    Parameters:
        source (string): video source to be validated
        extension (string): extension of image sequence.

    **Returns:** A boolean value, confirming whether tests passed, or not?.
    """
    # check if path exists
    dirpath = Path(source).parent
    try:
        if not (dirpath.exists() and dirpath.is_dir()):
            verbose and logger.warning(
                "Specified path `{}` doesn't exists or valid.".format(dirpath)
            )
            return False
        else:
            return len(list(dirpath.glob("*.{}".format(extension)))) > 2
    except:
        return False


def is_valid_image_seq(
    path: str, source: str | None = None, verbose: bool = False
) -> bool:
    """
    ## is_valid_image_seq

    Checks Image sequence validity by testing its extension against
    FFmpeg's supported pipe formats and number of Image files.

    Parameters:
        path (string): absolute path of FFmpeg binaries
        source (string): video source to be validated
        verbose (bool): enables verbose for its operations

    **Returns:** A boolean value, confirming whether tests passed, or not?.
    """
    if source is None or not (source):
        logger.error("Source is empty!")
        return False
    # extract all FFmpeg supported protocols
    formats = check_sp_output([path, "-hide_banner", "-formats"])
    extract_formats = re.findall(r"\w+_pipe", formats.decode("utf-8").strip())
    supported_image_formats = [
        x.split("_")[0] for x in extract_formats if x.endswith("_pipe")
    ]
    _filename, extension = os.path.splitext(source)
    # Test and return result whether scheme is supported
    if extension and source.endswith(tuple(supported_image_formats)):
        if validate_imgseqdir(source, extension=extension[1:], verbose=verbose):
            verbose and logger.debug(
                "A valid Image Sequence source of format `{}` found.".format(extension)
            )
            return True
        else:
            ValueError(
                "Given Image Sequence source of format `{}` contains insignificant(invalid) sample size, Check the `source` parameter value again!".format(
                    source.split(".")[1]
                )
            )
    else:
        verbose and logger.warning("Source isn't a valid Image Sequence")
        return False


def is_valid_url(path: str, url: str | None = None, verbose: bool = False) -> bool:
    """
    ## is_valid_url

    Checks URL validity by testing its scheme against
    FFmpeg's supported protocols.

    Parameters:
        path (string): absolute path of FFmpeg binaries
        url (string): URL to be validated
        verbose (bool): enables verbose for its operations

    **Returns:** A boolean value, confirming whether tests passed, or not?.
    """
    if url is None or not (url):
        logger.warning("URL is empty!")
        return False
    # extract URL scheme
    extracted_scheme_url = url.split("://", 1)[0]
    # extract all FFmpeg supported protocols
    protocols = check_sp_output([path, "-hide_banner", "-protocols"])
    splitted = [x.decode("utf-8").strip() for x in protocols.split(b"\n")]
    supported_protocols = splitted[splitted.index("Output:") + 1 : len(splitted) - 1]
    # RTSP is a demuxer somehow
    # support both RTSP and RTSPS(over SSL)
    supported_protocols += (
        ["rtsp", "rtsps"] if "rtsp" in get_supported_demuxers(path) else []
    )
    # Test and return result whether scheme is supported
    if extracted_scheme_url and extracted_scheme_url in supported_protocols:
        verbose and logger.debug(
            "URL scheme `{}` is supported by FFmpeg.".format(extracted_scheme_url)
        )
        return True
    else:
        verbose and logger.warning(
            "URL scheme `{}` isn't supported by FFmpeg!".format(extracted_scheme_url)
        )
        return False


def check_sp_output(*args: Any, **kwargs: Any) -> bytes:
    """
    ## check_sp_output

    Executes a subprocess command and returns its `stdout` (or `stderr` when
    requested). On timeout, performs a two-step graceful shutdown — sends
    `SIGTERM` first to allow FFmpeg to flush buffers and release hardware
    resources (decoders, capture devices), then escalates to `SIGKILL` if the
    process fails to exit within a short grace period.

    Parameters:
        args (based on input): Non Keyword Arguments
        kwargs (based on input): Keyword Arguments
            force_retrieve_stderr (bool): If True, returns stderr. Also
                suppresses `CalledProcessError` on non-zero exit, since some
                FFmpeg diagnostic commands (e.g. `-list_devices`) emit useful
                output on stderr while exiting non-zero by design.
            timeout (float): Seconds to wait before terminating the process.

    **Returns:** A bytes value.
    """
    # workaround for python bug: https://bugs.python.org/issue37380
    if platform.system() == "Windows":
        # see comment https://bugs.python.org/msg370334
        sp._cleanup = lambda: None

    # handle additional params
    retrieve_stderr = kwargs.pop("force_retrieve_stderr", False)
    timeout = kwargs.pop("timeout", None)

    # execute command in subprocess
    process = sp.Popen(
        *args,
        stdout=sp.PIPE,
        stderr=sp.PIPE if retrieve_stderr else sp.DEVNULL,
        **kwargs,
    )

    # communicate and poll process with two-step timeout handling
    timeout_occurred = False
    try:
        output, stderr = process.communicate(timeout=timeout)
    except sp.TimeoutExpired:
        timeout_occurred = True
        logger.warning(
            f"[Pipeline-Warning] :: Process exceeded timeout of {timeout}s. "
            "Attempting graceful termination..."
        )
        # Step 1: polite SIGTERM, give process a chance to clean up
        process.terminate()
        try:
            output, stderr = process.communicate(timeout=TERMINATE_TIMEOUT_SUBPROCESS)
        except sp.TimeoutExpired:
            # Step 2: process ignored SIGTERM, force kill
            logger.error(
                "[Pipeline-Error] :: Process unresponsive to SIGTERM. "
                "Hard killing..."
            )
            process.kill()
            output, stderr = process.communicate()

    retcode = process.poll()

    # handle return code
    # Bypass CalledProcessError if caller wants stderr (some FFmpeg commands
    # exit non-zero by design) or if we killed the process via our timeout.
    if retcode and not retrieve_stderr and not timeout_occurred:
        logger.error(
            "[Pipeline-Error] :: {}".format(
                output.decode("utf-8") if output else "No output"
            )
        )
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = args[0]
        error = sp.CalledProcessError(retcode, cmd)
        error.output = output
        raise error

    # warn if process emitted nothing on either stream
    if not (bool(output) or bool(stderr)):
        logger.error(
            "[Pipeline-Error] :: Pipeline failed to extract any data from command: {}!".format(
                args[0] if args else []
            )
        )

    # return stderr when explicitly requested (and present), else stdout
    return stderr if retrieve_stderr and stderr else output
