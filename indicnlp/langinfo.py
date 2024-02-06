#
#  Copyright (c) 2013-present, Anoop Kunchukuttan
#  All rights reserved.
#
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree.
#

## language codes
LC_TA = "ta"

SCRIPT_RANGES = {
    "pa": [0x0A00, 0x0A7F],
    "gu": [0x0A80, 0x0AFF],
    "or": [0x0B00, 0x0B7F],
    "ta": [0x0B80, 0x0BFF],
    "te": [0x0C00, 0x0C7F],
    "kn": [0x0C80, 0x0CFF],
    "ml": [0x0D00, 0x0D7F],
    "si": [0x0D80, 0x0DFF],
    "hi": [0x0900, 0x097F],
    "mr": [0x0900, 0x097F],
    "kK": [0x0900, 0x097F],
    "sa": [0x0900, 0x097F],
    "ne": [0x0900, 0x097F],
    "sd": [0x0900, 0x097F],
    "bn": [0x0980, 0x09FF],
    "as": [0x0980, 0x09FF],
}

DRAVIDIAN_LANGUAGES = [
    "ta",
    "te",
    "kn",
    "ml",
]
IE_LANGUAGES = [
    "hi",
    "mr",
    "kK",
    "sa",
    "ne",
    "sd",
    "bn",
    "as",
    "pa",
    "gu",
    "or",
    "si",
]
DANDA_DELIM_LANGUAGES = ["as", "bn", "hi", "ne", "or", "pa", "sa", "sd"]

URDU_RANGES = [
    [0x0600, 0x06FF],
    [0x0750, 0x077F],
    [0xFB50, 0xFDFF],
    [0xFE70, 0xFEFF],
]

COORDINATED_RANGE_START_INCLUSIVE = 0
COORDINATED_RANGE_END_INCLUSIVE = 0x6F

NUMERIC_OFFSET_START = 0x66
NUMERIC_OFFSET_END = 0x6F

HALANTA_OFFSET = 0x4D
AUM_OFFSET = 0x50
NUKTA_OFFSET = 0x3C

RUPEE_SIGN = 0x20B9

DANDA = 0x0964
DOUBLE_DANDA = 0x0965

# TODO: add missing fricatives and approximants
VELAR_RANGE = [0x15, 0x19]
PALATAL_RANGE = [0x1A, 0x1E]
RETROFLEX_RANGE = [0x1F, 0x23]
DENTAL_RANGE = [0x24, 0x29]
LABIAL_RANGE = [0x2A, 0x2E]

# verify
VOICED_LIST = [0x17, 0x18, 0x1C, 0x1D, 0x21, 0x22, 0x26, 0x27, 0x2C, 0x2D]
UNVOICED_LIST = [
    0x15,
    0x16,
    0x1A,
    0x1B,
    0x1F,
    0x20,
    0x24,
    0x25,
    0x2A,
    0x2B,
]  # TODO: add sibilants/sonorants
ASPIRATED_LIST = [0x16, 0x18, 0x1B, 0x1D, 0x20, 0x22, 0x25, 0x27, 0x2B, 0x2D]
UNASPIRATED_LIST = [0x15, 0x17, 0x1A, 0x1C, 0x1F, 0x21, 0x24, 0x26, 0x2A, 0x2C]
NASAL_LIST = [0x19, 0x1E, 0x23, 0x28, 0x29, 0x2D]
FRICATIVE_LIST = [0x36, 0x37, 0x38]
APPROXIMANT_LIST = [0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35]

# TODO: ha has to be properly categorized


def is_danda_delim(lang):
    """
    Returns True if danda/double danda is a possible delimiter for the language
    """
    return lang in DANDA_DELIM_LANGUAGES


def get_offset(c, lang):
    """
    Applicable to Brahmi derived Indic scripts
    """
    return ord(c) - SCRIPT_RANGES[lang][0]


def offset_to_char(c, lang):
    """
    Applicable to Brahmi derived Indic scripts
    """
    return chr(c + SCRIPT_RANGES[lang][0])


def in_coordinated_range(c_offset):
    """
    Applicable to Brahmi derived Indic scripts
    """
    return (
        c_offset >= COORDINATED_RANGE_START_INCLUSIVE
        and c_offset <= COORDINATED_RANGE_END_INCLUSIVE
    )


def is_indiclang_char(c, lang):
    """
    Applicable to Brahmi derived Indic scripts
    """
    o = get_offset(c, lang)
    return (o >= 0 and o <= 0x7F) or ord(c) == DANDA or ord(c) == DOUBLE_DANDA


# def is_vowel(c,lang):
#     """
#     Is the character a vowel
#     """
#     o=get_offset(c,lang)
#     return (o>=0x04 and o<=0x14)

