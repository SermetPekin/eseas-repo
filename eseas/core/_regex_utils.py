import functools
import re
from .utils_general2 import list_apply, tuple_apply, dict_apply

strategies = {"strict": r"\W+", "light": r"^[a-zA-Z0-9_ ]", "medium": r"\W+ "}


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
