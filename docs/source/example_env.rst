Example: Using `.env` Files
=====

Running the Script When a `.env` File Exists
--------------------------------------------

If a `.env` file is present in the current directory, the script will automatically load parameter values from it.

.. code-block:: python

    from eseas import Seasonal, Options
    import time

    # Load options from the `.env` file
    options = Options()

    # Initialize and execute the seasonal adjustment process
    m = Seasonal(options)
    m.part1()
    time.sleep(10)  # Pause before running part2
    m.part2()

Overwriting `demetra_folder` from Function Call
-----------------------------------------------

If a `.env` file exists, you can override the `demetra_folder` value by passing it directly in the function call.

.. code-block:: python

    from eseas import Seasonal, Options
    import time

    # Override `demetra_folder` from function call, ignoring the value in `.env`
    options = Options(demetra_folder="SomeDemetraFolder")

    # Initialize and execute the seasonal adjustment process
    m = Seasonal(options)
    m.part1()
    time.sleep(10)  # Pause before running part2
    m.part2()


Example `.env` File Content
---------------------------

The following is an example of a `.env` file used for defining parameters.  
If a parameter is not provided in the `Options` function, it will be loaded from the `.env` file.

.. code-block:: ini

    # Required if not specified in the Options function
    java_folder = /Users/guest/app/jwsacruncher-2.2.6/bin
    demetra_source_folder = ./eseas/data_for_testing/unix
    local_folder = ./test_out

    # Optional parameters
    java_bin = /usr/bin



Key Behavior
------------

- If `demetra_folder` **is not provided**, it defaults to the value in `.env`.
- If `demetra_folder` **is provided**, it overrides the `.env` file setting.
