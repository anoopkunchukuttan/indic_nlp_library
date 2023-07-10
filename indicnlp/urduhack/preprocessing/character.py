# coding: utf8
"""
Urduhack Character preprocess functions
"""

from .regexes import _SPACE_AFTER_ALL_PUNCTUATIONS_RE, _SPACE_BEFORE_ALL_PUNCTUATIONS_RE
from .regexes import _SPACE_AFTER_DIGITS_RE, _SPACE_BEFORE_DIGITS_RE
from .regexes import _SPACE_BEFORE_ENG_CHAR_RE, _SPACE_AFTER_ENG_CHAR_RE


def digits_space(text: str) -> str:
    """
    Add spaces before|after numeric and urdu digits

    Args:
        text (str): ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.preprocessing import digits_space
        >>> text = "20فیصد"
        >>> normalized_text = digits_space(text)
        >>> normalized_text
        20 فیصد
    """
    text = _SPACE_BEFORE_DIGITS_RE.sub(' ', text)
    text = _SPACE_AFTER_DIGITS_RE.sub(' ', text)

    return text


def english_characters_space(text: str) -> str:
    """
    Functionality to add spaces before and after English words in the given Urdu text. It is an important step in
    normalization of the Urdu data.

    this function returns a :py:class:`String` object which contains the original text with spaces before & after
    English words.

    Args:
        text (str): ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.preprocessing import english_characters_space
        >>> text = "خاتون Aliyaنے بچوںUzma and Aliyaکے قتل کا اعترافConfession کیا ہے۔"
        >>> normalized_text = english_characters_space(text)
        >>> normalized_text
        خاتون Aliya نے بچوں Uzma and Aliya کے قتل کا اعتراف Confession کیا ہے۔
    """
    text = _SPACE_BEFORE_ENG_CHAR_RE.sub(' ', text)
    text = _SPACE_AFTER_ENG_CHAR_RE.sub(' ', text)

    return text


def all_punctuations_space(text: str) -> str:
    """
    Add spaces after punctuations used in ``urdu`` writing

    Args:
        text (str): ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    """
    text = _SPACE_BEFORE_ALL_PUNCTUATIONS_RE.sub(' ', text)
    text = _SPACE_AFTER_ALL_PUNCTUATIONS_RE.sub(' ', text)
    return text


def preprocess(text: str) -> str:
    """
    To preprocess some text, all you need to do pass ``unicode`` text. It will return a ``str``
    with proper spaces after digits and punctuations.

    Args:
        text (str): ``Urdu`` text
    Returns:
        str: urdu text
    Raises:
        TypeError: If text param is not not str Type.
    Examples:
        >>> from urduhack.preprocessing import preprocess
        >>> text = "اَباُوگل پاکستان ﻤﯿﮟ 20 سال ﺳﮯ ، وسائل کی کوئی کمی نہیں ﮨﮯ۔"
        >>> normalized_text = preprocess(text)
        >>> # The text now contains proper spaces after digits and punctuations,
        >>> # normalized characters and no diacritics!
        >>> normalized_text
        اباوگل پاکستان ﻤﯿﮟ 20 سال ﺳﮯ ، وسائل کی کوئی کمی نہیں ﮨﮯ ۔
    """
    if not isinstance(text, str):
        raise TypeError("text must be str type.")

    text = digits_space(text)
    text = all_punctuations_space(text)
    text = english_characters_space(text)
    return text
