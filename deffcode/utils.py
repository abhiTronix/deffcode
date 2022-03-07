"""
===============================================
deffcode library source-code is deployed under the Apache 2.0 License:

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

# Contains all the support functions/modules required by FFdecoder package

# import the necessary packages
import os
import logging
from colorlog import ColoredFormatter

# import helper packages
from .version import __version__


def logger_handler():
    """
    ## logger_handler

    Returns the logger handler

    **Returns:** A logger handler
    """
    # logging formatter
    formatter = ColoredFormatter(
        "{green}{asctime}{reset} :: {bold_purple}{name:^13}{reset} :: {log_color}{levelname:^8}{reset} :: {bold_white}{message}",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            "INFO": "bold_cyan",
            "DEBUG": "bold_yellow",
            "WARNING": "bold_red,fg_thin_yellow",
            "ERROR": "bold_red",
            "CRITICAL": "bold_red,bg_white",
        },
        style="{",
    )
    # check if FFdecoder_LOGFILE defined
    file_mode = os.environ.get("FFRAVEL_LOGFILE", False)
    # define handler
    handler = logging.StreamHandler()
    if file_mode and isinstance(file_mode, str):
        file_path = os.path.abspath(file_mode)
        if (os.name == "nt" or os.access in os.supports_effective_ids) and os.access(
            os.path.dirname(file_path), os.W_OK
        ):
            file_path = (
                os.path.join(file_path, "FFdecoder.log")
                if os.path.isdir(file_path)
                else file_path
            )
            handler = logging.FileHandler(file_path, mode="a")
            formatter = logging.Formatter(
                "{asctime} :: {name} :: {levelname} :: {message}",
                datefmt="%H:%M:%S",
                style="{",
            )

    handler.setFormatter(formatter)
    return handler


# define logger
logger = logging.getLogger("Utilies")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)
# log current version for debugging
logger.info("Running FFdecoder Version: {}".format(str(__version__)))


def dict2Args(param_dict):
    """
    ## dict2Args

    Converts dictionary attributes to list(args)

    Parameters:
        param_dict (dict): Parameters dictionary

    **Returns:** Arguments list
    """
    args = []
    for key in param_dict.keys():
        if key in ["-clones"] or key.startswith("-core"):
            if isinstance(param_dict[key], list):
                args.extend(param_dict[key])
            else:
                logger.warning(
                    "{} with invalid datatype:`{}`, Skipped!".format(
                        "Core parameter" if key.startswith("-core") else "Clone",
                        param_dict[key],
                    )
                )
        else:
            args.append(key)
            args.append(str(param_dict[key]))
    return args
