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

"""
----------------------------------
      Global options
----------------------------------
"""

"""
    middle_folder
    .............
      -middle_folder : 'test_output'
      local_w_space / middle_folder / ...
      # produced csv content will be placed here
"""
middle_folder = "test_output"
"""
    demetra_command_file_name
    .............
       e.g. :  demetra_commands
"""
demetra_command_file_name = "demetra_commands"
"""
    max_num
    ...............
      this number will be maximum number of xml files that can be picked
      while searching for demetra xml files.
"""

max_num = 5_000
