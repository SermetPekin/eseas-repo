
# This file is part of the eseas project
# Copyright (C) 2024 Sermet Pekin 
#
# This source code is free software; you can redistribute it and/or
# modify it under the terms of the European Union Public License
# (EUPL), Version 1.2, as published by the European Commission.
#
# You should have received a copy of the EUPL version 1.2 along with this
# program. If not, you can obtain it at:
# <https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12>.
#
# This source code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# European Union Public License for more details.
#
# Alternatively, if agreed upon, you may use this code under any later
# version of the EUPL published by the European Commission.


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
