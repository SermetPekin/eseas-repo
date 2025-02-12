eseas
===========
**eseas** is a Python package that acts as a wrapper for the `jwsacruncher` Java package.
It enables users to process **Demetra workspace XML files**, create batch files, execute them, and collect the desired outputs into individual **Excel files**.



Features
--------
- Process **Demetra** workspace XML files.
- Automate **batch file creation and execution**.
- Retrieve specific results and store them in **Excel files**.
- Flexible options for **result extraction**.

Installation
------------
You can install **eseas** using pip:

.. code-block:: bash

    pip install eseas

Usage
-----
Here’s an example demonstrating how to use **eseas**:

.. code-block:: python

    from eseas import Seasonal, Options
    import time

    def main():
        # Specify the path to the jwsacruncher bin directory
        java_folder = r'../../Downloads/jwsacruncher-2.2.4/bin'
        demetra_source_folder = r"./demetra_source_folder"
        local_folder = r"./test_out"

        options = Options(
            demetra_source_folder,
            java_folder,
            local_folder,
            result_file_names=("sa", "s_f", "cal"),  # *1
            workspace_mode=True,
            file_name_explanation=True,
        )
        # Note (1)
        # result_file_names: See the full list of result types from Demetra Components below

        seas = Seasonal(options)

        seas.part1()
        time.sleep(10)
        seas.part2()

    if __name__ == "__main__":
        main()

Demetra Components (Result Types)
---------------------------------
The `result_file_names` parameter allows specifying different result types from **Demetra**.
Some common types include:

- `"sa"` - Seasonally Adjusted Series
- `"s_f"` - Smoothed Factors
- `"cal"` - Calendar Effects
- … (add more based on Demetra outputs)

License
-------
This project is licensed under the **European Union Public License (EUPL) v1.2**.
See the full license in the `LICENSE` file.


Author
------
Developed by **Sermet Pekin**.

