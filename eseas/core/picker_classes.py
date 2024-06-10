import traceback
from abc import ABC
from pathlib import Path
import pandas as pd
from evdspy.EVDSlocal.common.file_classes import FileItem
from ._options import middle_folder
from .cruncher_classes import get_cruncher
from .demetra import convert_df_general
from .demetra_file_naming import get_meaning_demetra_file


'''
    `FilePicker`s 
    These classes will harvest data after cruncher runs 
    will convert them to pandas dataframe 
    
'''

class FilePicker(ABC):
    def __init__(
        self,
        file_item,
        names=(
            "sa",
            "s",
            "cal",
        ),
    ):
        self.file_item = file_item
        self.names = names


class OutFilePicker(FilePicker):
    def __init__(
        self,
        file_item,
        names=(
            "sa",
            "s",
            "cal",
        ),
        file_name_explanation=True,
    ):
        super().__init__(file_item, names)
        self.file_name_explanationOption = file_name_explanation

    def process_file(self, file_name, name)->None :
        df = pd.read_csv(
            file_name,
            engine="python",
            encoding="unicode_escape",
            sep=";",
            index_col=False,
            header=None,
        )
        df = df.T
        df = convert_df_general(df)
        df.to_excel(
            get_name_format(
                self.file_item, name, get_explanation=self.file_name_explanationOption
            )
        )

    def pick_files(self):
        for name in self.names:
            try:
                self.process_file(get_file_name_x(self.file_item, name), name)
            except Exception:
                traceback.print_exc()
                print(f"This type of output [{name}] was not found in JDemetra output!")


def get_file_name_x(x: FileItem, name="sa")->Path :
    """while reading output files"""
    explanation = get_explanation_if_neces(name, False)
    # middle_folder: 'test_output'
    return (
        Path()
        / get_cruncher().local_work_space
        / middle_folder
        / x.encoded_name
        / "SAProcessing-1"
        / f"series_{name}{explanation}.csv"
    )


def get_explanation_if_neces(name_type, get_explanation=False)->str :
    if not get_explanation:
        return ""
    name_exp = get_meaning_demetra_file(name_type)
    if not name_exp:
        name_exp = "explanation_na"
    name_exp = "_{" + name_exp + "}"
    if not get_explanation:
        name_exp = ""
    return name_exp


def get_name_format(file_item: FileItem, name_type="sa", get_explanation=True)->Path :
    """While writing output files"""
    explanation = get_explanation_if_neces(name_type, get_explanation)
    if not isinstance(file_item, FileItem):
        return Path("None.xlsx")
    return Path(get_cruncher().local_work_space) / str(
        file_item.short_name + f"_{name_type}{explanation}_evdspy_" + ".xlsx"
    )
