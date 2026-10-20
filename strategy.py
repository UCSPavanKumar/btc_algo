from dotenv import load_dotenv  
from access import get_secret
load_dotenv()
import os
from delta import DeltaClient

dc = DeltaClient()
strike_price = dc.decide_strike_price()
contracts = dc.get_tickers_by_contracts('BTC','21-10-2026')
products = contracts[contracts['strike_price']==str(strike_price)]
ids = products['product_id'].to_list()
print(ids)
dc.place_basket_order(ids)
