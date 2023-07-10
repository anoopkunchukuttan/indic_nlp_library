# coding: utf8
"""
Preprocessing utilities
"""

import sys
import unicodedata

import regex as re

CURRENCIES = {'$': 'USD', 'zł': 'PLN', '£': 'GBP', '¥': 'JPY', '฿': 'THB',
              '₡': 'CRC', '₦': 'NGN', '₩': 'KRW', '₪': 'ILS', '₫': 'VND',
              '€': 'EUR', '₱': 'PHP', '₲': 'PYG', '₴': 'UAH', '₹': 'INR'}

_EMAIL_RE = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}(?:$|(?=\b))",
    flags=re.IGNORECASE | re.UNICODE)
_PHONE_RE = re.compile(r'(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?(\d{3}[ .-]?\d{4})(\s?(?:ext\.?'
                       r'|[#x-])\s?\d{2,6})?(?:$|(?=\W))')
_NUMBERS_RE = re.compile(r'(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)'
                         r'|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))')
_CURRENCY_RE = re.compile('({})+'.format('|'.join(re.escape(c) for c in CURRENCIES)))
_LINEBREAK_RE = re.compile(r'((\r\n)|[\n\v])+')
_NONBREAKING_SPACE_RE = re.compile(r'(?!\n)\s+')
_URL_RE = re.compile(r"(?:^|(?<![\w/.]))"
                     # protocol identifier
                     # r"(?:(?:https?|ftp)://)"  <-- alt?
                     r"(?:(?:https?://|ftp://|www\d{0,3}\.))"
                     # user:pass authentication
                     r"(?:\S+(?::\S*)?@)?"
                     r"(?:"
                     # IP address exclusion
                     # private & local networks
                     r"(?!(?:10|127)(?:\.\d{1,3}){3})"
                     r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
                     r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
                     # IP address dotted notation octets
                     # excludes loopback network 0.0.0.0
                     # excludes reserved space >= 224.0.0.0
                     # excludes network & broadcast addresses
                     # (first & last IP address of each class)
                     r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
                     r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
                     r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
                     r"|"
                     # host name
                     r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
                     # domain name
                     r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
                     # TLD identifier
                     r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
                     r")"
                     # port number
                     r"(?::\d{2,5})?"
                     # resource path
                     r"(?:/\S*)?"
                     r"(?:$|(?![\w?!+&/]))",
                     flags=re.UNICODE | re.IGNORECASE)  # source: https://gist.github.com/dperini/729294
_SHORT_URL_RE = re.compile(r"(?:^|(?<![\w/.]))"
                           # optional scheme
                           r"(?:(?:https?://)?)"
                           # domain
                           r"(?:\w-?)*?\w+(?:\.[a-z]{2,12}){1,3}"
                           r"/"
                           # hash
                           r"[^\s.,?!'\"|+]{2,12}"
                           r"(?:$|(?![\w?!+&/]))",
                           flags=re.IGNORECASE)


