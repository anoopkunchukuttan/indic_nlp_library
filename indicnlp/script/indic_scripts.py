#
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
#

import pandas as pd
import numpy as np
import os

from indicnlp import common
from indicnlp.common import IndicNlpException
from indicnlp import langinfo as li
from indicnlp.script import phonetic_constants as pc

###
# Phonetic Information about script characters
###

""" Phonetic data about all languages except Tamil """
ALL_PHONETIC_DATA = None

""" Phonetic data for Tamil """
TAMIL_PHONETIC_DATA = None

""" Phonetic vector for all languages except Tamil """
ALL_PHONETIC_VECTORS = None

""" Phonetic vector for Tamil """
TAMIL_PHONETIC_VECTORS = None

# Use phonetic vector length from constants, allow override during init
PHONETIC_VECTOR_LENGTH = pc.DEFAULT_PHONETIC_VECTOR_LENGTH

# PHONETIC PROPERTIES and RANGES are now in phonetic_constants.py
# Indexes into the Phonetic Vector are now in phonetic_constants.py

#####
# Unicode information about characters
#####

SCRIPT_OFFSET_START = 0
SCRIPT_OFFSET_RANGE = 0x80


def init():
    """
    To be called by library loader, do not call it in your program
    """

    global ALL_PHONETIC_DATA, ALL_PHONETIC_VECTORS, TAMIL_PHONETIC_DATA, TAMIL_PHONETIC_VECTORS, PHONETIC_VECTOR_LENGTH

    ALL_PHONETIC_DATA = pd.read_csv(
        os.path.join(
            common.get_resources_path(), "script", "all_script_phonetic_data.csv"
        ),
        encoding="utf-8",
    )
    TAMIL_PHONETIC_DATA = pd.read_csv(
        os.path.join(
            common.get_resources_path(), "script", "tamil_script_phonetic_data.csv"
        ),
        encoding="utf-8",
    )

    ALL_PHONETIC_VECTORS = ALL_PHONETIC_DATA.iloc[
        :, pc.PHONETIC_VECTOR_START_OFFSET :
    ].values
    TAMIL_PHONETIC_VECTORS = TAMIL_PHONETIC_DATA.iloc[
        :, pc.PHONETIC_VECTOR_START_OFFSET :
    ].values

    # Update the phonetic vector length based on the loaded data (assuming all_script has the representative length)
    if ALL_PHONETIC_VECTORS is not None and ALL_PHONETIC_VECTORS.shape[1] > 0:
        PHONETIC_VECTOR_LENGTH = ALL_PHONETIC_VECTORS.shape[1]
    elif TAMIL_PHONETIC_VECTORS is not None and TAMIL_PHONETIC_VECTORS.shape[1] > 0:
        PHONETIC_VECTOR_LENGTH = TAMIL_PHONETIC_VECTORS.shape[1]
    else:
        PHONETIC_VECTOR_LENGTH = pc.DEFAULT_PHONETIC_VECTOR_LENGTH


def is_supported_language(lang):
    return lang in list(li.SCRIPT_RANGES.keys())


def get_offset(c, lang):
    if not is_supported_language(lang):
        raise IndicNlpException("Language {}  not supported".format(lang))
    return ord(c) - li.SCRIPT_RANGES[lang][0]


def offset_to_char(off, lang):
    """
    Applicable to Brahmi derived Indic scripts
    """
    if not is_supported_language(lang):
        raise IndicNlpException("Language {}  not supported".format(lang))
    return chr(off + li.SCRIPT_RANGES[lang][0])


def is_indiclang_char(c, lang):
    """
    Applicable to Brahmi derived Indic scripts
    Note that DANDA and DOUBLE_DANDA have the same Unicode codepoint for all Indic scripts
    """
    if not is_supported_language(lang):
        raise IndicNlpException("Language {}  not supported".format(lang))
    o = get_offset(c, lang)
    return (
        (o >= SCRIPT_OFFSET_START and o < SCRIPT_OFFSET_RANGE)
        or ord(c) == li.DANDA
        or ord(c) == li.DOUBLE_DANDA
    )


def in_coordinated_range_offset(c_offset):
    """
    Applicable to Brahmi derived Indic scripts
    """
    return (
        c_offset >= li.COORDINATED_RANGE_START_INCLUSIVE
        and c_offset <= li.COORDINATED_RANGE_END_INCLUSIVE
    )


def in_coordinated_range(c, lang):
    if not is_supported_language(lang):
        raise IndicNlpException("Language {}  not supported".format(lang))
    return in_coordinated_range_offset(get_offset(c, lang))


def get_phonetic_info(lang):
    if not is_supported_language(lang):
        raise IndicNlpException("Language {}  not supported".format(lang))
    phonetic_data = ALL_PHONETIC_DATA if lang != li.LC_TA else TAMIL_PHONETIC_DATA
    phonetic_vectors = (
        ALL_PHONETIC_VECTORS if lang != li.LC_TA else TAMIL_PHONETIC_VECTORS
    )

    return (phonetic_data, phonetic_vectors)


