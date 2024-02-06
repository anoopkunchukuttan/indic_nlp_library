# coding: utf8
"""List of Regex"""

import regex as re

from indicnlp.urduhack.urdu_characters import URDU_PUNCTUATIONS, URDU_DIACRITICS

# Add spaces after ., if there is number then not Ex (9.00)
_SPACE_AFTER_PUNCTUATIONS_RE = re.compile(
    r"(?<=["
    + "".join(URDU_PUNCTUATIONS)
    + "])(?=[^"
    + "".join(URDU_PUNCTUATIONS)
    + "0-9 \n])",
    flags=re.U | re.M | re.I,
)
_REMOVE_SPACE_BEFORE_PUNCTUATIONS_RE = re.compile(
    r"\s+([" + "".join(URDU_PUNCTUATIONS) + "])", flags=re.U | re.M | re.I
)

_DIACRITICS_RE = re.compile(f'[{"".join(URDU_DIACRITICS)}]', flags=re.U | re.M | re.I)
