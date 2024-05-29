import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta

def create_and_save_chart(csv_filename, output_filename_prefix):
    try:
        # CSVファイルを読み込む
        data = pd.read_csv(csv_filename)

        # タイムスタンプを日時形式に変換
        data['Timestamp (JST)'] = pd.to_datetime(data['Timestamp (JST)'])

        # グラフを作成
        plt.figure(figsize=(10, 6))
        plt.plot(data['Timestamp (JST)'], data['BNB Price in JPY'], label='BNB Price in JPY')

        # グラフの装飾
        plt.xlabel('Time (JST)')
        plt.ylabel('BNB Price in JPY')
        plt.title('BNB Price in JPY Over Time')
        plt.legend()
        plt.grid(True)

        # 現在の東京時刻を取得
        jst_time = datetime.now(timezone.utc) + timedelta(hours=9)
        jst_time_str = jst_time.strftime('%Y%m%d_%H%M%S')

        # グラフを画像として保存（東京時刻をファイル名に追加）
        output_filename = f'{output_filename_prefix}_{jst_time_str}.png'
        plt.savefig(output_filename)
        plt.close()

        return True, output_filename
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None
