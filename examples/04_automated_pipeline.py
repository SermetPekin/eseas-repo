from eseas import Seasonal, Options


def main():
    """
    Example 4: Automation Pipeline (Quiet / Streamlined Run)

    If you're automating scripts across servers, pipelines, or background apps,
    configure the options to be quiet, skip copies (workspace_mode=False),
    and keep filenames short (file_name_explanation=False).
    """

    options = Options(
        demetra_source_folder=r"C:\CronJobs\monthly_data_source",
        local_folder=r"C:\CronJobs\monthly_data_output",
        result_file_names=("sa", "y_f", "cal"),  # See components.txt for choices
        workspace_mode=False,  # Don't clone demetra source folder into output
        file_name_explanation=False,  # Don't suffix filename string info in outputs
        auto_download=True,  # Make it bulletproof from crontabs
        auto_approve=True,  # Unattended execution flag
        verbose=False,  # Only show critical errors in the panel
    )

    seas = Seasonal(options)
    seas.run()


if __name__ == "__main__":
    main()
