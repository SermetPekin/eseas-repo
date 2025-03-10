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


from eseas.core.seas_utils import search_demetra_folder
from eseas.core.seas_utils import filter_xml
from eseas.core.seas_utils import filter_xml_demetra
from .test_utils import skip_if_github


@skip_if_github
def test_search_demetra_folder(capsys):
    with capsys.disabled():

        fold = "unix"
        demetra_folder = rf"./eseas/data_for_testing/{fold}"
        fs = search_demetra_folder(demetra_folder, None)
        assert fs
        fs2 = search_demetra_folder(demetra_folder, filter_xml)
        fs3 = filter_xml_demetra(fs2)
        print(fs3)
        assert len(fs3) == 1
