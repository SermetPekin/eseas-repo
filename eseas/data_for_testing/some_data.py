import pandas as pd
from io import StringIO
from typing import Tuple, Callable
from dataclasses import dataclass


if "main_" in __name__:
    from csv_content import template_csv, air_passenger
else:
    from .csv_content import template_csv, air_passenger


@dataclass
class eseas_DataFrame:
    name: str
    raw: str = None
    process_fnc: Callable = None
    df: pd.DataFrame = None

    def get_df(self) -> None:
        csv = StringIO(self.raw)
        df = pd.read_csv(csv, sep=";")
        self.df = df

    def process(self) -> None:
        self.get_df()

        if self.process_fnc is None:
            return
        self.df = self.process_fnc(self.df)

    def __str__(self) -> str:

        return f"<eseasDataFrame>{self.name}<name, df, raw>"

    def __repr__(self) -> str:
        return self.__str__()

    def to_df(self) -> pd.DataFrame:
        return self.df


def process_bal(df: pd.DataFrame) -> pd.DataFrame:
    if "Tarih" in df.columns:
        df = df.drop(["Unnamed: 4"], axis=1)
        df.set_index("Tarih", inplace=True)
    return df


def process_air(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["Month"], format="%Y-%m")
    df.drop(["Month"], axis=1, inplace=True)
    df = df[["date", "#Passengers"]]

    return df


def get_sample_ts(template: str, name: str, fnc: Callable) -> eseas_DataFrame:

    e = eseas_DataFrame(name, template, fnc)
    e.process()
    return e


def get_sample_ts2(template: str, name: str) -> eseas_DataFrame:
    csv = StringIO(template)
    df = pd.read_csv(csv, sep=";")
    return eseas_DataFrame(name, df, template)


class SampleData:
    def get(self) -> list[eseas_DataFrame]:
        bal = get_sample_ts(template_csv, "bal", process_bal)
        air = get_sample_ts(air_passenger, "air", process_air)
        return [bal, air]


def get_sample_data() -> Tuple[eseas_DataFrame]:
    a = SampleData().get()
    # print(a)
    _ = tuple(map(check, a))
    return a


def check(e: eseas_DataFrame):
    print(e.name, "name ")
    print(e.df.columns.to_list(), "cols")
    print(e)
    assert isinstance(e, eseas_DataFrame)
    df = e.to_df()
    assert isinstance(df, pd.DataFrame)


if "main_" in __name__:

    a = SampleData().get()
    print(a)
    _ = tuple(map(check, a))
