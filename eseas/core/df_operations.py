from typing import Tuple, Optional

import pandas as pd
from pathlib import Path


def get_rand_hash(num=5) -> str:
    import secrets

    return secrets.token_urlsafe(nbytes=num)


def try_to_write_excel(df: pd.DataFrame, file_name: Path) -> None:
    try:
        df.to_excel(file_name)
    except Exception:
        pa = file_name.parent
        hash_ = get_rand_hash(5)
        file_name_new = file_name.stem + f"_{hash_}.xlsx"
        print(Path(pa) / file_name_new)
        df.to_excel(Path(pa) / file_name_new)


def rreplace(st: str, e, y) -> str:
    if e not in st:
        return st
    st = st.replace(e, y)
    return rreplace(st, e, y)


def sayi_donustur(pot_sayi: str) -> float:
    if not pot_sayi:
        return pot_sayi
    try:
        if isinstance(pot_sayi, float):
            return pot_sayi
        if str(pot_sayi).isnumeric():
            return float(pot_sayi)
        pot_sayi = str(pot_sayi)
        pot_sayi = rreplace(pot_sayi, ".", "")
        pot_sayi = pot_sayi.replace(",", ".")
        if not pot_sayi.replace(".", "").isnumeric():
            return pot_sayi
        return float(pot_sayi)
    except Exception:
        return pot_sayi


def convert_df_number(df: pd.DataFrame, except_columns: Tuple[str] = ()):
    def convert_number_item(item):
        try:
            new_number = sayi_donustur(item)  # float(str(item).replace(",", "."))
        except Exception as exc:
            print(item)
            print(exc)
            new_number = 0

        return new_number

    def convert_numbers(numbers):
        return tuple(map(convert_number_item, numbers))

    if except_columns is None:
        except_columns = tuple()
    for column in df.columns:
        if column in except_columns:
            continue
        df[column] = convert_numbers(list(df[column]))


    return df


def make_df_float(df: pd.DataFrame, except_columns: Optional[Tuple[str]] = None):
    if except_columns is None:
        except_columns = ("donem",)
    df = convert_df_number(df, except_columns)
    return df
