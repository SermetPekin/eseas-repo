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
        demetra_source_folder = r"C:\Data\demetra_source_folder"

        # Your destination folder for the generated Excel files
        local_folder = r"C:\Data\test_out"

        # Initialize options focusing on simplicity and auto-downloading the engine
        options = Options(
            demetra_source_folder=demetra_source_folder,
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







Demetra Components
------------------
For a full list of result types available in **Demetra**, refer to the
:doc:`components <components>`.
