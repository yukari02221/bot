from web3 import Web3

# PancakeSwapのファクトリーコントラクトアドレスとABI
PANCAKESWAP_FACTORY_ADDRESS = '0xca143ce32fe78f1f7019d7d551a6402fc5350c73'
PANCAKESWAP_FACTORY_ABI = '[{"constant":true,"inputs":[{"name":"tokenA","type":"address"},{"name":"tokenB","type":"address"}],"name":"getPair","outputs":[{"name":"pair","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'

# BNBとUSDTのトークンコントラクトアドレス
BNB_ADDRESS = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'  # Wrapped BNB (WBNB)
USDT_ADDRESS = '0x55d398326f99059fF775485246999027B3197955'

# BSCのRPCエンドポイント
BSC_RPC_URL = 'https://bsc-dataseed.binance.org/'

# Web3インスタンスを作成
web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# チェックサムアドレスに変換
PANCAKESWAP_FACTORY_ADDRESS = Web3.to_checksum_address(PANCAKESWAP_FACTORY_ADDRESS)
BNB_ADDRESS = Web3.to_checksum_address(BNB_ADDRESS)
USDT_ADDRESS = Web3.to_checksum_address(USDT_ADDRESS)

# PancakeSwapのファクトリーコントラクトを作成
factory_contract = web3.eth.contract(address=PANCAKESWAP_FACTORY_ADDRESS, abi=PANCAKESWAP_FACTORY_ABI)

# BNB/USDTペアのアドレスを取得
pair_address = factory_contract.functions.getPair(BNB_ADDRESS, USDT_ADDRESS).call()

# チェックサムアドレスに変換
pair_address = Web3.to_checksum_address(pair_address)

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

# ペアコントラクトを作成
pair_contract = web3.eth.contract(address=pair_address, abi=PAIR_ABI)

# リザーブ（プール内のトークンの量）を取得
reserves = pair_contract.functions.getReserves().call()

# スワップレートを計算
reserve_bnb = reserves[0]
reserve_usdt = reserves[1]
bnb_usdt_rate = reserve_usdt / reserve_bnb

# 1USD = 155JPY のレートでBNBを円に換算
usd_to_jpy_rate = 157
bnb_to_usd_price = 1 / bnb_usdt_rate  # 1 USDT が何 BNB かを逆にして、1 BNB が何 USDT かに変換
bnb_to_jpy_price = bnb_to_usd_price * usd_to_jpy_rate

print(f"Current BNB/USDT swap rate: {bnb_usdt_rate}")
print(f"Current BNB price in JPY: {bnb_to_jpy_price}")