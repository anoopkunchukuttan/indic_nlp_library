# coding: utf8
"""Rule based Sentence tokenization module"""

# Global Variables
_URDU_CONJUNCTIONS = frozenset(
    [
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
)
_URDU_NEWLINE_WORDS = frozenset(
    [
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
)


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
                    _sen_parts = _sen.split()
                    new_sent_list = []
                    is_cont = False

                    for index, word in enumerate(_sen_parts):
                        if is_cont:
                            is_cont = False
                            continue

                        if (
                            word in _URDU_NEWLINE_WORDS
                            and index + 1 < len(_sen_parts)
                            and _sen_parts[index + 1] not in _URDU_CONJUNCTIONS
                        ):
                            if index + 1 < len(_sen_parts) and _sen_parts[
                                index + 1
                            ] in ["۔", "،"]:
                                new_sent_list.append(
                                    " " + word + " " + _sen_parts[index + 1] + "\\n"
                                )
                                is_cont = True
                            else:
                                new_sent_list.append(" " + word + "\\n")

                        else:
                            new_sent_list.append(" " + word)

                    new_sent_str = "".join(new_sent_list)
                    for sen_part in new_sent_str.split("\\n"):
                        if sen_part and len(sen_part.split()) >= 2:
                            all_sentences.append(sen_part.strip())

            else:
                sentence_parts = sentence.split()
                new_sent_list = []
                is_cont = False

                for index, word in enumerate(sentence_parts):
                    if is_cont:
                        is_cont = False
                        continue

                    if (
                        word in _URDU_NEWLINE_WORDS
                        and index + 1 < len(sentence_parts)
                        and sentence_parts[index + 1] not in _URDU_CONJUNCTIONS
                    ):
                        if index + 1 < len(sentence_parts) and sentence_parts[
                            index + 1
                        ] in [
                            "۔",
                            "،",
                        ]:
                            new_sent_list.append(
                                " " + word + " " + sentence_parts[index + 1] + "\\n"
                            )
                            is_cont = True
                        else:
                            new_sent_list.append(" " + word + "\\n")
                    else:
                        new_sent_list.append(" " + word)

                new_sent_str = "".join(new_sent_list)
                for sen_part in new_sent_str.split("\\n"):
                    if sen_part and len(sen_part.split()) >= 2:
                        all_sentences.append(sen_part.strip())

    return all_sentences
