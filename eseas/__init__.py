# __init__.py

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
import sys

# eseas
from eseas.core.seasonal_general import SeasonalADV as Seasonal
from eseas.core.seasonal_general import SeasonalADV
from eseas.core.seasonal_options import SeasonalOptions as Options
from eseas.core.seasonal_options import SeasonalOptions
from eseas.core.cruncher_classes import Cruncher
from eseas.core.collect import collect_parts_of_results as collect

from eseas.data_for_testing.some_data import get_sample_data
from eseas.core.utils_general2 import walk, walk2, sleep
from eseas.core._path import SPath 


# Install global exception handler for comprehensive error logging
try:
    from eseas.core.error_logger import install_global_exception_handler

    install_global_exception_handler()
except Exception:
    # Don't let exception handler installation break the import
    pass

if sys.platform == "win32":
    from eseas.core.refresh_excel import refresh
else:
    refresh = None

__all__ = [
    "Cruncher",
    "SeasonalADV",
    "SeasonalOptions",
    "Seasonal",
    "Options",
    "get_sample_data",
    "walk",
    "walk2",
    "Path",
    "refresh",
    "sleep",
    "collect",
    "SPath" , 
]

__version__ = "2.0.0"
