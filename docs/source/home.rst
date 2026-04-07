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
**Note:** **eseas v2.0.0+ requires Python 3.10+**. If you are on Python 3.9 or older, pip will automatically download the last compatible 1.x version instead.

You can install **eseas** using pip:

.. code-block:: bash

    pip install eseas -U

Usage
-----
Here’s an example demonstrating how to use **eseas**:

.. code-block:: python

    from eseas import Seasonal, Options

    def main():
        # Folder containing your Demetra XML workspace files
        demetra_folder = r"C:\Data\demetra_folder"

        # Your destination folder for the generated Excel files
        local_folder = r"C:\Data\test_out"

        # Initialize options focusing on simplicity and auto-downloading the engine
        options = Options(
            demetra_folder=demetra_folder,
            local_folder=local_folder,
            result_file_names=("sa", "s_f", "cal"),
            workspace_mode=True,
            auto_download=True,   # Seamlessly fetches jwsacruncher in the background
            auto_approve=True     # Skips y/n CLI prompts automatically
        )

        # Initialize the Seasonal process
        seas = Seasonal(options)

        # Execute the seasonal adjustment workflow synchronously
        seas.run()

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

