from eseas import Seasonal, Options


def main():
    """
    Example 5: Auto-Downloading to a Specific Custom Path

    By default, setting `auto_download=True` without a `java_folder` downloads
    the cruncher to a hidden `.eseas` folder in your user's home directory.

    However, if you provide a `java_folder` AND `auto_download=True`,
    eseas will download and extract the cruncher precisely into that target path.

    Note: If eseas detects that the jwsacruncher binaries are already
    present in this folder from an earlier run, it will skip the download
    and proceed to the seasonal adjustment. While this avoids re-downloading
    the file every run, you should evaluate whether automatic downloading
    aligns with your environment's security policies. Some users may prefer
    to download the tool manually and set `auto_download=False`.
    """
    options = Options(
        demetra_source_folder=r"C:\Data\demetra_source_folder",
        local_folder=r"C:\Data\test_out",
        # Target destination for the automatic download:
        java_folder=r"C:\Tools\JDemetra_Cruncher",
        result_file_names=("sa", "s_f", "cal"),
        workspace_mode=True,
        auto_download=True,  # Will download TO the java_folder above (if not already there)
        auto_approve=True,
    )

    # Initialize and execute the seasonal adjustment process synchronously
    seas = Seasonal(options)
    seas.run()


if __name__ == "__main__":
    main()
