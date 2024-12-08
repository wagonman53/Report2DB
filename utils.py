from pathlib import Path

def get_file_paths():
    # reportフォルダのパスを取得
    report_dir = Path('report')
    
    # 結果を格納する辞書
    processed_folders = {}
    
    # reportフォルダが存在することを確認
    if not report_dir.exists():
        raise FileNotFoundError("'report' フォルダが見つかりません")
    
    # reportフォルダ内のすべてのフォルダを処理
    for folder in report_dir.iterdir():
        if folder.is_dir():  # フォルダの場合のみ処理
            folder_paths = {}
            required_files = ['report_OOP_Full.csv', 'report_IP_Full.csv', 'report.csv']
            
            # フォルダ内のファイルを確認
            folder_files = [f.name for f in folder.iterdir() if f.is_file()]
            
            # 必要なファイルがすべて存在するか確認
            if all(file in folder_files for file in required_files):
                # 各CSVファイルのパスを保存
                for csv_file in required_files:
                    file_path = folder / csv_file
                    folder_paths[csv_file.replace('.csv', '')] = file_path
                
                # 処理したパスを辞書に格納
                processed_folders[folder.name] = folder_paths
            else:
                print(f"注意: {folder.name}フォルダには必要なCSVファイルがすべて揃っていません")
    
    return processed_folders


def get_action_columns(df):
    keywords = ["BET","RAISE","CALL","FOLD","CHECK"]

    columns = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword.lower() in col_lower for keyword in keywords):
            columns.append(col)
    
    return columns


def check_position(df, case_sensitive=False):
    columns = df.columns.tolist()
    keywords = ["BET","RAISE","CALL","FOLD","CHECK"]
    
    if not case_sensitive:
        columns = [col.lower() for col in columns]
        keywords = [keyword.lower() for keyword in keywords]
    
    for keyword in keywords:
        for col in columns:
            if keyword in col:
                return True
    
    return False