def invalid_vector():
    return pc.get_invalid_vector(PHONETIC_VECTOR_LENGTH)


def get_phonetic_feature_vector(c, lang):
    offset = get_offset(c, lang)

    if not in_coordinated_range_offset(offset):
        return invalid_vector()

    phonetic_data, phonetic_vectors = get_phonetic_info(lang)

    if phonetic_data.iloc[offset]["Valid Vector Representation"] == 0:
        return invalid_vector()

    return phonetic_vectors[offset]


def get_phonetic_feature_vector_offset(offset, lang):
    if not in_coordinated_range_offset(offset):
        return invalid_vector()

    phonetic_data, phonetic_vectors = get_phonetic_info(lang)

    if offset >= len(phonetic_data.index):
        return invalid_vector()

    if phonetic_data.iloc[offset]["Valid Vector Representation"] == 0:
        return invalid_vector()

    return phonetic_vectors[offset]


### Unary operations on vectors
def is_valid(v):
    return np.sum(v) > 0


def is_vowel(v):
    return v[pc.PVIDX_BT_VOWEL] == 1


def is_consonant(v):
    return v[pc.PVIDX_BT_CONSONANT] == 1


def is_halant(v):
    return v[pc.PVIDX_BT_HALANT] == 1


def is_nukta(v):
    return v[pc.PVIDX_BT_NUKTA] == 1


def is_anusvaar(v):
    return v[pc.PVIDX_BT_ANUSVAAR] == 1


def is_misc(v):
    return v[pc.PVIDX_BT_MISC] == 1


def is_dependent_vowel(v):
    return is_vowel(v) and v[pc.PVIDX_VSTAT_DEP] == 1


def is_plosive(v):
    return is_consonant(v) and get_property_vector(v, "consonant_type")[0] == 1


### Binary operations on phonetic vectors


def or_vectors(v1, v2):
    return np.array([1 if (b1 + b2) >= 1 else 0 for b1, b2 in zip(v1, v2)])


def xor_vectors(v1, v2):
    return np.array([1 if b1 != b2 else 0 for b1, b2 in zip(v1, v2)])


### Getting properties from phonetic vectors


def get_property_vector(v, prop_name):
    # Ensure prop_name is valid to prevent KeyError
    if prop_name not in pc.PV_PROP_RANGES:
        raise ValueError(f"Unknown property name: {prop_name}")
    return v[pc.PV_PROP_RANGES[prop_name][0] : pc.PV_PROP_RANGES[prop_name][1]]


def get_property_value(v, prop_name):
    factor_bits = get_property_vector(v, prop_name).tolist()

    v = 0
    c = 1
    for b in factor_bits[::-1]:
        v += c * b
        c = c * 2.0

    return int(v)


def lcsr_indic(srcw, tgtw, slang, tlang):
    """
    compute the Longest Common Subsequence Ratio (LCSR) between two strings at the character level.
    This works for Indic scripts by mapping both languages to a common script

    srcw: source language string
    tgtw: source language string
    slang: source language
    tlang: target language
    """
    score_mat = np.zeros((len(srcw) + 1, len(tgtw) + 1))

    for si, sc in enumerate(srcw, 1):
        for ti, tc in enumerate(tgtw, 1):
            so = get_offset(sc, slang)
            to = get_offset(tc, tlang)

            if (
                in_coordinated_range_offset(so)
                and in_coordinated_range_offset(to)
                and so == to
            ):
                score_mat[si, ti] = score_mat[si - 1, ti - 1] + 1.0
            elif (
                not (in_coordinated_range_offset(so) or in_coordinated_range_offset(to))
                and sc == tc
            ):
                score_mat[si, ti] = score_mat[si - 1, ti - 1] + 1.0
            else:
                score_mat[si, ti] = max(score_mat[si, ti - 1], score_mat[si - 1, ti])

    return (
        score_mat[-1, -1] / float(max(len(srcw), len(tgtw))),
        float(len(srcw)),
        float(len(tgtw)),
    )


def lcsr_any(srcw, tgtw):
    """
    LCSR computation if both languages have the same script
    """
    score_mat = np.zeros((len(srcw) + 1, len(tgtw) + 1))

    for si, sc in enumerate(srcw, 1):
        for ti, tc in enumerate(tgtw, 1):
            if sc == tc:
                score_mat[si, ti] = score_mat[si - 1, ti - 1] + 1.0
            else:
                score_mat[si, ti] = max(score_mat[si, ti - 1], score_mat[si - 1, ti])

    return (
        score_mat[-1, -1] / float(max(len(srcw), len(tgtw))),
        float(len(srcw)),
        float(len(tgtw)),
    )


def lcsr(srcw, tgtw, slang, tlang):
    """
    compute the Longest Common Subsequence Ratio (LCSR) between two strings at the character level.

    srcw: source language string
    tgtw: source language string
    slang: source language
    tlang: target language
    """

    if (
        slang == tlang
        or not is_supported_language(slang)
        or not is_supported_language(tlang)
    ):
        return lcsr_any(srcw, tgtw, slang, tlang)
    else:
        return lcsr_indic(srcw, tgtw)
