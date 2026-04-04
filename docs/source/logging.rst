Logging System
==============

eseas provides comprehensive automatic logging for all runs, helping with debugging, monitoring, and troubleshooting.

Overview
--------

All logs are stored in the ``.eseas/.logs/`` directory within your project:

.. code-block:: text

    your_project/
    ├── .eseas/
    │   ├── .logs/
    │   │   ├── last_good_run.log      # Latest successful run
    │   │   ├── failed_runs.log         # All errors
    │   │   └── emergency.log           # Fallback log
    │   ├── quick_start_example.py
    │   └── README.txt

Automatic Logging
-----------------

Logging happens automatically when using ``.run()``:

.. code-block:: python

    from eseas import Options, Seasonal

    options = Options(...)
    m = Seasonal(options)
    m.run()  # ← Automatically logs success or failure

No manual logging configuration needed!

Log Files
---------

last_good_run.log
~~~~~~~~~~~~~~~~~

Records the most recent successful run with comprehensive information:

**Contains:**

- Execution time
- System information (OS, Python, Java versions)
- All configuration options
- Workspace paths and validation
- Processing statistics
- Full execution script content

**Example:**

.. code-block:: json

    {
      "status": "success",
      "eseas_version": "2.0.0",
      "timestamp": "2026-04-04T18:42:24.346474",
      "execution_time_seconds": 3.65,
      "system": {
        "platform": "macOS-15.7.3-arm64-arm-64bit",
        "python_version": "3.12.8",
        "java_available": true,
        "java_version": "openjdk version 11.0.25"
      },
      "processing_stats": {
        "xml_files_found": 9,
        "csv_outputs_generated": 540,
        "xlsx_outputs_generated": 3
      }
    }

failed_runs.log
~~~~~~~~~~~~~~~

Records all failures with full diagnostic information:

**Contains:**

- Error message and full stack trace
- Execution time until failure
- System state at time of error
- All paths and configuration
- What was processed before the error

**Example:**

.. code-block:: json

    {
      "status": "error",
      "execution_time_seconds": 1.23,
      "error": {
        "message": "FileNotFoundError: [Errno 2] ...\n\nTraceback...",
        "type": "runtime_error"
      },
      "paths": {
        "demetra_folder_exists": false,
        "workspace_exists": true
      }
    }

emergency.log
~~~~~~~~~~~~~

Used when the main logging system fails (rare).

**Format:** Plain text

.. code-block:: text

    ================================================================================
    EMERGENCY LOG ENTRY - 2026-04-04T18:50:15.123456
    Logging system failed with error: [error details]
    Original error: [error message]
    ================================================================================

Information Logged
------------------

System Information
~~~~~~~~~~~~~~~~~~

- Platform (OS and architecture)
- Python version and executable path
- Current working directory
- User name
- Timestamp
- Java availability and version

Paths and Validation
~~~~~~~~~~~~~~~~~~~~

- Local workspace path
- Demetra folder path
- Cruncher folder path
- General params path
- Execution script path
- **Existence checks** for each path
- Full execution script content

Processing Statistics
~~~~~~~~~~~~~~~~~~~~~

- Count of XML files found
- List of XML file names
- Count of CSV outputs generated
- Count of Excel outputs generated

Configuration
~~~~~~~~~~~~~

All options are logged:

- demetra_folder
- java_folder
- local_folder
- workspace_mode
- auto_approve
- csvlayout
- result_file_names
- All other parameters

Execution Metrics
~~~~~~~~~~~~~~~~~

- Total execution time in seconds
- Timestamp for each run

Guaranteed Log Creation
-----------------------

eseas ensures logs are **always created** using multiple fallback mechanisms:

1. **Primary**: Write to ``.eseas/.logs/`` in current directory
2. **Fallback**: Write to system temp directory if CWD fails
3. **Emergency**: Write to ``emergency.log`` if JSON logging fails
4. **Last Resort**: Print to stderr if all else fails

Global Exception Handler
~~~~~~~~~~~~~~~~~~~~~~~~~

eseas installs a global exception handler that catches **any** uncaught exceptions:

- Automatically logs the error
- Provides full diagnostic information
- Never crashes your program
- Installed automatically on ``import eseas``

Accessing Logs
--------------

View Latest Success
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cat .eseas/.logs/last_good_run.log

View All Errors
~~~~~~~~~~~~~~~

.. code-block:: bash

    cat .eseas/.logs/failed_runs.log

Programmatic Access
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pathlib import Path
    import json
    import re

    # Read last successful run
    log_file = Path.cwd() / ".eseas" / ".logs" / "last_good_run.log"
    log_content = log_file.read_text()

    # Parse JSON (last entry)
    entries = re.split(
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - \w+ - INFO - ',
        log_content
    )

    for entry in reversed(entries):
        if entry.strip().startswith('{'):
            log_data = json.loads(entry.strip())
            print(f"Last run: {log_data['execution_time_seconds']}s")
            print(f"Files: {log_data['processing_stats']['xml_files_found']}")
            break

Troubleshooting
---------------

Logs Not Created?
~~~~~~~~~~~~~~~~~

1. Check write permissions for current directory
2. Verify ``.eseas/.logs/`` directory exists
3. Look in temp directory: ``/tmp/.eseas/.logs/`` (Unix/Mac) or ``%TEMP%\.eseas\.logs\`` (Windows)
4. Check ``emergency.log`` for logging system failures

Need More Detail?
~~~~~~~~~~~~~~~~~

Set ``verbose=True`` in Options:

.. code-block:: python

    options = Options(..., verbose=True)

Review Failed Runs
~~~~~~~~~~~~~~~~~~

After any error:

.. code-block:: bash

    tail -100 .eseas/.logs/failed_runs.log

Privacy & Security
------------------

**What's Logged:**

- File paths (local to your system)
- Configuration options
- Error messages
- System information (OS, Python version)

**What's NOT Logged:**

- File contents
- Sensitive data from XML files
- Passwords or credentials
- Network requests

Best Practices
--------------

1. **Review failed_runs.log** after any error
2. **Compare successful runs** using last_good_run.log
3. **Monitor execution_time_seconds** for performance issues
4. **Check processing_stats** to verify expected files processed
5. **Keep .eseas directory** for diagnostics

Example: Debugging a Failed Run
--------------------------------

When your script fails:

.. code-block:: bash

    # 1. Check what happened
    cat .eseas/.logs/failed_runs.log | tail -50

    # 2. Look for key information
    # - "demetra_folder_exists": false  ← Directory doesn't exist!
    # - "xml_files_found": 0            ← No XML files found!
    # - "java_available": false         ← Java not installed!

    # 3. Fix the issue and try again

The logs tell you exactly what went wrong and how to fix it.

Log Rotation
------------

Currently, logs append indefinitely. For long-running projects:

.. code-block:: bash

    # Archive old logs
    mv .eseas/.logs/failed_runs.log .eseas/.logs/failed_runs.$(date +%Y%m%d).log

    # Or delete old logs
    rm .eseas/.logs/*.log

Support
-------

If logging issues persist:

1. Check ``emergency.log`` file
2. Share relevant log entries (redacting sensitive paths)
3. Report issues: https://github.com/SermetPekin/eseas-repo/issues
