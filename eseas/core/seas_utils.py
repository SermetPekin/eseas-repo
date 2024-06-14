import typing as t
from pathlib import Path
import os
import random
from typing import Union, Iterable


from evdspy.EVDSlocal.common.file_classes import FileItem
from evdspy.EVDSlocal.common.colors import (
    print_excel_created_style,
    print_with_info_style,
    print_with_updating_style,
    print_with_success_style,
)

from ._options import max_num


color_funcs = (
    print_excel_created_style,
    print_with_info_style,
    print_with_updating_style,
    print_with_success_style,
    print,
)


def get_print_color() -> callable:
    return random.choice(color_funcs)


def display_line(line):
    indent = "" * 15
    result = f"{indent}{line}"
    return result


def display_lines(lines):
    st: str = "\n".join(tuple(map(display_line, lines)))
    func = get_print_color()
    func(st)


def view_display(*msg):
    for item in msg:
        item = str(item)
        display_lines(item.splitlines())


class SingleOptions:
    """SingleOptions"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingleOptions, cls).__new__(cls)
        return cls.instance

    def set_items(cls, options):
        cls.instance.options = options


def get_absolute(folder: str):
    p = Path(folder)
    return Path(p.absolute())


def clean_file_name(file_name: str):
    file_name = file_name.replace("\n", " ")
    file_name = file_name.replace(":", " ")
    file_name = file_name.replace("'", " ")
    file_name = file_name.replace("$", " ")
    return file_name.replace("\\", "..__")


def filter_xls(items: t.List[FileItem]):
    def check(item):
        def check_this(ext):
            return str(item).endswith(ext)

        return any(
            map(
                check_this,
                (
                    "xlsx",
                    "xlsm",
                    "xls",
                ),
            )
        )

    return tuple(x for x in items if check(x.full_name))


def filter_xml(items: t.List[FileItem]):
    return tuple(x for x in items if str(x.full_name).endswith("xml"))


def list_of_folders(folder: Union[str, Path]) -> list[str]:
    import os

    def check(d):
        return os.path.isdir(os.path.join(folder, d))

    return [d for d in os.listdir(folder) if check(d)]


def filter_xml_demetra(items: t.List[FileItem]):
    def stem(file_item: FileItem):
        return str(file_item.full_name.stem)

    def check_demetra(file_item: FileItem):
        """
        SomeFolder_JDemtra.xml
        Calendars.xml
        SAProcessing-1.xml
        Vars-1.xml
        """

        def check_if_folder_exists() -> bool:
            folders = list_of_folders(file_item.dir_path)
            fname = file_item.full_name
            if not hasattr(file_item, "short_name"):
                if str(fname).endswith(".xml"):
                    file_item.short_name = fname.stem
                else:

                    return False

            return file_item.short_name in folders

        def check_all_parts(part_func: t.Callable):
            def check_this_part(item: str):
                part: str = part_func(file_item)
                result = item.strip().lower() in part.strip().lower()
                return result

            return any(
                map(
                    check_this_part,
                    (
                        "jdemtra",
                        "demetra",
                        "seas_adj",
                    ),
                )
            )

        return any(map(check_all_parts, (stem,))) or check_if_folder_exists()

    items = filter_xml(items)

    return list(x for x in items if check_demetra(x))


class MaxFileNumberReached(BaseException):
    ...


def list_files_recursive(folder: t.Union[str, Path]) -> list[FileItem]:
    res = []
    break_loop = False
    if not Path(folder).is_dir():
        raise FileNotFoundError(folder)
    try:
        for dir_path, dir_names, file_names in os.walk(folder):
            print(f"{folder}>> {dir_path}   ")
            for file_name in file_names:
                if break_loop:
                    break
                file_item = FileItem(dir_path, file_name)
                if max_num < len(file_item.created_items):
                    view_display(
                        "limit max number reached  you "
                        " may change it from search_main.py file "
                    )
                    n = len(file_item.created_items)
                    raise MaxFileNumberReached(f"Max{n}")
                res.append(file_item)
    except MaxFileNumberReached:
        print("max number reached... returning limit number of files...")
    return res


def display(some_files: Iterable[FileItem], max_num=10):
    template = ""
    msg = f"""
=====================================================
        Number of files found :  {len(some_files)}
=====================================================
    """
    template += msg + chr(10)
    for index, item in enumerate(some_files):
        if index < max_num:
            template += item.file_name + chr(10)
    view_display(template)


def search_demetra_folder(
    root: t.Union[str, Path] = None,
    filter_func: callable = None,
) -> list[FileItem]:
    if not root:
        raise ValueError
    f = list_files_recursive(root)
    if not f or not callable(filter_func):
        return f

    files_filtered = filter_func(f)
    return files_filtered


def get_type_of_files_demetra(folder, filter_func=filter_xls):
    files = search_demetra_folder(folder, filter_func)
    return files


def get_type_of_files(folder, filter_func=filter_xls):
    files = search_demetra_folder(folder, filter_func)  # search_folders()
    return files


def get_xml_demetra(folder) -> list[FileItem]:
    return get_type_of_files_demetra(folder, filter_xml_demetra)
