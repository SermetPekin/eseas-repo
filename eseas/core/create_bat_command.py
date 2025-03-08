import subprocess
from pathlib import Path
import shutil
from typing import Iterable


from evdspy.EVDSlocal.common.file_classes import FileItem
from ._options import middle_folder
from .utils_general2 import get_os

if __name__ != "__main__":
    from ._general_params import _create_general_params
    from .cruncher_classes import get_cruncher
    from .demetra_caller import (
        DemetraCallerLinux,
        DemetraCallerMac,
        DemetraCallerWindows,
    )

NEW_LINE = chr(10)


os_str = get_os()


def get_demetra_type():
    if get_os() == "windows":
        return DemetraCallerWindows()
    if get_os() == "linux":
        return DemetraCallerLinux()
    if get_os() == "darwin":
        return DemetraCallerMac()
    # from .seasonal_adv_utils import this_is_pytest
    raise NotImplementedError("Computer OS not found.")




def general_params():
    return rf"{get_cruncher().crunch_folder}/general.params"


def create_general_params():
    folder = get_cruncher().crunch_folder

    return _create_general_params(folder, "general.params")


def copy_folder_demetra(files: Iterable[FileItem]):
    """
    this will copy demetra files from source
    directory to workspace
    :param files:
    :return:
    """

    def copy_all_files(file_item: FileItem):
        src = str(file_item.full_name).split(".xml")[0]
        trg = Path() / get_cruncher().local_work_space / file_item.encoded_name
        try:
            shutil.copytree(
                src,
                trg,
                symlinks=False,
                ignore=None,
                copy_function=shutil.copy2,
                ignore_dangling_symlinks=False,
                dirs_exist_ok=True,
            )
        except Exception as exc:
            print(exc)

    return list(map(copy_all_files, files))


def copy_xml_files_local(files: list[FileItem]):
    def copy_xml_file(file_item: FileItem):
        shutil.copy(
            file_item.full_name,
            Path(get_cruncher().local_work_space)
            / str(file_item.encoded_name + ".xml"),
        )

    return list(map(copy_xml_file, files))


def get_line_win(file_item: FileItem):
    fname = str(file_item.encoded_name + ".xml")
    ws = Path(get_cruncher().local_work_space)
    dest = ws / fname
    line_info = f"rem {file_item.short_name}\nrem " + "-" * 50 + "\n"
    cmd1 = rf'{line_info}{get_demetra_type().cruncher_command()} "{dest}"'
    cmd2 = rf'-x "{general_params()}"'
    cmd3 = rf'-d "{ws}/{middle_folder}/{file_item.short_name}"{NEW_LINE}'
    command = f"{cmd1} {cmd2} {cmd3}"
    # print(command)
    return command


def get_line_MAC(file_item: FileItem):
    ws = Path(get_cruncher().local_work_space)
    dest = ws / str(file_item.encoded_name + ".xml")
    line_info = f"# {file_item.short_name}\n# " + "-" * 50 + "\n"
    cmd1 = f'{line_info}\n{get_demetra_type().cruncher_command()} "{dest}"'
    cmd2 = f'-x "{general_params()}"'
    cmd3 = f'-d "{ws}/{middle_folder}/{file_item.short_name}"{NEW_LINE}'
    command = f"{cmd1} {cmd2} {cmd3}"
    # print(command)
    return command


def create_command(files):
    return map(get_line, files)


def patch_template_for_os(template):
    if get_os() != "windows":
        template = "\n".join(tuple(f"#{x}" for x in template.splitlines()))
    return template


def begin_content_win():
    from datetime import date

    today = date.today()
    template = f"""rem ==============================================================
rem         evdspy
rem         @2022 evdspy ==> JDemetra caller
rem         searched space  : {get_cruncher().demetra_folder}
rem         date created : {today}
rem ==============================================================
echo on
"""
    return patch_template_for_os(template)


def begin_content_MAC():
    # from datetime import date
    # today = date.today()
    template = """#!/bin/bash
echo "Starting the script..."
"""
    return template


def end_content_win() -> str:
    template = """
rem pause
    """
    return template


def end_content_MAC() -> str:
    return "\n"


if os_str != "windows":
    get_line = get_line_MAC
    begin_content = begin_content_MAC
    end_content = end_content_MAC
else:
    get_line = get_line_win
    begin_content = begin_content_win
    end_content = end_content_win




def write_bat_file(content, file_name):
    content = begin_content() + content + end_content()
    print("WRITING", content)
    fname = get_demetra_type().exec_file_name(file_name)
    with open(fname, mode="w+", encoding="utf-8") as file_:
        file_.write(content)



def run_bat_commands_win():
    """run_bat_commands_win"""
    create_general_params()
    name = get_demetra_type().demetra_command_file_name()
    f = subprocess.Popen(name, shell=True).wait()
    print(f)


def run_bat_commands_mac():
    """run_bat_commands_mac"""
    import os

    create_general_params()
    script_path = get_demetra_type().demetra_command_file_name()
    os.chmod(script_path, 0o755)
    subprocess.run([script_path])


if os_str == "windows":
    run_bat_commands = run_bat_commands_win
else:
    run_bat_commands = run_bat_commands_mac
