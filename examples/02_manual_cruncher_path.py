from eseas import Seasonal, Options


def main():
    """
    Example 2: Traditional Setup (Manual Cruncher File Path)

    If auto_download=False (default behavior), you must point to a
    pre-installed jdmetra jwsacruncher distribution binary locally using
    the `java_folder` parameter.
    """
    options = Options(
        demetra_source_folder=r"C:\Data\Finance\projects\demetra",
        java_folder=r"C:\Tools\jwsacruncher-2.2.4\bin",  # Pre-downloaded java_folder
        local_folder=r"C:\Data\Finance\projects\output",
        result_file_names=("sa", "s_f"),
        workspace_mode=True,  # Wrap into workspace directory structure
        file_name_explanation=True,  # Verbose suffix naming for generated Excel
        auto_download=False,  # Optional default: we bring our own cruncher
        auto_approve=False,  # Require shell prompts to assure users
    )

    seas = Seasonal(options)
    seas.run()


if __name__ == "__main__":
    main()
