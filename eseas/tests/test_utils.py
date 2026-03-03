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


from eseas.core.github_actions import GithubActions
import pytest
import sys
import os


def gth_testing():
    return GithubActions().is_testing()


reason_gth = "passing when github Actions "


skip_if_github = pytest.mark.skipif(gth_testing(), reason=reason_gth)


def has_cruncher():
    """Check if jwsacruncher is available via JAVA_CRUNCHER_BIN environment variable."""
    cruncher_bin = os.environ.get("JAVA_CRUNCHER_BIN")
    return cruncher_bin is not None and cruncher_bin.strip() != ""


# Use custom marker - the pytest_runtest_setup hook in conftest.py will handle skipping
skip_if_no_cruncher = pytest.mark.skip_if_no_cruncher


def is_unix():
    """Check if the system is Unix-based (macOS or Linux)."""
    return sys.platform in ("darwin", "linux")


skip_if_unix = pytest.mark.skipif(
    is_unix(),
    reason="Skipping on Unix systems (macOS/Linux) - Windows-only features",
)
