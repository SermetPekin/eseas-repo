from pathlib import Path
import os

import pandas as pd

from evdspy.EVDSlocal.common.file_classes import FileItem

# eseas
from eseas.core.seasonal_options import SeasonalOptions as Options
from eseas.core.seas_utils import get_xml_demetra


def make_float(d: pd.DataFrame):
    if "Unnamed: 0" in d.columns:
        cols = d.columns.drop("Unnamed: 0")
    else:
        cols = d.columns.to_list()[1:]
    d[cols] = d[cols].astype(str).apply(lambda x: x.str.replace(",", ".").astype(float))
    return d


def collect_parts_of_results(
    options: Options,
    xml_folders=None,
    out_folder=None,
    out_file_name="combined",
    encoding="latin-1",
):
    parts = options.result_file_names
    if xml_folders is None:
        files: list[FileItem] = get_xml_demetra(options.demetra_folder)
        xml_folders = [Path(x.file_name).stem for x in files]
    sheets = list()
    for xml_folder in xml_folders:

        for part in parts:
            try:
                source_file = (
                    Path(options.local_folder)
                    / rf"test_output\{xml_folder}\SAProcessing-1\series_{part}.csv"
                )
                sheet = pd.read_csv(
                    source_file,
                    encoding=encoding,
                    delimiter=";",
                )

                sheet = make_float(sheet)
                sheets.append(sheet)
            except:
                import traceback
                traceback.print_exc()
                print(f"passing collecting {part} from {source_file}")

        if out_folder is None:
            out_file_name_full = (
                Path(options.local_folder)
                / "test_output"
                / xml_folder
                / f"{out_file_name}.xlsx"
            )
        else:
            dest_folder = Path(out_folder) / xml_folder
            os.makedirs(dest_folder, exist_ok=True)

            out_file_name_full = dest_folder / f"{out_file_name}.xlsx"

        with pd.ExcelWriter(out_file_name_full) as writer:
            for part, sheet in zip(parts, sheets):
                sheet.to_excel(writer, sheet_name=part)
            print(f"[created] {out_file_name_full}")
