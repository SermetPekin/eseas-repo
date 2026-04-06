from eseas import Seasonal, Options


def main():
    """
    Example 3: Forcing a specific Java Version Executable Path

    If your system has multiple JDK/JRE instances or does not expose Java directly
    to the system PATH, you can pass `java_bin` so eseas natively targets that JDK.
    """
    # A Windows specific JDK path
    java_bin_path = r"C:\Program Files\Java\jdk-17\bin"

    # Use auto_download or manual jdmetra path, but provide java_bin
    options = Options(
        demetra_source_folder=r"C:\Data\Finance\demetra",
        local_folder=r"C:\Data\Finance\output_v3",
        java_bin=java_bin_path,  # Forces execution using this JDK
        result_file_names=("sa", "s", "cal"),
        auto_download=True,  # Works nicely along with auto_download
        auto_approve=True,
        workspace_mode=True,
    )

    seas = Seasonal(options)
    seas.run()


if __name__ == "__main__":
    main()
