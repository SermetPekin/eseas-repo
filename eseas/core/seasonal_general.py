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
from pathlib import Path
import time
from evdspy.EVDSlocal.common.colors import print_with_failure_style
from evdspy.EVDSlocal.utils.utils_general import create_directory
from .create_bat_command import run_bat_commands
from .cruncher_classes import Cruncher
from .demetra import get_demetra_files, write_bat_file_demetra
from .picker_classes import OutFilePicker
from .seas_utils import view_display
from evdspy.EVDSlocal.common.files import Write
from .seasonal_adv_utils import (
    get_input_from_user,
    common_space_msg,
    seasonal_results_msg,
    get_results_info,
    display,
)

from ._options import demetra_command_file_name

# demetra_command_file_name = 'demetra_commands'


class SeasonalADV:
    def __init__(self, options):
        self.options = options
        self.code_reproduce()

    def sleep(self, seconds: int = 2):
        print(f"Sleeping for {seconds} seconds.")
        time.sleep(seconds)

    def part1(self):
        self.common_space_check()

    def part2(self):
        self.seasonal_results_advanced()

    def run(self, seconds : int = 10 ):
        """Run part1 and part2 with a sleep in between"""
        self.part1()
        self.sleep(seconds)
        self.part2()

    def common_space_check(self):
        """common_space_check"""
        msg = common_space_msg(self.options.test, self.options.demetra_folder)
        view_display(msg)
        time.sleep(1)
        xml_demetra = get_demetra_files(self.options.demetra_folder)
        if self.options.test:
            xml_demetra = xml_demetra[0:20]
        fn = demetra_command_file_name
        write_bat_file_demetra(xml_demetra, file_name=fn)
        if not self.options.auto_approve and not get_input_from_user():
            view_display(
                "demetra command did not run.\n"
                "You may type y next time if you like them to run."
            )
            return
        run_bat_commands()

    def seasonal_results_advanced(self):
        """seasonal_results_advanced"""
        view_display(seasonal_results_msg(self.options.test))
        time.sleep(1)
        if self.options.replace_original_files:
            t = get_results_info(Cruncher().local_work_space)
            print(t)
        xml_demetra = get_demetra_files(self.options.demetra_folder)
        if self.options.test:
            xml_demetra = xml_demetra[0:5]
        if self.options.verbose:
            display(xml_demetra)
        for file in xml_demetra:
            of_picker = OutFilePicker(
                file,
                names=self.options.result_file_names,
                file_name_explanation=self.options.file_name_explanation,
            )
            of_picker.pick_files()
        return xml_demetra

    def code_reproduce(self):
        return ReproduceMevsimsel(self).code_reproduce()


@dataclass
class ReproduceMevsimsel:
    def __init__(self, mevsimsel: SeasonalADV):
        self.mevsimsel = mevsimsel

    def code_reproduce(self):
        template = self.code_reproduce_template()
        folder_name = Path() / Cruncher().local_work_space / "@codes_reproduce"
        create_directory(folder_name)
        file_name = folder_name / "code_run.py"
        try:
            Write(file_name, template)
        except Exception as exc:
            print(exc)
            print_with_failure_style(
                f"Could not create reproduce file for later use.  {str(exc)}"
            )

    def code_reproduce_template(self):
        from datetime import datetime

        date_str = datetime.now()
        template = f"""\n
#======================================================================
# This script was created by eseas    {date_str}
#   In order to reproduce you may use this template
#======================================================================
from eseas import SeasonalOptions
from eseas import Seasonal
def main():
    {self.mevsimsel.options.__repr__()}
    m = Seasonal(options)
    m.part1()
    m.part2()
main()
        """
        return template


__all__ = ["SeasonalADV"]
