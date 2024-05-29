from pancake_price import PancakeSwapPriceLogger
from Discord import send_discord_message, send_discord_image
from make_image import create_and_save_chart
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone, timedelta
import asyncio
import sys

async def schedule_task_at(target_hour, target_minute):
    while True:
        now = datetime.now(timezone.utc) + timedelta(hours=9)  # 現在の東京時刻を取得
        target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)
        await perform_task()

async def perform_task():
    # CSVファイル名
    CSV_FILENAME = 'bnb_usdt_price.csv'

    # Discord Webhook URL
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1245371669648900187/aKCeSl08YPUOfNl8tmsSZ424jXJTr6ysFdRtTnrgvVoMvHbdat1BoFrXpZtD8QiszlpO"

    # グラフを作成し保存
    success, output_filename = create_and_save_chart(CSV_FILENAME, 'bnb_price_chart')

    # グラフの作成に成功した場合、Discordに画像を送信
    if success:
        send_discord_image(DISCORD_WEBHOOK_URL, output_filename)
    else:
        sys.exit()

async def main():
    # PancakeSwapのファクトリーコントラクトアドレスとABI
    PANCAKESWAP_FACTORY_ADDRESS = '0xca143ce32fe78f1f7019d7d551a6402fc5350c73'
    PANCAKESWAP_FACTORY_ABI = '[{"constant":true,"inputs":[{"name":"tokenA","type":"address"},{"name":"tokenB","type":"address"}],"name":"getPair","outputs":[{"name":"pair","type":"address"}],"payable":false,"stateMutility":"view","type":"function"}]'

    # BNBとUSDTのトークンコントラクトアドレス
    BNB_ADDRESS = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'  # Wrapped BNB (WBNB)
    USDT_ADDRESS = '0x55d398326f99059fF775485246999027B3197955'

    # BSCのRPCエンドポイント
    BSC_RPC_URL = 'https://bsc-dataseed.binance.org/'

    # ペアコントラクトのABI（一般的なUniswap v2のペアコントラクトのABIを使用）
    PAIR_ABI = '''
    [
        {
            "constant": true,
            "inputs": [],
            "name": "getReserves",
            "outputs": [
                { "name": "_reserve0", "type": "uint112" },
                { "name": "_reserve1", "type": "uint112" },
                { "name": "_blockTimestampLast", "type": "uint32" }
            ],
            "payable": false,
            "stateMutility":"view",
            "type":"function"
        }
    ]
    '''

    # 1USD = 155JPY のレート
    USD_TO_JPY_RATE = 155

    # CSVファイル名
    CSV_FILENAME = 'bnb_usdt_price.csv'

    # PancakeSwapPriceLoggerのインスタンスを作成
    logger = PancakeSwapPriceLogger(BSC_RPC_URL, PANCAKESWAP_FACTORY_ADDRESS, PANCAKESWAP_FACTORY_ABI, BNB_ADDRESS, USDT_ADDRESS, PAIR_ABI, CSV_FILENAME, USD_TO_JPY_RATE)

    # ロギングを非同期に開始
    logging_task = asyncio.create_task(logger.start_logging(interval=60))

    # 特定の東京時刻でタスクをスケジュール
    schedule_tasks = [
        schedule_task_at(9, 0),  # 毎日午前9時
        schedule_task_at(21, 0)  # 毎日午後9時
    ]

    await asyncio.gather(logging_task, *schedule_tasks)

if __name__ == "__main__":
    asyncio.run(main())
