import csv
import time
import asyncio
from web3 import Web3
from datetime import datetime, timezone, timedelta

class PancakeSwapPriceLogger:
    def __init__(self, bsc_rpc_url, factory_address, factory_abi, bnb_address, usdt_address, pair_abi, csv_filename, usd_to_jpy_rate):
        self.web3 = Web3(Web3.HTTPProvider(bsc_rpc_url))
        self.factory_address = Web3.to_checksum_address(factory_address)
        self.factory_abi = factory_abi
        self.bnb_address = Web3.to_checksum_address(bnb_address)
        self.usdt_address = Web3.to_checksum_address(usdt_address)
        self.pair_abi = pair_abi
        self.csv_filename = csv_filename
        self.usd_to_jpy_rate = usd_to_jpy_rate
        self.factory_contract = self.web3.eth.contract(address=self.factory_address, abi=self.factory_abi)
        self.pair_address = Web3.to_checksum_address(self.factory_contract.functions.getPair(self.bnb_address, self.usdt_address).call())
        self.pair_contract = self.web3.eth.contract(address=self.pair_address, abi=self.pair_abi)
        self._initialize_csv()

    def _initialize_csv(self):
        with open(self.csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp (UTC)', 'Timestamp (JST)', 'BNB/USDT Rate', 'BNB Price in JPY'])

    def get_swap_rate(self):
        reserves = self.pair_contract.functions.getReserves().call()
        reserve_bnb = reserves[0]
        reserve_usdt = reserves[1]
        bnb_usdt_rate = reserve_usdt / reserve_bnb
        bnb_to_usd_price = 1 / bnb_usdt_rate
        bnb_to_jpy_price = bnb_to_usd_price * self.usd_to_jpy_rate
        return bnb_usdt_rate, bnb_to_jpy_price

    def log_price(self):
        bnb_usdt_rate, bnb_to_jpy_price = self.get_swap_rate()
        utc_timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        jst_timestamp = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
        with open(self.csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([utc_timestamp, jst_timestamp, bnb_usdt_rate, bnb_to_jpy_price])
        print(f"{utc_timestamp} (UTC) / {jst_timestamp} (JST) - BNB/USDT swap rate: {bnb_usdt_rate}, BNB price in JPY: {bnb_to_jpy_price}")

    async def start_logging(self, interval=60):
        while True:
            self.log_price()
            await asyncio.sleep(interval)
