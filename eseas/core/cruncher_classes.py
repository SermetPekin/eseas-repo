# ====================================================================
#
# eseas
#
from .utils_general2 import create_dir
from .folder_class import (
    FolderClass,
    DemetraFolder,
    JavaBinFolder,
    WorkspaceFolder,
    CruncherFolder,
)
from .seas_utils import get_absolute

# ====================================================================
import traceback
from pathlib import Path
from rich import print
from evdspy.EVDSlocal.common.file_classes import make_eng
from evdspy.EVDSlocal.utils.utils_general import replace_recursive
import time
import tempfile
import os
from typing import Union


class Cruncher:
    """cruncher"""

    crunch_folder = "."
    local_work_space = "@wspace"
    demetra_folder: str = "."

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Cruncher, cls).__new__(cls)
        return cls.instance

    def set_items(
        self,
        crunch_folder,
        local_work_space,
        demetra_folder,
        workspace_mode=False,
        file_name_explanation=True,
        java_bin=None,
    ):
        """Set Items Cruncher"""

        crunch_folder = str(crunch_folder)
        local_work_space = str(local_work_space)
        demetra_folder = str(demetra_folder)

        self.instance.crunch_folder = get_absolute(crunch_folder)
        self.instance.local_work_space = get_absolute(local_work_space)
        self.demetra_folder = get_absolute(demetra_folder)

        control(
            self
        )  # it will raise if any of the folders does not exist except local workspace folder

        self.workspace_mode = workspace_mode
        self.file_name_explanation = file_name_explanation
        if java_bin:
            java_bin = Path(str(java_bin))
        self.java_bin = java_bin

        self.check_workspace_mode()
        self.set_environ_java(self.java_bin)

    def set_environ_java(self, java_bin: Path):
        from .java_environ import JavaEnviron

        e = JavaEnviron(java_bin)

    def set_itemsObj(self, obj):
        """Set Items Cruncher"""

        self.instance.crunch_folder = get_absolute(obj.crunch_folder)
        self.instance.local_work_space = get_absolute(obj.local_work_space)
        self.demetra_folder = get_absolute(obj.demetra_folder)
        self.java_bin = get_absolute(obj.java_bin)
        control(self)
        self.workspace_mode = obj.workspace_mode
        self.file_name_explanation = obj.file_name_explanation
        self.check_workspace_mode()

    def create_workspace(self):
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
            p = Path() / self.instance.demetra_folder
            p = path_str(p)
            p = make_eng(p)
            return f"@eseas_wspace_{p}"

        if self.workspace_mode:
            ws = self.instance.local_work_space
            n_fname = Path() / ws / naming_format()
            if create_directory(n_fname):
                self.instance.local_work_space = n_fname

    def check_workspace_mode(self):
        # Cruncher
        # TODO SingleOptions().workspace_mode
        try:
            if self.workspace_mode:
                self.create_workspace()
        except Exception as exc:
            print(exc)
            exit()


def show_cruncher_details_raise(cls):
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
    raise CruncherNotSet(msg)


def control(cls):
    if not check_cruncher(cls):
        show_cruncher_details_raise(cls)  # raise


def check_write_permission(folder: Union[str, Path]) -> bool:
    if not os.path.isdir(folder):
        raise NotADirectoryError(folder)
        # return False

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


def check_write_permission_create(folder):
    if not os.path.isdir(folder):
        create_dir(folder)
    return check_write_permission(folder)


def check_cruncher(cls) -> bool:
    msg_if_error = """
    Cruncher will need write permission to
    write permission
        - local workspace
        - java_folder
    read permission
        - demetra folder
    """

    a1 = check_write_permission(Path(cls.instance.crunch_folder))

    a2 = check_write_permission_create(Path(cls.instance.local_work_space))
    # this is for outputs therefore it will be created if it does not exist

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
        time.sleep(3)
        return False
        # raise CruncherNotSet()
    return ok


class CruncherNotSet(BaseException):
    pass


def get_cruncher():
    c = Cruncher()
    control(c)
    assert (
        c.crunch_folder is not None and c.local_work_space is not None
    ), "Cruncher not set!"
    return c


__all__ = [
    "get_cruncher",
    "Cruncher",
]
