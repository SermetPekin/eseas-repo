from dataclasses import dataclass
from ._general_params import _create_general_params
from .cruncher_classes import get_cruncher

from abc import ABC, abstractmethod
from ._options import demetra_command_file_name

# demetra_command_file_name = 'demetra_commands'


@dataclass
class DemetraCaller(ABC):
    @abstractmethod
    def cruncher_command(self): ...

    @abstractmethod
    def demetra_command_file_name(self): ...

    @abstractmethod
    def exec_file_name(self, file_name): ...


class DemetraCallerWindows(DemetraCaller):

    def cruncher_command(self):
        return rf"start {get_cruncher().crunch_folder}/jwsacruncher.bat"

    def demetra_command_file_name(self):
        return rf"{get_cruncher().crunch_folder}/{demetra_command_file_name}.bat"

    def exec_file_name(self, file_name):
        return rf"{get_cruncher().crunch_folder}/{file_name}.bat"


@dataclass
class DemetraCallerLinux(DemetraCaller):

    def cruncher_command(self):
        return rf"{get_cruncher().crunch_folder}/jwsacruncher"

    def demetra_command_file_name(self):
        return rf"{get_cruncher().crunch_folder}/{demetra_command_file_name}.sh"

    def exec_file_name(self, file_name):
        return rf"{get_cruncher().crunch_folder}/{file_name}.sh"


@dataclass
class DemetraCallerMac(DemetraCallerLinux): ...
