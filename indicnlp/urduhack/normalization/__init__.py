# coding: utf8
"""
Normalization
==============

The normalization of Urdu text is necessary to make it useful for the machine
learning tasks. In the :py:mod:`~urduhack.normalization.normalize` module, the very basic
problems faced when working with Urdu data are handled with ease and
efficiency. All the problems and how :py:mod:`~urduhack.normalization.normalize` module handles
them are listed below.

This modules fixes the problem of correct encodings for the Urdu characters as well as replace Arabic
characters with correct Urdu characters. This module brings all the characters in the specified unicode range
(0600-06FF) for Urdu language.

It also fixes the problem of joining of different Urdu words. By joining we mean that when space between two Urdu words
is removed, they must not make a new word. Their rendering must not change and even after the removal of space
they should look the same.

You can use the library to normalize the Urdu text for correct unicode characters.
By normalization we mean to end the confusion between Urdu and Arabic characters,
to replace two words with one word keeping in mind the context they are used in.
Like the character 'ﺁ' and 'ﺂ' are to be replaced by 'آ'. All this is done using regular expressions.

The normalization of Urdu text is necessary to make it useful for the machine learning tasks.
This module provides the following functionality:

    - Normalizing Single Characters
    - Normalizing Combine Characters
    - Removal of Diacritics from Urdu Text
    - Replace all digits with Urdu and vice versa English
"""
from .character import normalize_characters, normalize_combine_characters, \
    remove_diacritics, replace_digits, normalize

__all__ = ["normalize", "normalize_characters", "normalize_combine_characters", "remove_diacritics", "replace_digits"]
