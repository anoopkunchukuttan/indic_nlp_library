# coding: utf8
"""
This module provides the functionality to generate tokens (both sentence and word wise) from Urdu text.
"""

from typing import List

from .eos import _generate_sentences


def sentence_tokenizer(text: str) -> List[str]:
    """
    Convert ``Urdu`` text into possible sentences.
    If successful, this function returns a :py:class:`List` object containing multiple urdu :py:class:`String`
    sentences.

    Args:
        text (str): ``Urdu`` text
    Returns:
        list: Returns a ``list`` object containing multiple urdu sentences type ``str``.
    Raises:
        TypeError: If text is not a str Type
    Examples:
        >>> from urduhack.tokenization import sentence_tokenizer
        >>> text = "عراق اور شام نے اعلان کیا ہے دونوں ممالک جلد اپنے اپنے سفیروں کو واپس بغداد اور دمشق بھیج دیں گے؟"
        >>> sentences = sentence_tokenizer(text)
        >>> sentences
        ["دونوں ممالک جلد اپنے اپنے سفیروں کو واپس بغداد اور دمشق بھیج دیں گے؟" ,"عراق اور شام نے اعلان کیا ہے۔"]
    """
    if not isinstance(text, str):
        raise TypeError("text parameter must be str type.")

    return _generate_sentences(text)
