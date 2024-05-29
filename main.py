from pancake_price import PancakeSwapPriceLogger
from Discord import send_discord_message, send_discord_image
from make_image import create_and_save_chart
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone, timedelta
import asyncio
import sys

async def main():
    # PancakeSwapのファクトリーコントラクトアドレスとABI
    PANCAKESWAP_FACTORY_ADDRESS = '0xca143ce32fe78f1f7019d7d551a6402fc5350c73'
    PANCAKESWAP_FACTORY_ABI = '[{"constant":true,"inputs":[{"name":"tokenA","type":"address"},{"name":"tokenB","type":"address"}],"name":"getPair","outputs":[{"name":"pair","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'

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
            "stateMutability": "view",
            "type": "function"
        }
    ]
    '''

    # CSVファイル名
    CSV_FILENAME = 'bnb_usdt_price.csv'

    # 1USD = 155JPY のレート
    USD_TO_JPY_RATE = 155

    # Discord Webhook URL
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1245371669648900187/aKCeSl08YPUOfNl8tmsSZ424jXJTr6ysFdRtTnrgvVoMvHbdat1BoFrXpZtD8QiszlpO"

    # PancakeSwapPriceLoggerのインスタンスを作成
    logger = PancakeSwapPriceLogger(BSC_RPC_URL, PANCAKESWAP_FACTORY_ADDRESS, PANCAKESWAP_FACTORY_ABI, BNB_ADDRESS, USDT_ADDRESS, PAIR_ABI, CSV_FILENAME, USD_TO_JPY_RATE)

    # ロギングを非同期に開始
    logging_task = asyncio.create_task(logger.start_logging(interval=60))

    # 30秒待機してからグラフを作成
    await asyncio.sleep(30)

    # グラフを作成し保存
    success, output_filename = create_and_save_chart(CSV_FILENAME, 'bnb_price_chart')

    # グラフの作成に成功した場合、Discordに画像を送信
    if success:
        send_discord_image(DISCORD_WEBHOOK_URL, output_filename)
    else:
        sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
