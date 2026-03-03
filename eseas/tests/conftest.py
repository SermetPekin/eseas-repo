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

import os
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import pytest
import time


CRUNCHER_VERSION = "2.2.5"
CRUNCHER_URL = f"https://github.com/jdemetra/jwsacruncher/releases/download/v{CRUNCHER_VERSION}/jwsacruncher-{CRUNCHER_VERSION}-bin.zip"
CRUNCHER_EXTRACT_PATH = Path(__file__).parent.parent.parent / "jwsacruncher"
CRUNCHER_BIN_PATH = CRUNCHER_EXTRACT_PATH / f"jwsacruncher-{CRUNCHER_VERSION}" / "bin"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def download_jwsacruncher():
    """Download jwsacruncher if not already present, with retry logic."""
    if CRUNCHER_BIN_PATH.exists():
        print(f"jwsacruncher already exists at {CRUNCHER_BIN_PATH}")
        return True

    print(f"\nDownloading jwsacruncher {CRUNCHER_VERSION}...")
    CRUNCHER_EXTRACT_PATH.mkdir(parents=True, exist_ok=True)

    zip_file = CRUNCHER_EXTRACT_PATH / f"jwsacruncher-{CRUNCHER_VERSION}-bin.zip"

    for attempt in range(MAX_RETRIES):
        try:
            print(f"Download attempt {attempt + 1}/{MAX_RETRIES}...")
            
            # Create a custom request with a User-Agent header
            req = urllib.request.Request(
                CRUNCHER_URL,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                with open(zip_file, 'wb') as out_file:
                    out_file.write(response.read())
            
            print(f"Downloaded to {zip_file}")

            print(f"Extracting to {CRUNCHER_EXTRACT_PATH}...")
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(CRUNCHER_EXTRACT_PATH)

            zip_file.unlink()  # Remove zip file after extraction
            print(f"jwsacruncher extracted successfully to {CRUNCHER_BIN_PATH}")
            return True

        except Exception as e:
            print(f"Download attempt {attempt + 1} failed: {e}")
            if zip_file.exists():
                zip_file.unlink()
            
            if attempt < MAX_RETRIES - 1:
                print(f"Waiting {RETRY_DELAY} seconds before retry...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"Failed to download jwsacruncher after {MAX_RETRIES} attempts")
                return False


@pytest.fixture(scope="session", autouse=True)
def setup_cruncher():
    """Automatically download and set up jwsacruncher for tests."""
    # Check if JAVA_CRUNCHER_BIN is already set
    if os.environ.get("JAVA_CRUNCHER_BIN"):
        cruncher_bin = os.environ.get("JAVA_CRUNCHER_BIN")
        print(f"Using existing JAVA_CRUNCHER_BIN: {cruncher_bin}")
        
        # Verify it exists
        if not Path(cruncher_bin).exists():
            print(f"Warning: JAVA_CRUNCHER_BIN points to non-existent path: {cruncher_bin}")
        return

    # Try to download
    if download_jwsacruncher():
        # Set the environment variable
        os.environ["JAVA_CRUNCHER_BIN"] = str(CRUNCHER_BIN_PATH)
        print(f"Set JAVA_CRUNCHER_BIN to {os.environ['JAVA_CRUNCHER_BIN']}")
    else:
        print("WARNING: Could not download jwsacruncher. Tests requiring the cruncher will be skipped.")


def pytest_configure(config):
    """Hook that runs before test collection to setup cruncher and register markers."""
    # Ensure download happens before any test collection
    if not os.environ.get("JAVA_CRUNCHER_BIN"):
        if download_jwsacruncher():
            os.environ["JAVA_CRUNCHER_BIN"] = str(CRUNCHER_BIN_PATH)
            print(f"Set JAVA_CRUNCHER_BIN to {os.environ['JAVA_CRUNCHER_BIN']}")
        else:
            print("WARNING: Could not download jwsacruncher. Tests requiring the cruncher will be skipped.")
    
    # Register custom markers
    config.addinivalue_line(
        "markers", "skip_if_no_cruncher: skip test if jwsacruncher is not available"
    )


def pytest_runtest_setup(item):
    """Skip tests at runtime if they require cruncher but it's not available."""
    if item.get_closest_marker("skip_if_no_cruncher"):
        if not os.environ.get("JAVA_CRUNCHER_BIN"):
            pytest.skip("jwsacruncher not available (JAVA_CRUNCHER_BIN not set)")

