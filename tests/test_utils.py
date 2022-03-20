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

import pytest
import logging
import os
from os.path import expanduser
from deffcode.utils import (
    dict2Args,
    logger_handler,
)

# define test logger
logger = logging.getLogger("Test_utils")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(logging.DEBUG)


test_data = [
    (os.path.join(expanduser("~"), "deffcode.log"), logging.FileHandler("test.log")),
    (False, logging.StreamHandler()),
]


@pytest.mark.parametrize("log_filepath, handler_type", test_data)
def test_loggerhandler(log_filepath, handler_type):
    """
    Testing dict2Args utils function.
    """
    if log_filepath:
        os.environ["DEFFCODE_LOGFILE"] = log_filepath
    try:
        assert type(logger_handler()) == type(handler_type), "Test failed"
    except AssertionError:
        pytest.fail("Logger handler test failed!")
    finally:
        log_filepath and os.environ.pop("DEFFCODE_LOGFILE", None)


test_data = [
    {"-thread_queue_size": "512", "-f": "alsa", "-clones": 24},
    {
        "-thread_queue_size": "512",
        "-f": "alsa",
        "-clones": ["-map", "0:v:0", "-map", "1:a?"],
        "-ac": "1",
        "-ar": "48000",
        "-i": "plughw:CARD=CAMERA,DEV=0",
    },
    {
        "-thread_queue_size": "512",
        "-f": "alsa",
        "-ac": "1",
        "-ar": "48000",
        "-i": "plughw:CARD=CAMERA,DEV=0",
    },
]


@pytest.mark.parametrize("dictionary", test_data)
def test_dict2Args(dictionary):
    """
    Testing dict2Args utils function.
    """
    result = dict2Args(dictionary)
    if result and isinstance(result, list):
        logger.debug("dict2Args converted Arguments are: {}".format(result))
    else:
        pytest.fail("Failed to complete this test!")


def test_delete_file_safe():
    """
    Testing delete_file_safe method
    """
    try:
        delete_file_safe(os.path.join(expanduser("~"), "invalid"))
    except Exception as e:
        pytest.fail(str(e))
