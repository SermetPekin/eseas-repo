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


def convert_df_number(df: pd.DataFrame, except_columns=()):
    def convert_number_item(item):
        try:
            new_number = sayi_donustur(item)  # float(str(item).replace(",", "."))
        except Exception as exc:
            print(item)
            print(exc)
            new_number = 0
            # new_number = -987654321.0123
            # raise exc
        return new_number

    def convert_numbers(numbers):
        return tuple(map(convert_number_item, numbers))

    for column in list(df.columns):
        if column not in except_columns:
            df[column] = convert_numbers(list(df[column]))
        else:
            ...
            # print("passing...", column)
    return df


def make_df_float(df):
    except_columns = ("donem",)
    df = convert_df_number(df, except_columns)
    return df


def test_make_float():
    data_dict = {
        "donem": ["200201", "200202"],
        "kolon1": ["60,8456", "66,12656"],
        "kolon2": ["60,8456", "66,12656"],
    }
    df = pd.DataFrame.from_records(data_dict)
    new_df = make_df_float(df)
    print(new_df.head())
