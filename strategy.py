from dotenv import load_dotenv  
from access import get_secret
load_dotenv()
import math
import os
from delta import DeltaClient

dc = DeltaClient()
ltp = dc.get_current_price('BTCUSD')
strike_price = math.ceil(ltp/100)*100
data = dc.get_tickers_by_contracts('BTC','21-10-2026')
print("LTP: ",ltp,"Strike Price :",strike_price)
products = data[data['strike_price']==str(strike_price)]
ids = products['product_id'].to_list()
dc.place_basket_order(ids
