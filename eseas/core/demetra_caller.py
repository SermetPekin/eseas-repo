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
