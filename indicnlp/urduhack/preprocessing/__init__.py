# coding: utf8
"""
Text PreProcessing
===================

The pre-processing of Urdu text is necessary to make it useful for the machine
learning tasks.
This module provides the following functionality:

    - Normalize whitespace
    - Put Spaces Before & After Digits
    - Put Spaces Before & After English Words
    - Put Spaces  Before & After Urdu Punctuations
    - Replace urls
    - Replace emails
    - Replace number
    - Replace phone_number
    - Replace currency_symbols

You can look for all the different functions that come with pre-process
module in the reference here :py:mod:`~urduhack.preprocess`.

"""
from .character import digits_space, english_characters_space, all_punctuations_space, preprocess
from .util import (normalize_whitespace, replace_urls, replace_emails, replace_numbers, replace_phone_numbers,
                   replace_currency_symbols, remove_punctuation, remove_accents, remove_english_alphabets)

__all__ = ["digits_space", "english_characters_space", "all_punctuations_space", "preprocess", "normalize_whitespace",
           "remove_punctuation", "remove_accents", "replace_urls",
           "replace_emails", "replace_numbers", "replace_phone_numbers",
           "replace_currency_symbols", "remove_english_alphabets", ]
