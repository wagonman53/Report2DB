import pandas as pd
from typing import Optional
from sqlalchemy import create_engine


def save_table(
    df: pd.DataFrame,
    table_name: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    database: str = "postgres",
    user: str = "postgres",
) -> None:
    try:
        conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

        engine = create_engine(conn_string)

        df.to_sql(
        name=table_name,
        con=engine,
        if_exists='replace',  # テーブルが存在する場合は置き換え
        index=False,
        schema='public'
    )

        print(f"{table_name} 正常に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise

    finally:
        if 'engine' in locals():
            engine.dispose()