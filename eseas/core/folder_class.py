# ====================================================================
#
# eseas
#
from pathlib import Path


class FolderClass:
    type_: str = "demetra_folder"

    def __init__(self, value: str = None):
        if value is None:
            self.value = None
        else:
            self.value = Path(value)
        self.check()

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def warn_stop(self, msg: str = None):
        if msg:
            self.warn(msg, stop=True)
            return
        
        template = f"""
            {self.type_} does not exist
        """
        print(template)
        self.warn(template, stop=True)

    def warn(self, msg: str, stop=False):

        print(msg)
        self.sleep()
        if stop:
            raise ValueError(msg)

    def sleep(self, number: int = 2):
        import time

        time.sleep(number)

    def check(self):
        if not self.exists():
            self.warn_stop()

    def exists(self):
        if self.value is None:
            return False
        return Path(self.value).exists()

    def create(self, value: Path):
        import os

        value = Path(value)
        try:
            os.makedirs(value, exist_ok=True)
        except OSError as e:
            print(f"Error creating folder {value} {e}")
            return False
        return True


class DemetraFolder(FolderClass):
    type_ = "DemetraFolder"


class JavaBinFolder(FolderClass):
    type_ = "JavaBinFolder"

    def check(self):
        if self.value is None:
            return
        if not self.exists():
            self.warn_stop(f"Java binary folder does not exist {self.value}")


class CruncherFolder(FolderClass):
    type_ = "CruncherFolder"


class WorkspaceFolder(FolderClass):
    type_ = "WorkspaceFolder"

    def check(self):

        if not self.exists():
            self.warn(f"Creating folder for workspace since it does not exist yet.")
            if not self.create(self.value):
                self.warn_stop(f"Error creating folder {self.value}")
