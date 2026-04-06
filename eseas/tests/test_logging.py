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


import pytest
from pathlib import Path
import json


def test_success_log_format():
    """Test that success logs contain comprehensive information"""
    log_file = Path.cwd() / ".eseas" / ".logs" / "last_good_run.log"

    if not log_file.exists():
        pytest.skip("No success log file exists yet")

    # Read the log file and extract JSON entries
    log_content = log_file.read_text(encoding="utf-8")

    # Split by the log timestamp pattern to get individual log entries
    import re

    entries = re.split(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - \w+ - INFO - ", log_content
    )

    # Get the last non-empty entry
    last_json = None
    for entry in reversed(entries):
        entry = entry.strip()
        if entry and entry.startswith("{"):
            try:
                last_json = json.loads(entry)
                break
            except json.JSONDecodeError:
                continue

    if not last_json:
        pytest.skip("Could not parse log entry")

    # Verify comprehensive information is present
    assert "status" in last_json
    assert last_json["status"] == "success"
    assert "eseas_version" in last_json
    assert "timestamp" in last_json
    assert "execution_time_seconds" in last_json
    assert "system" in last_json
    assert "options" in last_json
    assert "paths" in last_json
    assert "processing_stats" in last_json

    # Verify system info
    system = last_json["system"]
    assert "platform" in system
    assert "python_version" in system
    assert "java_available" in system
    assert "java_version" in system

    # Verify processing stats
    stats = last_json["processing_stats"]
    assert "xml_files_found" in stats or "error" in stats

    print("\nSuccess log verification passed!")
    print(f"  - eseas version: {last_json['eseas_version']}")
    print(f"  - execution time: {last_json['execution_time_seconds']}s")
    print(f"  - platform: {system['platform']}")
    if "xml_files_found" in stats:
        print(f"  - XML files processed: {stats['xml_files_found']}")


def test_error_log_creation():
    """Test that error logs are created when exceptions occur"""
    from eseas import Options, Seasonal

    # Try to run with invalid folder to trigger error
    with pytest.raises(Exception):
        options = Options(
            demetra_folder="nonexistent_folder_xyz123",
            java_folder="/usr/bin",
            local_folder="./temp_test",
        )
        m = Seasonal(options)
        m.run()

    # Check if error log was created
    error_log = Path.cwd() / ".eseas" / ".logs" / "failed_runs.log"
    assert error_log.exists(), "Error log should be created when exception occurs"

    # Verify error log contains useful information
    log_content = error_log.read_text(encoding="utf-8")
    assert "error" in log_content.lower()

    print("\nError log creation verified!")


def test_log_directory_creation():
    """Test that log directory is always created"""
    log_dir = Path.cwd() / ".eseas" / ".logs"
    assert log_dir.exists(), "Log directory should be created"
    assert log_dir.is_dir(), "Log path should be a directory"

    # Check that example script was created
    example_script = Path.cwd() / ".eseas" / "quick_start_example.py"
    assert example_script.exists(), "Quick start example should be created"

    # Check that README was created
    readme = Path.cwd() / ".eseas" / "README.txt"
    assert readme.exists(), "README should be created"

    print("\nLog directory structure verified!")
