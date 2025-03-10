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


import json
from pathlib import Path
import typing as t


def dict_apply(dict_: dict, func: t.Callable, args=None):
    if isinstance(dict_, (tuple, list)):
        return list(map(func, dict_))
    new_dict_ = {}
    for k, v in dict_.items():
        if isinstance(v, str):
            obj = {k: func(v)}
            new_dict_.update(obj)
    return new_dict_


def remove_json_bad_chars(json_object_str):
    if isinstance(json_object_str, (tuple, list)):
        return list(map(remove_json_bad_chars, json_object_str))
    if isinstance(json_object_str, (dict)):
        return dict_apply(json_object_str, remove_json_bad_chars)
    bad_chars = ("$", "%", "&", "?", "Ä", "ÄŸ")
    replace_chars = ("USD", "PERCENT", "AMPERSTAND", "QUESTIONMARK", "G", "g")
    for index, bad_char in enumerate(bad_chars):
        new_char = replace_chars[index]
        json_object_str = replace_recursive_json(json_object_str, bad_char, new_char)
    return json_object_str


def replace_recursive_json(text: str, char: str, new_char: str):
    parts = text.split(char)
    return new_char.join(parts)


def create_json_file(json_dict: dict, file_name="file_and_cols.js"):
    json_object_str: str = json.dumps(json_dict, ensure_ascii=False)
    json_object_str = "file_and_cols='" + json_object_str + "'"
    json_file_name = Path() / file_name
    from evdspy.EVDSlocal.common.files import Write

    print("writing....", json_file_name)
    result, msg = Write(Path() / json_file_name, json_object_str)
    print(result, msg)
    result, msg = Write(Path(r"some_folder/json") / json_file_name, json_object_str)
    print(result, msg)
