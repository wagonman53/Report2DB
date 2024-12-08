import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def save_table(
    df: pd.DataFrame,
    table_name: str,
) -> None:
    try:
        # 環境変数から接続情報を取得
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        database = os.getenv("DB_NAME", "postgres")

        if not all([user, password, host, port, database]):
            raise ValueError("必要なDB接続情報が.envファイルに設定されていません。")

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