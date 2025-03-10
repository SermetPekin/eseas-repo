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


from pathlib import Path
from collections import OrderedDict
from typing import Union, Optional
import os


def load_dotenv(filepath=".env") -> Optional[OrderedDict]:
    """Load environment variables from a .env file."""
    d = OrderedDict()

    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            key, sep, value = line.partition("=")
            if sep and key.strip():
                os.environ[key.strip()] = value.strip()
                d[key.strip()] = value.strip()
    return d


class FolderClass:
    type_: str = "FolderClass"

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

    def check_env_file(self):
        if self.env_file_exists():
            if self.value is None:
                v = self.get_from_env()
                if v is not None:
                    self.value = Path(v)

    def check(self):
        if self.env_file_exists():
            self.load_env()
            v = self.get_from_env()
            if v is not None:
                self.value = Path(v)
                return
        if not self.exists():
            self.warn_stop()

    def exists(self):
        if self.value is None:
            return False
        return Path(self.value).exists()

    def create(self):
        import os

        value = self.value
        print(f"creating folder {value}")
        if value is None:
            return False
        value = Path(value)

        try:
            os.makedirs(value, exist_ok=True)
        except OSError as e:
            print(f"Error creating folder {value} {e}")
            return False
        return True

    @staticmethod
    def load_env(env_file: str = ".env"):
        d = load_dotenv(env_file)
        if d is None:
            print(f" {env_file} not found. it will be ignored")
            return

        k = d.keys()
        if len(k) == 0:
            print(f"no keys found in {env_file}")
            return

    def env_file_exists(self, env_file: str = ".env"):
        return Path(env_file).exists

    def get_from_env(self):
        _ = self.load_env()
        if self.value is None:
            self.value = os.getenv(self.type_)
        return self.value


class TestFolderInstance(FolderClass):
    type_ = "TestFolderInstance"

    def check2(self):
        if not self.exists():
            self.warn(f"Test folder does not exist {self.value}")


class DemetraFolder(FolderClass):
    type_ = "demetra_source_folder"


class JavaBinFolder(FolderClass):
    type_ = "java_bin"

    def java_available(self):
        from eseas.core.java_environ import JavaEnviron

        print("Checking if java is available")
        j = JavaEnviron()
        p = j.find_java_paths()
        return bool(p)

    def check(self):
        self.check_env_file()

        if self.value is None:
            self.get_from_env()  # env is secondary

            if self.value is None:
                if self.java_available():
                    print(
                        """Java binary not given from the function or from env file but Java is available in the system."""
                    )
                    self.sleep(4)
                    return
                else:
                    self.warn_stop(f"Java binary folder does not exist {self.value}")

        if not self.exists():
            if self.java_available():
                print(
                    f"""Ignoring folder `{self.value}`since it does not exist and Java is available in the system."""
                )
                self.sleep(3)
                return
            self.warn_stop(f"Java binary folder does not exist {self.value}")


class CruncherFolder(FolderClass):
    type_ = "java_folder"


class WorkspaceFolder(FolderClass):
    type_ = "local_folder"

    def check(self):
        self.check_env_file()

        if not self.exists():
            self.warn(f"Creating folder for workspace since it does not exist yet.")
            if not self.create():
                self.warn_stop(f"Error creating folder {self.value}")
