from rich import print
import pandas as pd
from evdspy.EVDSlocal.common.file_classes import file_items_update, FileItem
from .df_operations import make_df_float
from .seas_utils import get_xml_demetra, display

from ._options import demetra_command_file_name


def get_demetra_files(folder) -> list[FileItem]:
    xml_demetra = get_xml_demetra(folder)
    display(xml_demetra)
    xml_demetra = file_items_update(xml_demetra)  # [0:4]
    return xml_demetra


def convert_df_general(df: pd.DataFrame) -> pd.DataFrame:
    def ay_yil(yil, num, baslangic_ay):
        def ay_hesapla():
            ay = (num + baslangic_ay) % int(period)
            if ay == 0:
                return 12
            return ay

        def yil_hesapla():
            artik = 0
            if num + baslangic_ay > 12:
                artik = 1
            return yil + artik

        sonuc = yil_hesapla() * 100 + ay_hesapla()
        return sonuc

    df.index = range(len(df))
    df_new = df.copy()
    df_new.drop([0, 1, 2, 3, 4], axis=0, inplace=True)
    period = list(df.iloc[1])[0]
    baslangic_yil = list(df.iloc[2])[0]
    baslangic_ay = list(df.iloc[3])[0]
    adet = list(df.iloc[4])[0]
    adet = int(adet)
    liste = tuple(ay_yil(baslangic_yil, x, baslangic_ay) for x in range(adet))
    df_new.columns = df.iloc[0]
    df_new["donem"] = liste
    df_new.set_index("donem", drop=True, inplace=True)
    df_new = make_df_float(df_new)
    return df_new


def show_title(msg: str) -> None:
    print("=" * 50)
    print(" " * 5, msg)
    print("=" * 50)


def write_bat_file_demetra(xml_demetra, file_name=demetra_command_file_name) -> None:
    from .create_bat_command import (
        create_command,
        copy_xml_files_local,
        copy_folder_demetra,
        write_bat_file,
    )

    cmds = create_command(xml_demetra)
    copy_xml_files_local(xml_demetra)
    copy_folder_demetra(xml_demetra)
    text = "".join(cmds)
    show_title(f"Creating command file to call `jwsacruncher` : [{file_name}]")

    write_bat_file(text, file_name)
