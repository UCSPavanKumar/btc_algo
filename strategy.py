from dotenv import load_dotenv  
from access import get_secret
load_dotenv()

import os
from delta import DeltaClient

dc = DeltaClient()
ltp = dc.get_current_price('BTCUSD')
data = dc.get_tickers_by_contracts('BTC','21-10-2026')
dc.place_basket_order([158952,158962])
