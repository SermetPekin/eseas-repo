from typing import Iterable
import functools
import traceback
import typing as t
from functools import update_wrapper
from pathlib import Path
from typing import Callable

from evdspy.EVDSlocal.utils.utils_general import replace_recursive

from .json_ops import remove_json_bad_chars


def walk(items: t.Iterable[t.Any], fnc: t.Callable) -> tuple:
    if callable(items):
        items, fnc = fnc, items

    return tuple(map(fnc, items))


def walk2(items: t.Iterable[t.Any], fnc: t.Callable) -> None:
    if callable(items):
        items, fnc = fnc, items
    _ = tuple(map(fnc, items))


def bound(f, *args):
    return update_wrapper(functools.partial(f, *args), f)


def dict_apply(dict_: dict, func: t.Callable, args=None):
    if isinstance(dict_, (tuple, list)):
        return list(map(func, dict_))
    new_dict_ = {}
    for k, v in dict_.items():
        if isinstance(v, str):
            obj = {k: func(v)}
            new_dict_.update(obj)
    return new_dict_


def list_apply(list_: Iterable, func: Callable, args=None):
    return list(func(x) for x in list_)


def tuple_apply(tuple_: tuple, func: Callable, args=None):
    return tuple(func(x) for x in tuple_)


def dict_temizle(dict_: dict, func: t.Callable = remove_json_bad_chars):
    return dict_apply(dict_, func)


def create_dir(folder: str):
    folder = Path(folder)
    if folder.is_dir():
        return
    import os
    return os.makedirs(folder, exist_ok=True)


def clean_file_name(file_name: str):
    file_name = file_name.replace("\n", " ")
    file_name = file_name.replace(":", " ")
    file_name = file_name.replace("'", " ")
    file_name = file_name.replace("$", " ")
    return file_name.replace("\\", "..__")


def deep_temizle_list(content: list) -> tuple:
    return tuple(deep_temizle(x) for x in content)


def deep_temizle(content: str) -> t.Union[str, tuple, list, dict]:
    if isinstance(
            content,
            (
                    list,
                    tuple,
            ),
    ):
        return deep_temizle_list(content)
    if isinstance(content, (dict)):
        return dict_apply(content, deep_temizle)
    import re

    # print(content)
    # reg1 = r'/[a-zA-Z]+/g'
    # reg2 = r'\W+'
    # reg3 = r'^[a-zA-Z0-9_ ]*$'
    reg4 = r"\W+"
    try:
        content = re.sub(reg4, "", content)
    except Exception as exc:
        print(content, type(content))
        print(exc)
    return content


def create_directory(address: Path):
    import os

    try:
        if not Path(address).is_dir():
            os.makedirs(address)
        return True
    except Exception:
        traceback.print_exc()
        return False


def make_eng(text: str) -> str:
    # return text
    dict_ = {
        "s": "s",
        "ç": "c",
        "ı": "i",
        "ü": "u",
        "ö": "o",
        "ğ": "g",
        "İ°": "I",
        "Ş": "S",
        "Ğ": "G",
        "Ç": "C",
        "Ü": "U",
        "Ö": "O",
    }
    return text.translate(text.maketrans(dict_))


def temizle(content: str) -> str:
    chars = ("$", "*", ">", "\xa0", "Ã ", "Ã¢", "Ä", "ÄŸ", "â€™", "'", ":")
    for harf in chars:
        content = replace_recursive(content, harf, "")
    return content


def get_os():
    import platform

    return str(platform.system()).lower()