# def is_vowel_sign(c,lang):
#     """
#     Is the character a vowel sign (maatraa)
#     """
#     o=get_offset(c,lang)
#     return (o>=0x3e and o<=0x4c)

# def is_halanta(c,lang):
#     """
#     Is the character the halanta character
#     """
#     o=get_offset(c,lang)
#     return (o==HALANTA_OFFSET)

# def is_nukta(c,lang):
#     """
#     Is the character the halanta character
#     """
#     o=get_offset(c,lang)
#     return (o==NUKTA_OFFSET)

# def is_aum(c,lang):
#     """
#     Is the character a vowel sign (maatraa)
#     """
#     o=get_offset(c,lang)
#     return (o==AUM_OFFSET)

# def is_consonant(c,lang):
#     """
#     Is the character a consonant
#     """
#     o=get_offset(c,lang)
#     return (o>=0x15 and o<=0x39)

# def is_velar(c,lang):
#     """
#     Is the character a velar
#     """
#     o=get_offset(c,lang)
#     return (o>=VELAR_RANGE[0] and o<=VELAR_RANGE[1])

# def is_palatal(c,lang):
#     """
#     Is the character a palatal
#     """
#     o=get_offset(c,lang)
#     return (o>=PALATAL_RANGE[0] and o<=PALATAL_RANGE[1])

# def is_retroflex(c,lang):
#     """
#     Is the character a retroflex
#     """
#     o=get_offset(c,lang)
#     return (o>=RETROFLEX_RANGE[0] and o<=RETROFLEX_RANGE[1])

# def is_dental(c,lang):
#     """
#     Is the character a dental
#     """
#     o=get_offset(c,lang)
#     return (o>=DENTAL_RANGE[0] and o<=DENTAL_RANGE[1])

# def is_labial(c,lang):
#     """
#     Is the character a labial
#     """
#     o=get_offset(c,lang)
#     return (o>=LABIAL_RANGE[0] and o<=LABIAL_RANGE[1])

# def is_voiced(c,lang):
#     """
#     Is the character a voiced consonant
#     """
#     o=get_offset(c,lang)
#     return o in VOICED_LIST

# def is_unvoiced(c,lang):
#     """
#     Is the character a unvoiced consonant
#     """
#     o=get_offset(c,lang)
#     return o in UNVOICED_LIST

# def is_aspirated(c,lang):
#     """
#     Is the character a aspirated consonant
#     """
#     o=get_offset(c,lang)
#     return o in ASPIRATED_LIST

# def is_unaspirated(c,lang):
#     """
#     Is the character a unaspirated consonant
#     """
#     o=get_offset(c,lang)
#     return o in UNASPIRATED_LIST

# def is_nasal(c,lang):
#     """
#     Is the character a nasal consonant
#     """
#     o=get_offset(c,lang)
#     return o in NASAL_LIST

# def is_fricative(c,lang):
#     """
#     Is the character a fricative consonant
#     """
#     o=get_offset(c,lang)
#     return o in FRICATIVE_LIST

# def is_approximant(c,lang):
#     """
#     Is the character an approximant consonant
#     """
#     o=get_offset(c,lang)
#     return o in APPROXIMANT_LIST

# def is_number(c,lang):
#     """
#     Is the character a number
#     """
#     o=get_offset(c,lang)
#     return (o>=0x66 and o<=0x6f)


def is_vowel(c, lang):
    """
    Is the character a vowel
    """
    o = get_offset(c, lang)
    return o >= 0x04 and o <= 0x14


def is_vowel_sign(c, lang):
    """
    Is the character a vowel sign (maatraa)
    """
    o = get_offset(c, lang)
    return o >= 0x3E and o <= 0x4C


def is_halanta(c, lang):
    """
    Is the character the halanta character
    """
    o = get_offset(c, lang)
    return o == HALANTA_OFFSET


def is_nukta(c, lang):
    """
    Is the character the halanta character
    """
    o = get_offset(c, lang)
    return o == NUKTA_OFFSET


def is_aum(c, lang):
    """
    Is the character a vowel sign (maatraa)
    """
    o = get_offset(c, lang)
    return o == AUM_OFFSET


def is_consonant(c, lang):
    """
    Is the character a consonant
    """
    o = get_offset(c, lang)
    return o >= 0x15 and o <= 0x39


def is_velar(c, lang):
    """
    Is the character a velar
    """
    o = get_offset(c, lang)
    return o >= VELAR_RANGE[0] and o <= VELAR_RANGE[1]


def is_palatal(c, lang):
    """
    Is the character a palatal
    """
    o = get_offset(c, lang)
    return o >= PALATAL_RANGE[0] and o <= PALATAL_RANGE[1]


