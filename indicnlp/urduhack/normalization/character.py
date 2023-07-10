# coding: utf8
"""
Character Normalization functions
provides functionality to put proper spaces before and after numeric digits, urdu digits
and punctuations.
"""
from typing import Dict, List
import logging

from .regexes import _DIACRITICS_RE
from .regexes import _SPACE_AFTER_PUNCTUATIONS_RE, _REMOVE_SPACE_BEFORE_PUNCTUATIONS_RE

logger = logging.getLogger(__name__)

# Contains wrong Urdu characters mapping to correct characters
_CORRECT_URDU_CHARACTERS_MAPPING: Dict[str, List[str]] = {'آ': ['ﺁ', 'ﺂ'],
                                                          'أ': ['ﺃ'],
                                                          'ا': ['ﺍ', 'ﺎ', ],
                                                          'ب': ['ﺏ', 'ﺐ', 'ﺑ', 'ﺒ'],
                                                          'پ': ['ﭖ', 'ﭘ', 'ﭙ', ],
                                                          'ت': ['ﺕ', 'ﺖ', 'ﺗ', 'ﺘ'],
                                                          'ٹ': ['ﭦ', 'ﭧ', 'ﭨ', 'ﭩ'],
                                                          'ث': ['ﺛ', 'ﺜ', 'ﺚ'],
                                                          'ج': ['ﺝ', 'ﺞ', 'ﺟ', 'ﺠ'],
                                                          'ح': ['ﺡ', 'ﺣ', 'ﺤ', 'ﺢ'],
                                                          'خ': ['ﺧ', 'ﺨ', 'ﺦ'],
                                                          'د': ['ﺩ', 'ﺪ'],
                                                          'ذ': ['ﺬ', 'ﺫ'],
                                                          'ر': ['ﺭ', 'ﺮ'],
                                                          'ز': ['ﺯ', 'ﺰ', ],
                                                          'س': ['ﺱ', 'ﺲ', 'ﺳ', 'ﺴ', ],
                                                          'ش': ['ﺵ', 'ﺶ', 'ﺷ', 'ﺸ'],
                                                          'ص': ['ﺹ', 'ﺺ', 'ﺻ', 'ﺼ', ],
                                                          'ض': ['ﺽ', 'ﺾ', 'ﺿ', 'ﻀ'],
                                                          'ط': ['ﻃ', 'ﻄ'],
                                                          'ظ': ['ﻅ', 'ﻇ', 'ﻈ'],
                                                          'ع': ['ﻉ', 'ﻊ', 'ﻋ', 'ﻌ', ],
                                                          'غ': ['ﻍ', 'ﻏ', 'ﻐ', ],
                                                          'ف': ['ﻑ', 'ﻒ', 'ﻓ', 'ﻔ', ],
                                                          'ق': ['ﻕ', 'ﻖ', 'ﻗ', 'ﻘ', ],
                                                          'ل': ['ﻝ', 'ﻞ', 'ﻟ', 'ﻠ', ],
                                                          'م': ['ﻡ', 'ﻢ', 'ﻣ', 'ﻤ', ],
                                                          'ن': ['ﻥ', 'ﻦ', 'ﻧ', 'ﻨ', ],
                                                          'چ': ['ﭺ', 'ﭻ', 'ﭼ', 'ﭽ'],
                                                          'ڈ': ['ﮈ', 'ﮉ'],
                                                          'ڑ': ['ﮍ', 'ﮌ'],
                                                          'ژ': ['ﮋ', ],
                                                          'ک': ['ﮎ', 'ﮏ', 'ﮐ', 'ﮑ', 'ﻛ', 'ك'],
                                                          'گ': ['ﮒ', 'ﮓ', 'ﮔ', 'ﮕ'],
                                                          'ں': ['ﮞ', 'ﮟ'],
                                                          'و': ['ﻮ', 'ﻭ', 'ﻮ', ],
                                                          'ؤ': ['ﺅ'],
                                                          'ھ': ['ﮪ', 'ﮬ', 'ﮭ', 'ﻬ', 'ﻫ', 'ﮫ'],
                                                          'ہ': ['ﻩ', 'ﮦ', 'ﻪ', 'ﮧ', 'ﮩ', 'ﮨ', 'ه', ],
                                                          'ۂ': [],
                                                          'ۃ': ['ة'],
                                                          'ء': ['ﺀ'],
                                                          'ی': ['ﯼ', 'ى', 'ﯽ', 'ﻰ', 'ﻱ', 'ﻲ', 'ﯾ', 'ﯿ', 'ي'],
                                                          'ئ': ['ﺋ', 'ﺌ', ],
                                                          'ے': ['ﮮ', 'ﮯ', 'ﻳ', 'ﻴ', ],
                                                          'ۓ': [],
                                                          '۰': ['٠'],
                                                          '۱': ['١'],
                                                          '۲': ['٢'],
                                                          '۳': ['٣'],
                                                          '۴': ['٤'],
                                                          '۵': ['٥'],
                                                          '۶': ['٦'],
                                                          '۷': ['٧'],
                                                          '۸': ['٨'],
                                                          '۹': ['٩'],
                                                          '۔': [],
                                                          '؟': [],
                                                          '٫': [],
                                                          '،': [],
                                                          'لا': ['ﻻ', 'ﻼ'],
                                                          '': ['ـ']

                                                          }

