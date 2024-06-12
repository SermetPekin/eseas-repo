import traceback
from pathlib import Path
from rich import print
from .seas_utils import get_absolute
from evdspy.EVDSlocal.common.file_classes import make_eng
from evdspy.EVDSlocal.utils.utils_general import replace_recursive
import time
import tempfile
import os
from typing import Union


class Cruncher:
    """cruncher"""

    crunch_folder = False
    local_work_space = "@wspace"
    demetra_folder: str = "."

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Cruncher, cls).__new__(cls)
        return cls.instance

    def set_items(
        cls,
        crunch_folder,
        local_work_space,
        demetra_folder,
        workspace_mode=False,
        file_name_explanation=True,
    ):
        """Set Items Cruncher"""
        cls.instance.crunch_folder = get_absolute(crunch_folder)
        cls.instance.local_work_space = get_absolute(local_work_space)
        cls.demetra_folder = get_absolute(demetra_folder)
        control(cls)
        cls.workspace_mode = workspace_mode
        cls.file_name_explanation = file_name_explanation
        cls.check_workspace_mode()

    def set_itemsObj(cls, obj):
        """Set Items Cruncher"""

        cls.instance.crunch_folder = get_absolute(obj.crunch_folder)
        cls.instance.local_work_space = get_absolute(obj.local_work_space)
        cls.demetra_folder = get_absolute(obj.demetra_folder)
        control(cls)
        cls.workspace_mode = obj.workspace_mode
        cls.file_name_explanation = obj.file_name_explanation
        cls.check_workspace_mode()

    def create_workspace(cls):
        def create_directory(address: Path):
            import os

            try:
                if not Path(address).is_dir():
                    os.makedirs(address)
                return True
            except Exception:
                traceback.print_exc()
                return False

        def path_str(Path_: Path):
            r = replace_recursive(str(Path_), "\\", ".")
            r = replace_recursive(r, ":", "..")
            return r

        def naming_format():
            p = Path() / cls.instance.demetra_folder
            p = path_str(p)
            p = make_eng(p)
            return f"@eseas_wspace_{p}"

        if cls.workspace_mode:
            new_folder_name = Path() / cls.instance.local_work_space / naming_format()
            if create_directory(new_folder_name):
                cls.instance.local_work_space = new_folder_name

    def check_workspace_mode(cls):
        # Cruncher
        # TODO SingleOptions().workspace_mode
        try:
            if cls.workspace_mode:
                cls.create_workspace()
        except Exception as exc:
            print(exc)
            exit()


def control(cls):
    global checked
    if not check_cruncher(cls):

        def check(folder: str):
            if Path(folder).is_dir():
                return "exists"
            return "does not exist!"

        msg = f"""\n\n
_______________________________________________________________       
Could not find some folders.  
_______________________________________________________________
    java_folder     : [{check(cls.instance.crunch_folder)}] 
                      {cls.instance.crunch_folder}   
    local_workspace : [{check(cls.instance.local_work_space)}] 
                      {cls.instance.local_work_space}  
    demetra_folder  : [{check(cls.instance.demetra_folder)}] 
                      {cls.instance.demetra_folder} 
"""
        raise ChruncerNotSet(msg)
    else:
        checked = True


def check_write_permission(folder: Union[str, Path]) -> bool:
    if not os.path.isdir(folder):
        raise NotADirectoryError(folder)
        return False

    try:
        testfile = tempfile.TemporaryFile(dir=folder)
        testfile.close()
        return True
    except (OSError, IOError):
        return False


def check_read_permission(folder: Union[str, Path]) -> bool:
    if not os.path.isdir(folder):
        raise NotADirectoryError(folder)
        # return False
    return os.access(folder, os.R_OK)


def check_cruncher(cls):
    msg_if_error = """
    Cruncher will need write permission to
    write permission
        - local workspace
        - java_folder
    read permission
        - demetra folder
    """

    a1 = check_write_permission(Path(cls.instance.crunch_folder))
    a2 = check_write_permission(Path(cls.instance.local_work_space))
    a3 = check_read_permission(Path(cls.instance.demetra_folder))
    ok = all(
        (
            a1,
            a2,
            a3,
        )
    )
    if not ok:
        print(msg_if_error)
        time.sleep(5)
        raise ChruncerNotSet()
    return ok


class ChruncerNotSet(BaseException):
    pass


def get_cruncher():
    c = Cruncher()
    control(c)
    assert (
        c.crunch_folder is not None and c.local_work_space is not None
    ), "Chruncer not set!"
    return c


__all__ = [
    "get_cruncher",
    "Cruncher",
]
