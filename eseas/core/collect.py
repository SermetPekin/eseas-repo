from pathlib import Path
import os

import pandas as pd

from evdspy.EVDSlocal.common.file_classes import FileItem

# eseas
from eseas.core.seasonal_options import SeasonalOptions as Options
from eseas.core.seas_utils import get_xml_demetra
from eseas.core.cruncher_classes import get_cruncher


def make_float(d: pd.DataFrame):
    if "Unnamed: 0" in d.columns:
        cols = d.columns.drop("Unnamed: 0")
    else:
        cols = d.columns.to_list()[1:]
    d[cols] = d[cols].astype(str).apply(lambda x: x.str.replace(",", ".").astype(float))
    return d


class ResultCollector:
    """
    Collects seasonality result parts (sa, s, cal, etc.) and compiles them into Excel resources.
    """
    def __init__(
        self,
        options: Options,
        out_folder: str = None,
        out_file_name: str = "combined",
        encoding: str = "latin-1",
    ):
        self.options = options
        self.out_folder = out_folder
        self.out_file_name = out_file_name
        self.encoding = encoding
        self.parts = options.result_file_names

    def get_xml_folders(self, xml_folders: list = None) -> list:
        if xml_folders is not None:
            return xml_folders
        files: list[FileItem] = get_xml_demetra(self.options.demetra_folder)
        return [Path(x.file_name).stem for x in files]

    def get_source_file(self, xml_folder: str, part: str) -> Path:
        return (
            Path(get_cruncher().local_work_space)
            / "test_output"
            / xml_folder
            / "SAProcessing-1"
            / f"series_{part}.csv"
        )

    def load_sheet(self, source_file: Path) -> pd.DataFrame:
        sheet = pd.read_csv(
            source_file,
            encoding=self.encoding,
            delimiter=";",
        )
        return make_float(sheet)

    def get_output_file_name(self, xml_folder: str) -> Path:
        if self.out_folder is None:
            out_file_name_full = (
                Path(self.options.local_folder)
                / "test_output"
                / xml_folder
                / f"{self.out_file_name}.xlsx"
            )
            os.makedirs(out_file_name_full.parent, exist_ok=True)
        else:
            dest_folder = Path(self.out_folder) / xml_folder
            os.makedirs(dest_folder, exist_ok=True)
            out_file_name_full = dest_folder / f"{self.out_file_name}.xlsx"
        return out_file_name_full

    def process_folder(self, xml_folder: str):
        # We explicitly store parts in a dictionary to prevent zip mismatch
        # in case a specific part fails to load.
        sheets_data = {}
        for part in self.parts:
            source_file = self.get_source_file(xml_folder, part)
            try:
                sheets_data[part] = self.load_sheet(source_file)
            except Exception:
                import traceback
                traceback.print_exc()
                print(f"passing collecting {part} from {source_file}")

        if not sheets_data:
            return

        out_file_name_full = self.get_output_file_name(xml_folder)
        with pd.ExcelWriter(out_file_name_full) as writer:
            for part, sheet in sheets_data.items():
                sheet.to_excel(writer, sheet_name=part)
        print(f"[created] {out_file_name_full}")

    def collect(self, xml_folders=None):
        folders = self.get_xml_folders(xml_folders)
        for xml_folder in folders:
            self.process_folder(xml_folder)


def collect_parts_of_results(
    options: Options,
    xml_folders=None,
    out_folder=None,
    out_file_name="combined",
    encoding="latin-1",
):
    """
    Collects parts of results using the ResultCollector class.
    """
    collector = ResultCollector(
        options=options,
        out_folder=out_folder,
        out_file_name=out_file_name,
        encoding=encoding,
    )
    collector.collect(xml_folders)
