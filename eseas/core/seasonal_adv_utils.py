import sys
from pathlib import Path

from evdspy.EVDSlocal.common.file_classes import FileItem
from .seas_testing_utils import get_env_java_folder
from .seas_utils import view_display


def this_is_pytest() -> bool:
    """
    Sometimes we need to check if it is pytest
    in order to avoid tests to break
    """

    def check():
        path_ = Path(sys.argv[0])
        return "pytest" in str(path_.stem)

    if len(sys.argv) > 0 and check():
        return True
    return False


def get_input_both(msg="Your choice", default_answer="y") -> str:
    """
    using input function causes pytest to raise error
    we need to check if it is pytest
    """
    view_display(msg)
    if this_is_pytest():  # pytest
        return default_answer
    if get_env_java_folder():  # Probably Docker
        return default_answer
    return input()


def get_input_from_user() -> bool:
    msg = """
==========================================================================
    Confirm running `jwsacruncher` for seasonal adjusment ?
           ( if you prefer running manually instead, you may do so by calling
             batch file that was created by this script )

==========================================================================
?(y/N)
    """
    ans = get_input_both(msg, "y")
    if str(ans).lower() in (
        "y",
        "yes",
    ):
        return True
    else:
        return False


def display(items: list[FileItem]) -> tuple:
    def print_spec(item: FileItem):
        template = f"""
---------------- Detail -------------------------
dir       : {item.dir_path}
file_name : {item.file_name}
-------------------------------------------------
        """
        view_display(template)
        return template

    return tuple(map(print_spec, items))


def common_space_msg(test, demetra_folder):
    return f"""
========================================================================
        common_space_check has run
test : {test}
folder to check demetra files : {demetra_folder}
========================================================================
"""


def seasonal_results_msg(test):
    return f"""
========================================================================
        seasonal_results function is running.
        test : {test}
        Collecting results
========================================================================
    """


def get_results_info(adres):
    t = f"""
    --------------------------
    {adres}
    """
    return t
