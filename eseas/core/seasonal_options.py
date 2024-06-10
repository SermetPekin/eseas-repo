from .cruncher_classes import Cruncher


class SingleOptions:
    """SingleOptions"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingleOptions, cls).__new__(cls)
        return cls.instance

    def set_items(cls, options):
        cls.instance.options = options


class SeasonalOptions:
    def __init__(
        self,
        demetra_folder,
        java_folder,
        local_folder,
        test=False,
        verbose=False,
        replace_original_files=False,
        auto_approve=False,
        result_file_names=(
            "sa",
            "s",
            "cal",
        ),
        workspace_mode=True,
        file_name_explanation=True,
    ):
        self.demetra_folder = demetra_folder
        self.java_folder = java_folder
        self.local_folder = local_folder
        self.test = test
        self.verbose = verbose
        self.replace_original_files = replace_original_files
        self.auto_approve = auto_approve
        self.result_file_names = result_file_names
        self.workspace_mode = workspace_mode
        self.file_name_explanation = file_name_explanation
        self.set_options(workspace_mode)
        so = SingleOptions()
        so.set_items(self)

    def __repr__(self):
        template = f"""
    options= SeasonalOptions(
            demetra_folder="{self.demetra_folder}",
            java_folder="{self.java_folder}",
            local_folder="{self.local_folder}",
            test={self.test},
            verbose= {self.verbose},
            replace_original_files={self.replace_original_files},
            auto_approve={self.auto_approve},
            result_file_names={self.result_file_names},
            workspace_mode={self.workspace_mode},
    )
        """
        return template

    def set_options(self, workspace_mode):
        c = Cruncher()
        c.set_items(
            local_work_space=self.local_folder,
            crunch_folder=self.java_folder,
            demetra_folder=self.demetra_folder,
            workspace_mode=workspace_mode,
            file_name_explanation=self.file_name_explanation,
        )
