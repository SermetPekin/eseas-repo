You can install **eseas** using pip:

.. code-block:: bash

    pip install eseas

Usage
-----
Here’s an example demonstrating how to use **eseas**:

.. code-block:: python

    from eseas import Seasonal, Options


    def main():
        # Specify the path to the jwsacruncher bin directory
        java_folder = r'../../Downloads/jwsacruncher-2.2.4/bin' 

        # [Optional] Java binary folder (where the Java executable exists)
        # This will be added to the environment PATH variable if provided.
        java_bin = r'/usr/bin'

        # Folder containing Demetra XML files
        demetra_source_folder = r"./demetra_source_folder"

        # Workspace where output files will be stored
        local_folder = r"./test_out"

        options = Options(
            demetra_source_folder,
            java_folder,
            local_folder,
            result_file_names=("sa", "s_f", "cal"),  # See "Demetra Components" below
            workspace_mode=True,
            file_name_explanation=True,
            java_bin=java_bin
        )

        # Initialize the Seasonal process
        seas = Seasonal(options)

        # Execute the two-step process synchronously
        seas.run() # Triggers part1 followed by part2 immediately

    if __name__ == "__main__":
        main()







Demetra Components
------------------
For a full list of result types available in **Demetra**, refer to the
:doc:`components <components>`.
