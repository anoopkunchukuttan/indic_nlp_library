#
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
#

import os
import pandas as pd
import numpy as np

from indicnlp import common
from indicnlp.script import phonetic_constants as pc

# Maps from ARPABET to Internal Id
ARPABET_ID_MAP = {}
ID_ARPABET_MAP = {}


# Phonetic Information about script characters
ENGLISH_PHONETIC_DATA = None

ENGLISH_PHONETIC_VECTORS = None

# Use phonetic vector length from constants, allow override during init
PHONETIC_VECTOR_LENGTH = pc.DEFAULT_PHONETIC_VECTOR_LENGTH


def init():
    """
    To be called by library loader, do not call it in your program
    """

    global ENGLISH_PHONETIC_DATA, ENGLISH_PHONETIC_VECTORS, PHONETIC_VECTOR_LENGTH

    ENGLISH_PHONETIC_DATA = pd.read_csv(
        os.path.join(
            common.get_resources_path(), "script", "english_script_phonetic_data.csv"
        ),
        encoding="utf-8",
    )

    ENGLISH_PHONETIC_VECTORS = ENGLISH_PHONETIC_DATA.iloc[
        :, pc.PHONETIC_VECTOR_START_OFFSET :
    ].values

    # Update the phonetic vector length based on the loaded data
    if ENGLISH_PHONETIC_VECTORS is not None:
        PHONETIC_VECTOR_LENGTH = ENGLISH_PHONETIC_VECTORS.shape[1]
    else:
        # Fallback or error handling if vectors are not loaded
        PHONETIC_VECTOR_LENGTH = pc.DEFAULT_PHONETIC_VECTOR_LENGTH

    ### Load mapping from ARPABET representation of phoneme to internal ID
    global ARPABET_ID_MAP, ID_ARPABET_MAP

    with open(
        os.path.join(common.get_resources_path(), "script", "english_arpabet_list.csv"),
        "r",
        encoding="utf-8",
    ) as infile:
        for ph_id, name in enumerate(iter(infile)):
            name = name.strip()
            ARPABET_ID_MAP[name] = ph_id
            ID_ARPABET_MAP[ph_id] = name


def phoneme_to_offset(ph):
    return ARPABET_ID_MAP[ph]


def offset_to_phoneme(ph_id):
    return ID_ARPABET_MAP[ph_id]


def phoneme_to_enc(ph):
    return chr(pc.SCRIPT_RANGE_START + phoneme_to_offset(ph))


def enc_to_phoneme(ph):
    return offset_to_phoneme(enc_to_offset(ph))


def enc_to_offset(c):
    return ord(c) - pc.SCRIPT_RANGE_START


def in_range(offset):
    return offset >= pc.SCRIPT_RANGE_START and offset < pc.SCRIPT_RANGE_END


def get_phonetic_info(
    lang,
):  # lang parameter is kept for API consistency if called from generic code
    return (ENGLISH_PHONETIC_DATA, ENGLISH_PHONETIC_VECTORS)


def invalid_vector():
    return pc.get_invalid_vector(PHONETIC_VECTOR_LENGTH)


def get_phonetic_feature_vector(p, lang):  # lang parameter is kept for API consistency
    offset = enc_to_offset(p)

    if not in_range(offset):
        return invalid_vector()

    # Since this is english_script, we directly use its phonetic data
    # phonetic_data, phonetic_vectors = get_phonetic_info(lang) # Not needed

    if ENGLISH_PHONETIC_DATA.iloc[offset]["Valid Vector Representation"] == 0:
        return invalid_vector()

    return ENGLISH_PHONETIC_VECTORS[offset]
