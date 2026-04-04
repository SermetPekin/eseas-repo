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
from .seas_utils import view_display
from evdspy.EVDSlocal.common.files import Write
from .seasonal_adv_utils import (
    get_input_from_user,
    common_space_msg,
    display,
)

from ._options import demetra_command_file_name

# demetra_command_file_name = 'demetra_commands'

from eseas.core.collect import collect_parts_of_results as collect


class SeasonalADV:
    def __init__(self, options):
        self.options = options
        self.code_reproduce()

    def part1(self):
        self.common_space_check()

    def part2(
        self,
        xml_folders=None,
        out_folder=None,
        out_file_name="combined",
        encoding="latin-1",
    ):
        collect(
            self.options,
            xml_folders=xml_folders,
            out_folder=out_folder,
            out_file_name=out_file_name,
            encoding=encoding,
        )

    def run(self):
        """Run part1 and part2 sequentially without manual interruption"""
        from .error_logger import log_eseas_error
        import traceback
        try:
            self.part1()
            self.part2()
        except Exception as e:
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            log_eseas_error(error_msg, self.options)
            raise

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