def is_retroflex(c, lang):
    """
    Is the character a retroflex
    """
    o = get_offset(c, lang)
    return o >= RETROFLEX_RANGE[0] and o <= RETROFLEX_RANGE[1]


def is_dental(c, lang):
    """
    Is the character a dental
    """
    o = get_offset(c, lang)
    return o >= DENTAL_RANGE[0] and o <= DENTAL_RANGE[1]


def is_labial(c, lang):
    """
    Is the character a labial
    """
    o = get_offset(c, lang)
    return o >= LABIAL_RANGE[0] and o <= LABIAL_RANGE[1]


def is_voiced(c, lang):
    """
    Is the character a voiced consonant
    """
    o = get_offset(c, lang)
    return o in VOICED_LIST


def is_unvoiced(c, lang):
    """
    Is the character a unvoiced consonant
    """
    o = get_offset(c, lang)
    return o in UNVOICED_LIST


def is_aspirated(c, lang):
    """
    Is the character a aspirated consonant
    """
    o = get_offset(c, lang)
    return o in ASPIRATED_LIST


def is_unaspirated(c, lang):
    """
    Is the character a unaspirated consonant
    """
    o = get_offset(c, lang)
    return o in UNASPIRATED_LIST


def is_nasal(c, lang):
    """
    Is the character a nasal consonant
    """
    o = get_offset(c, lang)
    return o in NASAL_LIST


def is_fricative(c, lang):
    """
    Is the character a fricative consonant
    """
    o = get_offset(c, lang)
    return o in FRICATIVE_LIST


def is_approximant(c, lang):
    """
    Is the character an approximant consonant
    """
    o = get_offset(c, lang)
    return o in APPROXIMANT_LIST


def is_number(c, lang):
    """
    Is the character a number
    """
    o = get_offset(c, lang)
    return o >= 0x66 and o <= 0x6F


##################################################


def is_vowel_offset(c_offset):
    """
    Is the offset a vowel
    """
    return c_offset >= 0x04 and c_offset <= 0x14


def is_vowel_sign_offset(c_offset):
    """
    Is the offset a vowel sign (maatraa)
    """
    return c_offset >= 0x3E and c_offset <= 0x4C


def is_halanta_offset(c_offset):
    """
    Is the offset the halanta offset
    """
    return c_offset == HALANTA_OFFSET


def is_nukta_offset(c_offset):
    """
    Is the offset the halanta offset
    """
    return c_offset == NUKTA_OFFSET


def is_aum_offset(c_offset):
    """
    Is the offset a vowel sign (maatraa)
    """
    return c_offset == AUM_OFFSET


def is_consonant_offset(c_offset):
    """
    Is the offset a consonant
    """
    return c_offset >= 0x15 and c_offset <= 0x39


def is_velar_offset(c_offset):
    """
    Is the offset a velar
    """
    return c_offset >= VELAR_RANGE[0] and c_offset <= VELAR_RANGE[1]


def is_palatal_offset(c_offset):
    """
    Is the offset a palatal
    """
    return c_offset >= PALATAL_RANGE[0] and c_offset <= PALATAL_RANGE[1]


def is_retroflex_offset(c_offset):
    """
    Is the offset a retroflex
    """
    return c_offset >= RETROFLEX_RANGE[0] and c_offset <= RETROFLEX_RANGE[1]


def is_dental_offset(c_offset):
    """
    Is the offset a dental
    """
    return c_offset >= DENTAL_RANGE[0] and c_offset <= DENTAL_RANGE[1]


def is_labial_offset(c_offset):
    """
    Is the offset a labial
    """
    return c_offset >= LABIAL_RANGE[0] and c_offset <= LABIAL_RANGE[1]


def is_voiced_offset(c_offset):
    """
    Is the offset a voiced consonant
    """
    return c_offset in VOICED_LIST


def is_unvoiced_offset(c_offset):
    """
    Is the offset a unvoiced consonant
    """
    return c_offset in UNVOICED_LIST


def is_aspirated_offset(c_offset):
    """
    Is the offset a aspirated consonant
    """
    return c_offset in ASPIRATED_LIST


def is_unaspirated_offset(c_offset):
    """
    Is the offset a unaspirated consonant
    """
    return c_offset in UNASPIRATED_LIST


def is_nasal_offset(c_offset):
    """
    Is the offset a nasal consonant
    """
    return c_offset in NASAL_LIST


def is_fricative_offset(c_offset):
    """
    Is the offset a fricative consonant
    """
    return c_offset in FRICATIVE_LIST


def is_approximant_offset(c_offset):
    """
    Is the offset an approximant consonant
    """
    return c_offset in APPROXIMANT_LIST


def is_number_offset(c_offset):
    """
    Is the offset a number
    """
    return c_offset >= 0x66 and c_offset <= 0x6F
