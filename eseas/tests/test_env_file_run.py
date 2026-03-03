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



from eseas import Seasonal
from eseas import Options
from eseas.core.seas_testing_utils import get_testing_utils
from eseas.tests.test_utils import skip_if_no_cruncher


def create_env_file():
    testing_utils = get_testing_utils()
    demetra_folder = testing_utils.demetra_folder
    java_folder = testing_utils.java_folder
    local_folder = testing_utils.local_folder

    template = f"""
java_bin = /usr/bin
java_folder = {java_folder}
demetra_source_folder = {demetra_folder}
local_folder = {local_folder}

"""
    with open(".env", "w") as f:
        f.write(template)


create_env_file()


@skip_if_no_cruncher
def test_seasonal_environment_file():
    options = Options(
        None,
        None,
        None,
        test=False,
        verbose=False,
        replace_original_files=False,
        auto_approve=False,
        result_file_names=(
            "sa",
            "s",
            "cal",
        ),
        workspace_mode=True,
        java_bin=None,
    )
    m = Seasonal(options)
    m.part1()
    m.part2()


@skip_if_no_cruncher
def test_seasonal_environment_file2():
    options = Options(
        demetra_folder=None,
        java_folder=None,
        local_folder=None,
        test=False,
        verbose=False,
        replace_original_files=False,
        auto_approve=False,
        result_file_names=(
            "sa",
            "s",
            "cal",
        ),
        workspace_mode=True,
        java_bin=None,
    )
    m = Seasonal(options)
    m.part1()
    m.part2()


@skip_if_no_cruncher
def test_with_empty_options():
    from eseas import Seasonal, Options
    import time

    # Load options from the `.env` file
    options = Options()

    # Initialize and execute the seasonal adjustment process
    m = Seasonal(options)
    m.part1()
    time.sleep(2)  # Pause before running part2
    m.part2()
