#
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
#

import os
from pathlib import Path

"""
Path to the Indic NLP Resources directory
"""
# Default path, calculated relative to this file
_DEFAULT_RESOURCES_PATH = os.path.join(Path(__file__).resolve().parent, "RESOURCES")

# Get path from environment variable
_ENV_RESOURCES_PATH = os.environ.get("INDIC_RESOURCES_PATH")

# Use environment variable if it's set and not just whitespace, otherwise use default
if _ENV_RESOURCES_PATH and _ENV_RESOURCES_PATH.strip():
    INDIC_RESOURCES_PATH = _ENV_RESOURCES_PATH
else:
    INDIC_RESOURCES_PATH = _DEFAULT_RESOURCES_PATH


def init():
    """
    Validates that INDIC_RESOURCES_PATH is set to a non-empty string.
    The path is initialized at module load (considering environment variables)
    and can be modified by `set_resources_path`.
    This function can be called to explicitly check the configuration.
    """
    global INDIC_RESOURCES_PATH  # Keep global as set_resources_path also uses it.

    # Validate that INDIC_RESOURCES_PATH is a non-empty string.
    if not INDIC_RESOURCES_PATH or not INDIC_RESOURCES_PATH.strip():
        error_msg = (
            "INDIC_RESOURCES_PATH is not set or is empty. "
            "It should be automatically configured to point to the 'RESOURCES' directory "
            "within the library. This path can be overridden by setting the "
            "INDIC_RESOURCES_PATH environment variable or by calling "
            "the 'set_resources_path()' function."
        )
        raise IndicNlpException(error_msg)


def get_resources_path():
    """
    Get the path to the Indic NLP Resources directory
    """
    return INDIC_RESOURCES_PATH


def set_resources_path(resources_path):
    """
    Set the path to the Indic NLP Resources directory
    """
    global INDIC_RESOURCES_PATH
    INDIC_RESOURCES_PATH = resources_path


class IndicNlpException(Exception):
    """
    Exceptions thrown by Indic NLP Library components are instances of this class.
    'msg' attribute contains exception details.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
