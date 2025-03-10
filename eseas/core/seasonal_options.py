# This file is part of the eseas project
# Copyright (C) 2024 Sermet Pekin 
#
# This source code is free software; you can redistribute it and/or
# modify it under the terms of the European Union Public License
# (EUPL), Version 1.2, as published by the European Commission.
#
# You should have received a copy of the EUPL version 1.2 along with this
# program. If not, you can obtain it at:
# <https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12>.
#
# This source code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# European Union Public License for more details.
#
# Alternatively, if agreed upon, you may use this code under any later
# version of the EUPL published by the European Commission.


# ====================================================================
#
# eseas
#
from .cruncher_classes import Cruncher
from .folder_class import (
    FolderClass,
    DemetraFolder,
    JavaBinFolder,
    WorkspaceFolder,
    CruncherFolder,
)

# ====================================================================


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
        demetra_folder=None,
        java_folder=None,
        local_folder=None,
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
        java_bin=None,
    ):

        self.demetra_folder = DemetraFolder(demetra_folder)
        self.java_folder = CruncherFolder(java_folder)
        self.local_folder = WorkspaceFolder(local_folder)
        self.java_bin = JavaBinFolder(java_bin)

        self.demetra_folder = str(self.demetra_folder)
        self.java_folder = str(self.java_folder)
        self.local_folder = str(self.local_folder)
        self.java_bin = java_bin if java_bin else None

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
            java_bin = {self.java_bin}
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
            java_bin=self.java_bin,
        )
