#!/usr/bin/env python
# coding: utf-8

import sys
import time
from pathlib import Path
import psutil
import subprocess

if sys.platform == "win32":
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

    def __init__(
        self,
        name: str,
        root: str = None,
        macro_name="Macro1",
        approve: bool = False,
        dont_check=False,
    ):
        self.name = name
        self.root = root
        self.macro_name = macro_name
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

    def sleep(self, seconds: 0):
        import time

        time.sleep(seconds)

    def refresh(self, excel_app, sleep=0):  # Pass excel_app as an argument
        try:
            print(f"working on: {self}")
            wb = excel_app.Workbooks.Open(self.path)
            for conn in wb.Connections:
                if conn.Type == 1:  # OLEDB Connection
                    conn.OLEDBConnection.BackgroundQuery = False
                elif conn.Type == 2:  # ODBC Connection
                    conn.ODBCConnection.BackgroundQuery = False

            wb.RefreshAll()

            wb.Save()
            self.sleep(sleep)
            wb.Close(False)

            print(f"Done => {self}")
        except Exception as e:
            import traceback

            traceback.print_exc()

            print(f"Error - {self}:\n{e}")

    def refresh_macro(self, excel_app, sleep=0):
        try:
            print(f"working on: {self}")
            wb = excel_app.Workbooks.Open(self.path)

            for conn in wb.Connections:
                if conn.Type == 1:  # OLEDB Connection
                    conn.OLEDBConnection.BackgroundQuery = False
                elif conn.Type == 2:  # ODBC Connection
                    conn.ODBCConnection.BackgroundQuery = False

            wb.RefreshAll()

            excel_app.Application.Run(self.macro_name)

            wb.Save()
            self.sleep(sleep)

            wb.Close(False)
            print(f"Done [Macro: {self.macro_name}] => {self}")
        except Exception as e:
            import traceback

            traceback.print_exc()

            print(f"Error - {self}:\n{e}")


def check_and_get_files(
    files,
    macro_names: tuple = None,
    root=None,
    approve: bool = False,
    dont_check: bool = False,
):
    if isinstance(files, (str, Path)):
        files = [files]
    if isinstance(macro_names, str):
        if len(files) == 1:
            macro_names = [macro_names]
        else:
            import warnings

            warnings.warn(f"""
                          
                          Assuming all macro names are {macro_names}
                          
                          if they differ consider giving them as a list 
                          
                          >  refresh_macro(["a.xlsm" , "b.xlsm"] , ["Macro1", "Macro1Another"]) 
                          
                          """)
            macro_names = [macro_names for _ in range(len(files))]

    if macro_names:
        fs = []
        for file, macro_name in zip(files, macro_names):
            fs.append(
                File(
                    file,
                    root=root,
                    macro_name=macro_name,
                    approve=approve,
                    dont_check=dont_check,
                )
            )

    else:
        fs = [File(x, root=root, approve=approve, dont_check=dont_check) for x in files]

    for a in fs:
        a.check()

    for File_ in fs:
        yield File_


def get_excel_app(approve=False, visible=False):
    if excel_running():
        shut_excel(approve)
    excel_app = win32com.client.DispatchEx("Excel.Application")
    excel_app.Visible = int(visible)

    return excel_app


def refresh(
    files, root: Path | str | None = None, approve: bool = False, visible=False, sleep=0
):
    pythoncom.CoInitialize()
    excel_app = None

    try:
        excel_app = get_excel_app(approve=approve, visible=visible)
        for File_ in check_and_get_files(
            files, macro_names=None, root=root, approve=approve
        ):
            File_.refresh(excel_app, sleep=sleep)

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


def refresh_macro(
    files,
    macro_names: tuple,
    root: Path | str | None = None,
    approve: bool = False,
    visible=False,
    sleep=0,
):
    pythoncom.CoInitialize()
    excel_app = None

    try:
        excel_app = get_excel_app(approve=approve, visible=visible)
        for File_ in check_and_get_files(
            files, macro_names=macro_names, root=root, approve=approve
        ):
            File_.refresh_macro(excel_app, sleep=sleep)
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
