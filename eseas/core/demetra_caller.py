from dataclasses import dataclass

from .cruncher_classes import get_cruncher

from abc import ABC, abstractmethod
from ._options import demetra_command_file_name


@dataclass
class DemetraCaller(ABC):
    @property
    def cf(self):
        return get_cruncher().crunch_folder

    @abstractmethod
    def cruncher_command(self):
        ...

    @abstractmethod
    def demetra_command_file_name(self):
        ...

    @abstractmethod
    def exec_file_name(self, file_name):
        ...


class DemetraCallerWindows(DemetraCaller):
    def cruncher_command(self):
        return rf"start {self.cf }/jwsacruncher.bat"

    def demetra_command_file_name(self):
        return rf"{self.cf}/{demetra_command_file_name}.bat"

    def exec_file_name(self, file_name):
        return rf"{ self.cf }/{file_name}.bat"


@dataclass
class DemetraCallerLinux(DemetraCaller):
    def cruncher_command(self):
        return rf"{self.cf}/jwsacruncher"

    def demetra_command_file_name(self):
        return rf"{ self.cf}/{demetra_command_file_name}.sh"

    def exec_file_name(self, file_name):
        return rf"{self.cf}/{file_name}.sh"


@dataclass
class DemetraCallerMac(DemetraCallerLinux):
    ...