_TRANSLATOR = {}
for key, value in _CORRECT_URDU_CHARACTERS_MAPPING.items():
    _TRANSLATOR.update(dict.fromkeys(map(ord, value), key))


def normalize_characters(text: str) -> str:
    """
    The most important module in the UrduHack is the :py:mod:`~urduhack.normalization.character` module,
    defined in the module with the same name. You can use this module separately to normalize
    a piece of text to a proper specified Urdu range (0600-06FF). To get an understanding of how this module works, one
    needs to understand unicode. Every character has a unicode. You can search for any character unicode from any
    language you will find it. No two characters can have the same unicode. This module works with reference to the
    unicodes. Now as urdu language has its roots in Arabic, Parsian and Turkish. So we have to deal with all those
    characters and convert them to a normal urdu character. To get a bit more of what the above explanation means is.::

    >>> all_fes = ['ﻑ', 'ﻒ', 'ﻓ', 'ﻔ', ]
    >>> urdu_fe = 'ف'

    All the characters in all_fes are same but they come from different languages and they all have different unicodes.
    Now as computers deal with numbers, same character appearing in more than one place in a different language will
    have a different unicode and that will create confusion which will create problems in understanding the context of
    the data. :py:mod:`~character` module will eliminate this problem by replacing all the characters in all_fes by
    urdu_fe.

    This provides the functionality to replace wrong arabic characters with correct urdu characters and fixed the
    combine|join characters issue.

    Replace ``urdu`` text characters with correct ``unicode`` characters.

    Args:
        text : ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.normalization import normalize_characters
        >>> # Text containing characters from Arabic Unicode block
        >>> _text = "مجھ کو جو توڑا ﮔیا تھا"
        >>> normalized_text = normalize_characters(_text)
        >>> # Normalized text - Arabic characters are now replaced with Urdu characters
        >>> normalized_text
        مجھ کو جو توڑا گیا تھا
    """
    return text.translate(_TRANSLATOR)


COMBINE_URDU_CHARACTERS: Dict[str, str] = {"آ": "آ",
                                           "أ": "أ",
                                           "ۓ": "ۓ",
                                           }


# Issue to be resolved: Words like کیجئے and کیجیے appear in the same context but they have different unicodes.
# We cannot merge them neither can we have them separately. Because if we decompose ئ,
# we get unicode that are not available in our unicode list.

def normalize_combine_characters(text: str) -> str:
    """
    To normalize combine characters with single character unicode text, use the
    :py:func:`~urduhack.normalization.character.normalize_combine_characters` function in the
    :py:mod:`~urduhack.normalization.character` module.

    Replace combine|join ``urdu`` characters with single unicode character

    Args:
        text : ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.normalization import normalize_combine_characters
        >>> # In the following string, Alif ('ا') and Hamza ('ٔ ') are separate characters
        >>> _text = "جرأت"
        >>> normalized_text = normalize_combine_characters(_text)
        >>> # Now Alif and Hamza are replaced by a Single Urdu Unicode Character!
        >>> normalized_text
        جرأت
    """
    for _key, _value in COMBINE_URDU_CHARACTERS.items():
        text = text.replace(_key, _value)
    return text


