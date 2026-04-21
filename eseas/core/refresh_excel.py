#!/usr/bin/env python
# coding: utf-8

import sys
import time
from pathlib import Path
import psutil
import subprocess
import pythoncom

import win32com.client


def get_input():
    ans = input(
        "In order to refresh this file \nEXCEL.EXE application will be stopped if it is running. \nConfirm ? [Y/n]"
    )
    return ans


def ask_permission() -> bool:
    ans = get_input()

    return ans.lower() in ["y", "yes", "ok", "good"]


def shut_excel(approve: bool = False):
    if not approve:
        answer = ask_permission()
        if not answer:
            raise ValueError("User did not confirm closing EXCEL.EXE application")

    command = ["cmd", "/c", "taskkill", "/f", "/im", "EXCEL.EXE"]
    print("closing Excel.exe application ...")
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, encoding="utf-8"
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def excel_running():
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"].lower() == "excel.exe":
            return True
    return False


class File:
    """
    File ( a.xlsx , a/b/c) => a/b/c/a.xlsx

    File (a/b/c/a.xlsx)

    File (a/b/c/a.xlsx, root = None )

    """

    def __init__(self, name: str, root: str = None, approve: bool = False, dont_check=False):
        self.name = name
        self.root = root
        self.dont_check = dont_check
        if self.root is None:
            self.path = Path(name).absolute()
        else:

            if isinstance(root, str):
                self.root = Path(self.root)

            self.path: Path = (self.root / name).absolute()

        self.approve = approve

    def __str__(self):
        return f"<File [{self.path}]>"

    def exists(self):
        return self.path.exists()

    def check(self):
        if self.dont_check:
            print("Passing check since this is test")
            return
        if not self.exists():

            raise ValueError(f"File Not found ! {self.path}")
        assert self.exists()

    def refresh(self, excel_app):  # Pass excel_app as an argument
        try:
            print(f"working on: {self}")
            wb = excel_app.Workbooks.Open(self.path)
            wb.RefreshAll()
            time.sleep(1)
            wb.Save()
            wb.Close(False)
            print(f"Done => {self}")
        except Exception as e:
            import traceback

            traceback.print_exc()

            print(f"Error - {self}:\n{e}")


def check_and_get_files(files, root=None, approve: bool = False, dont_check: bool = False):

    fs = [File(x, root=root, approve=approve, dont_check=dont_check) for x in files]
    for a in fs:
        a.check()

    for File_ in fs:
        yield File_


def get_excel_app(approve=False):
    if excel_running():
        shut_excel(approve)

    excel_app = win32com.client.Dispatch("Excel.Application")
    return excel_app


def refresh(files, root: Path | str | None = None, approve: bool = False):
    pythoncom.CoInitialize()
    excel_app = None   

    try:
        excel_app = get_excel_app(approve)
        for File_ in check_and_get_files(files, root, approve):
            File_.refresh(excel_app)  

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An error occurred during refresh: {e}")

    finally:
        if excel_app is not None:
            try:
                excel_app.Quit()
                print("Closing excel application!")
            except Exception as quit_error:
                import traceback
                traceback.print_exc()
                print(f"Error while trying to close excel : {quit_error}")

        pythoncom.CoUninitialize()
