# coding: utf8
"""Rule based Sentence tokenization module"""

# Global Variables
_URDU_CONJUNCTIONS = [
    "جنہیں",
    "جس",
    "جن",
    "جو",
    "اور",
    "اگر",
    "اگرچہ",
    "لیکن",
    "مگر",
    "پر",
    "یا",
    "تاہم",
    "کہ",
    "کر",
    "تو",
    "گے",
    "گی",
]
_URDU_NEWLINE_WORDS = [
    "کیجیے",
    "کیجئے",
    "گئیں",
    "تھیں",
    "ہوں",
    "خریدا",
    "گے",
    "ہونگے",
    "گا",
    "چاہیے",
    "ہوئیں",
    "گی",
    "تھا",
    "تھی",
    "تھے",
    "ہیں",
    "ہے",
]


def _split_and_keep(_str, separator):
    """Replace end of sentence with separator"""
    if not _str:
        return []
    max_p = chr(ord(max(_str)) + 1)
    return _str.replace(separator, separator + max_p).split(max_p)


def _generate_sentences(text: str) -> list:
    """Generate a list of urdu sentences from a given string.
    This function automatically fixes multiple whitespaces
    or new lines so you just need to pass the data and
    get sentences in return.

    Args:
        text (str): base string
    Returns:
        list
    """
    all_sentences = []
    sentences = _split_and_keep(text, "۔")

    for sentence in sentences:  # pylint: disable=too-many-nested-blocks
        if sentence and (len(sentence.split()) >= 2):
            if "؟" in sentence:
                q_sentences = _split_and_keep(sentence, "؟")
                for _sen in q_sentences:
                    _sen = _sen.split()
                    new_sent = ""
                    is_cont = False

                    for index, word in enumerate(_sen):
                        if is_cont:
                            is_cont = False
                            continue

                        if (
                            word in _URDU_NEWLINE_WORDS
                            and index + 1 < len(_sen)
                            and _sen[index + 1] not in _URDU_CONJUNCTIONS
                        ):
                            if index + 1 < len(_sen) and _sen[index + 1] in ["۔", "،"]:
                                new_sent += " " + word + " " + _sen[index + 1] + "\n"
                                is_cont = True
                            else:
                                new_sent += " " + word + "\n"

                        else:
                            new_sent += " " + word

                    for sen in new_sent.split("\n"):
                        if sen and len(sen.split()) >= 2:
                            all_sentences.append(sen.strip())

            else:
                sentence = sentence.split()
                new_sent = ""
                is_cont = False

                for index, word in enumerate(sentence):
                    if is_cont:
                        is_cont = False
                        continue

                    if (
                        word in _URDU_NEWLINE_WORDS
                        and index + 1 < len(sentence)
                        and sentence[index + 1] not in _URDU_CONJUNCTIONS
                    ):
                        if index + 1 < len(sentence) and sentence[index + 1] in [
                            "۔",
                            "،",
                        ]:
                            new_sent += " " + word + " " + sentence[index + 1] + "\n"
                            is_cont = True
                        else:
                            new_sent += " " + word + "\n"
                    else:
                        new_sent += " " + word

                for sen in new_sent.split("\n"):
                    if sen and len(sen.split()) >= 2:
                        all_sentences.append(sen.strip())

    return all_sentences