def punctuations_space(text: str) -> str:
    """
    Add spaces after punctuations used in ``urdu`` writing

    Args:
        text : ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.normalization.character import punctuations_space
        >>> _text = "ہوتا ہے   ۔  ٹائپ"
        >>> normalized_text = punctuations_space(_text)
        >>> normalized_text
        ہوتا ہے۔ ٹائپ
    """
    text = _SPACE_AFTER_PUNCTUATIONS_RE.sub(' ', text)
    text = _REMOVE_SPACE_BEFORE_PUNCTUATIONS_RE.sub(r'\1', text)
    return text


def remove_diacritics(text: str) -> str:
    """
    Remove ``urdu`` diacritics from text. It is an important step in pre-processing of the Urdu data.
    This function returns a String object which contains the original text minus Urdu diacritics.

    Args:
        text : ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.normalization import remove_diacritics
        >>> _text = "شیرِ پنجاب"
        >>> normalized_text = remove_diacritics(_text)
        >>> normalized_text
        شیر پنجاب
    """
    return _DIACRITICS_RE.sub('', text)


ENG_URDU_DIGITS_MAP: Dict = {
    '0': ['۰'],
    '1': ['۱'],
    '2': ['۲'],
    '3': ['۳'],
    '4': ['۴'],
    '5': ['۵'],
    '6': ['۶'],
    '7': ['۷'],
    '8': ['۸'],
    '9': ['۹']
}

_ENG_DIGITS_TRANSLATOR = {}
for key, value in ENG_URDU_DIGITS_MAP.items():
    _ENG_DIGITS_TRANSLATOR.update(dict.fromkeys(map(ord, value), key))

URDU_ENG_DIGITS_MAP: Dict = {
    '۰': ['0'],
    '۱': ['1'],
    '۲': ['2'],
    '۳': ['3'],
    '۴': ['4'],
    '۵': ['5'],
    '۶': ['6'],
    '۷': ['7'],
    '۸': ['8'],
    '۹': ['9']
}

_URDU_DIGITS_TRANSLATOR = {}
for key, value in URDU_ENG_DIGITS_MAP.items():
    _URDU_DIGITS_TRANSLATOR.update(dict.fromkeys(map(ord, value), key))


def replace_digits(text: str, with_english: bool = True) -> str:
    """
    Replace urdu digits with English digits and vice versa

    Args:
        text : Urdu text string
        with_english (bool): Boolean to convert digits from one language to other
    Returns:
        Text string with replaced digits
    """
    if with_english:
        return text.translate(_ENG_DIGITS_TRANSLATOR)
    return text.translate(_URDU_DIGITS_TRANSLATOR)


def normalize(text: str) -> str:
    """
    To normalize some text, all you need to do pass ``Urdu`` text. It will return a ``str``
    with normalized characters both single and combined, proper spaces after digits and punctuations
    and diacritics removed.

    Args:
        text : ``Urdu`` text
    Returns:
        str: Normalized ``Urdu`` text
    Raises:
        TypeError: If text param is not not str Type.
    Examples:
        >>> from urduhack import normalize
        >>> _text = "اَباُوگل پاکستان ﻤﯿﮟ 20 سال ﺳﮯ ، وسائل کی کوئی کمی نہیں ﮨﮯ۔"
        >>> normalized_text = normalize(_text)
        >>> # The text now contains proper spaces after digits and punctuations,
        >>> # normalized characters and no diacritics!
        >>> normalized_text
        اباوگل پاکستان ﻤﯿﮟ 20 سال ﺳﮯ ، وسائل کی کوئی کمی نہیں ﮨﮯ۔
    """
    if not isinstance(text, str):
        raise TypeError("Text must be str type.")

    logger.info("Normalizing the text.")

    text = remove_diacritics(text)
    text = normalize_characters(text)
    text = normalize_combine_characters(text)
    return text
