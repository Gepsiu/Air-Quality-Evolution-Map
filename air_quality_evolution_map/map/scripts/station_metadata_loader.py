from pathlib import Path

import environ
import pandas as pd
from openpyxl import load_workbook
from sqlalchemy import create_engine

env = environ.Env()

ENGINE = create_engine(
    'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(env("DB_USER"), env("DB_PASSWORD"),
                                                  env("DB_HOST"), env("DB_PORT"), env("DB_NAME")))
FILE_PATH = r'C:\Users\d_pio\PycharmProjects\air_pollution\Metadane oraz kody stacji i stanowisk pomiarowych.xlsx'


def update_table(df: pd.DataFrame, table_name: str):
    df.to_sql(
        table_name,
        con=ENGINE,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )


def file_converter(path: str) -> pd.DataFrame:
    workbook = load_workbook(path)
    ws = workbook.active

    station_code = list(ws.iter_cols(min_col=2, min_row=2, max_col=2, values_only=True))[0]
    voivodeship = list(ws.iter_cols(min_col=11, min_row=2, max_col=11, values_only=True))[0]
    outdated_station_code = list(ws.iter_cols(min_col=5, min_row=2, max_col=5, values_only=True))[0]
    rows = list(zip(station_code, voivodeship, outdated_station_code))
    return pd.DataFrame(rows).dropna(how='all')


def process_file(path):
    df_converted = file_converter(path)
    df_converted.columns = ['code', 'voivodeship', 'outdated_code']
    update_table(df_converted, 'stations')
    file_name = Path(path).name
    print(f"Finished: {file_name}")


def main():
    try:
        process_file(FILE_PATH)
    except Exception as e:
        print(f"[ERROR] File: {FILE_PATH}: {e}")


if __name__ == "__main__":
    main()
