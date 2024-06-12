import functools
import random
import re
from .utils_general2 import list_apply, tuple_apply, dict_apply

strategies = {"strict": r"\W+", "light": r"^[a-zA-Z0-9_ ]", "medium": r"\W+ "}
valid_chars_JSON = (
    """ . """ "d",
    "a",
    "t",
    "f",
    "i",
    "h",
    "r",
    "s",
    "=",
    "'",
    "{",
    '"',
    "b",
    "e",
    "_",
    "p",
    "y",
    "o",
    ":",
    " ",
    "[",
    "S",
    "E",
    "R",
    "I",
    "C",
    "O",
    "D",
    "T",
    "P",
    "A",
    "1",
    "2",
    ",",
    "G",
    "U",
    "N",
    "M",
    "Y",
    "L",
    "K",
    "ÄŸ",
    "Ä±",
    "l",
    "k",
    "m",
    "F",
    "z",
    "H",
    "W",
    "g",
    "v",
    "n",
    "Q",
    "B",
    "V",
    "0",
    "5",
    "9",
    "8",
    "}",
    "3",
    "7",
    "Ãœ",
    "4",
    "ÅŸ",
    "u",
    "c",
    "]",
    "Ä°",
    "Å",
    "Z",
    "Ã¼",
    "q",
    "6",
    "w",
    "Ã§",
    "Ã¶",
    "x",
    "Ã‡",
    "X",
    "Ä",
    "J",
    "j",
    "Ã–",
    "Ã¢",
    "Ã ",
    " ",
    "-",
)


def base_replace(string, level="strict"):
    bound_func = functools.update_wrapper(
        functools.partial(base_replace, level=level), base_replace
    )
    if isinstance(string, (list,)):
        return list_apply(string, bound_func)
    if isinstance(string, (tuple,)):
        return tuple_apply(string, bound_func)
    if isinstance(string, (dict,)):
        return dict_apply(string, bound_func)
    reg_strategy = strategies[level]
    return re.sub(reg_strategy, "_", string)


def replace_strict(string):
    return base_replace(string, "strict")


def replace_light(string):
    return base_replace(string, "light")


def replace_medium(string):
    return base_replace(string, "medium")