def normalize_whitespace(text: str):
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more linebreaks with a single newline. Also strip leading/trailing whitespace.

    Args:
        text (str): ``Urdu`` text
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.preprocessing import normalize_whitespace
        >>> text = "عراق اور شام     اعلان کیا ہے دونوں         جلد اپنے     گے؟"
        >>> normalized_text = normalize_whitespace(text)
        >>> normalized_text
        عراق اور شام اعلان کیا ہے دونوں جلد اپنے گے؟
    """
    return _NONBREAKING_SPACE_RE.sub(' ', _LINEBREAK_RE.sub(r'\n', text)).strip()


def replace_urls(text: str, replace_with=''):
    """
    Replace all URLs in ``text`` str with ``replace_with`` str.

    Args:
        text (str): ``Urdu`` text
        replace_with (str): Replace string
    Returns:
        str: Returns a ``str`` object replace url with ``replace_with`` text.
    Examples:
        >>> from urduhack.preprocessing import replace_urls
        >>> text = "20 www.gmail.com  فیصد"
        >>> replace_urls(text)
        '20  فیصد'
    """
    return _URL_RE.sub(replace_with, _SHORT_URL_RE.sub(replace_with, text))


def replace_emails(text: str, replace_with=''):
    """
    Replace all emails in ``text`` str with ``replace_with`` str.

    Args:
        text (str): ``Urdu`` text
        replace_with (str): Replace string
    Returns:
        str: Returns a ``str`` object replace emails with ``replace_with`` text.
    Examples:
        >>> text = "20 gunner@gmail.com  فیصد"
        >>> from urduhack.preprocessing import replace_emails
        >>> replace_emails(text)
    """
    return _EMAIL_RE.sub(replace_with, text)


def replace_phone_numbers(text: str, replace_with=''):
    """
    Replace all phone numbers in ``text`` str with ``replace_with`` str.

    Args:
        text (str): ``Urdu`` text
        replace_with (str): Replace string
    Returns:
        str: Returns a ``str`` object replace number_no with ``replace_with`` text.
    Examples:
        >>> from urduhack.preprocessing import replace_numbers
        >>> text = "20  فیصد"
        >>> replace_numbers(text)
        ' فیصد'
    """
    return _PHONE_RE.sub(replace_with, text)


def replace_numbers(text: str, replace_with=''):
    """
    Replace all numbers in ``text`` str with ``replace_with`` str.

    Args:
        text (str): ``Urdu`` text
        replace_with (str): Replace string
    Returns:
        str: Returns a ``str`` object replace number with ``replace_with`` text.
    Examples:
        >>> from urduhack.preprocessing import replace_phone_numbers
        >>> text = "یعنی لائن آف کنٹرول پر فائربندی کا معاہدہ 555-123-4567 میں ہوا تھا"
        >>> replace_phone_numbers(text)
        'یعنی لائن آف کنٹرول پر فائربندی کا معاہدہ میں ہوا تھا'
    """
    return _NUMBERS_RE.sub(replace_with, text)


def replace_currency_symbols(text: str, replace_with=None):
    """
    Replace all currency symbols in ``text`` str with string specified by ``replace_with`` str.

    Args:
        text (str): Raw text
        replace_with (str): if None (default), replace symbols with
            their standard 3-letter abbreviations (e.g. '$' with 'USD', '£' with 'GBP');
            otherwise, pass in a string with which to replace all symbols
            (e.g. "*CURRENCY*")
    Returns:
        str: Returns a ``str`` object containing normalized text.
    Examples:
        >>> from urduhack.preprocessing import replace_currency_symbols
        >>> text = "یعنی لائن آف کنٹرول پر فائربندی کا معاہدہ 2003 میں ہوا 33$ تھا۔"
        >>> replace_currency_symbols(text)
    'یعنی لائن آف کنٹرول پر فائربندی کا معاہدہ 2003 میں ہوا 33USD تھا۔'
    """
    if replace_with is None:
        for key, value in CURRENCIES.items():
            text = text.replace(key, value)
        return text

    return _CURRENCY_RE.sub(replace_with, text)


PUNCTUATION_TRANSLATE_UNICODE = dict.fromkeys((i for i in range(sys.maxunicode)
                                               if unicodedata.category(chr(i)).startswith('P')), '')


def remove_punctuation(text: str, marks=None) -> str:
    """
    Remove punctuation from ``text`` by removing all instances of ``marks``.

    Args:
        text (str): Urdu text
        marks (str): If specified, remove only the characters in this string,
            e.g. ``marks=',;:'`` removes commas, semi-colons, and colons.
            Otherwise, all punctuation marks are removed.
    Returns:
        str: returns a ``str`` object containing normalized text.
    Note:
        When ``marks=None``, Python's built-in :meth:`str.translate()` is
        used to remove punctuation; otherwise, a regular expression is used
        instead. The former's performance is about 5-10x faster.
    Examples:
        >>> from urduhack.preprocessing import remove_punctuation
        >>> output = remove_punctuation("کر ؟ سکتی ہے۔")
        کر سکتی ہے

    """
    if marks:
        return re.sub('[{}]+'.format(re.escape(marks)), '', text, flags=re.UNICODE)

    return text.translate(PUNCTUATION_TRANSLATE_UNICODE)


def remove_accents(text: str) -> str:
    """
    Remove accents from any accented unicode characters in ``text`` str, either by
    transforming them into ascii equivalents or removing them entirely.

    Args:
        text (str): Urdu text
    Returns:
        str
    Examples:
        >>> from urduhack.preprocessing import remove_accents
        >>>text = "دالتِ عظمیٰ درخواست"
        >>> remove_accents(text)
    'دالت عظمی درخواست'
    """
    return ''.join(c for c in text if not unicodedata.combining(c))


def remove_english_alphabets(text: str):
    """
    Removes ``English`` words and digits from a ``text``

    Args:
         text (str): Urdu text
    Returns:
        str: ``str`` object with english alphabets removed
    """
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    table = str.maketrans({key: None for key in characters})
    return text.translate(table)
