from dotenv import load_dotenv  
from access import get_secret
load_dotenv()
from datetime import datetime
import os
from delta import DeltaClient

dc = DeltaClient()
expiry_date = datetime.now().strftime('%d-%m-%Y')
strike_price = dc.decide_strike_price()
contracts = dc.get_tickers_by_contracts('BTC',expiry_date,'call_options,put_options')
products = contracts[contracts['strike_price']==str(strike_price)]
if len(products)==0:
    products = contracts[contracts['strike_price']==str(strike_price-100)]
ids = products['product_id'].to_list()
dc.place_basket_order(ids)
