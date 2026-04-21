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
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Tuple, Optional, Any
import pathlib
from pathlib import Path
import traceback

from .cruncher_classes import Cruncher
from .folder_class import (
    DemetraFolder,
    JavaBinFolder,
    WorkspaceFolder,
    CruncherFolder,
)

# ====================================================================


class SingleOptions:
    """SingleOptions"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingleOptions, cls).__new__(cls)
            cls._instance.options = None
        return cls._instance

    def set_items(self, options):
        self.options = options


class SeasonalOptions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="ignore")

    demetra_folder: Optional[str] | Optional[Path] = None
    java_folder: Optional[str] | Optional[Path] = None
    local_folder: Optional[str] | Optional[Path] = None
    test: bool = False
    verbose: bool = False
    replace_original_files: bool = False
    auto_approve: bool = False
    result_file_names: Tuple[str, ...] = ("sa", "s", "cal")
    workspace_mode: bool = True
    file_name_explanation: bool = True
    java_bin: Optional[str] | Optional[Path] = None
    auto_download: bool = False
    replace_general_params: bool = False
    csvlayout: str = "Vtable"
    general_params_path: Optional[str] = None
    special_names: Optional[tuple] = None
    out_index: Optional[bool] = False

    def __init__(self, *args, **kwargs):
        from .error_logger import log_eseas_error, setup_eseas_logger

        # Map positional arguments to kwargs if they were passed
        if args:
            arg_names = ["demetra_folder", "java_folder", "local_folder"]
            for i, arg in enumerate(args):
                if i < len(arg_names) and arg_names[i] not in kwargs:
                    kwargs[arg_names[i]] = arg

        try:
            super().__init__(**kwargs)
            try:
                setup_eseas_logger()
            except Exception:
                pass
        except Exception as e:
            error_msg = f"{str(e)}\n{traceback.format_exc()}"

            class OptsWrapper:
                def __init__(self, d):
                    for k, v in d.items():
                        setattr(self, k, v)

            log_eseas_error(error_msg, OptsWrapper(kwargs))
            try:
                setup_eseas_logger()
            except Exception:
                pass
            raise

    @model_validator(mode="after")
    def apply_logic(self):
        # If auto_download is True, automatically fetch the cruncher directly to java_folder
        if self.auto_download:
            from .download_tools import download_jwsacruncher

            target_path = (
                pathlib.Path(self.java_folder)
                if self.java_folder
                else pathlib.Path.home() / ".eseas"
            )
            self.java_folder = str(download_jwsacruncher(target_path))

        dem_folder = DemetraFolder(self.demetra_folder)
        jav_folder = CruncherFolder(self.java_folder)
        loc_folder = WorkspaceFolder(self.local_folder)
        jav_bin = JavaBinFolder(self.java_bin) if self.java_bin else None

        self.demetra_folder = str(dem_folder)
        self.java_folder = str(jav_folder)
        self.local_folder = str(loc_folder)
        self.java_bin = str(jav_bin) if jav_bin else None

        self.general_params_path = (
            self.general_params_path
            if self.general_params_path
            else str(pathlib.Path.cwd() / "general.params")
        )

        self.set_options(self.workspace_mode)
        so = SingleOptions()
        so.set_items(self)
        return self

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
            java_bin = {self.java_bin},
            replace_general_params={self.replace_general_params},
            csvlayout="{self.csvlayout}",
            general_params_path="{self.general_params_path}",
            special_names="{self.special_names}"
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
