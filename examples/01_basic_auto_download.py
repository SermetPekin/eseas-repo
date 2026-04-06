from eseas import Seasonal, Options


def main():
    """
    Example 1: Basic Usage with Auto-Download

    This is the simplest way to use eseas starting from version 2.0.0.
    It doesn't require you to point to a local jwsacruncher installation,
    because it automatically fetches and evaluates the JDemetra+ cruncher for you.
    """
    options = Options(
        demetra_source_folder=r"C:\Data\demetra_source_folder",  # Your input XML files
        local_folder=r"C:\Data\test_out",  # Your destination Excel output
        result_file_names=("sa", "s_f", "cal"),  # Components to output
        workspace_mode=True,  # Groups Excel outputs gracefully
        auto_download=True,  # Seamlessly fetches jwsacruncher
        auto_approve=True,  # Automatically skip [y/n] CLI prompts
    )

    # Initialize and execute the seasonal adjustment process synchronously
    seas = Seasonal(options)
    seas.run()


if __name__ == "__main__":
    main()
